"""
Módulo para extração de texto de imagens usando AWS Textract.
Substitui OCR local por serviço em nuvem da AWS para maior precisão.
"""

import boto3
import re
import os
from typing import Dict, Optional
import base64


class OCRAws:
    def __init__(self, region_name='us-east-1'):
        """
        Inicializa o cliente AWS Textract.
        
        Args:
            region_name: Região AWS para usar o serviço
        """
        try:
            self.textract = boto3.client('textract', region_name=region_name)
            print("✅ AWS Textract inicializado!")
        except Exception as e:
            print(f"❌ Erro ao inicializar AWS Textract: {e}")
            print("💡 Verifique suas credenciais AWS com: aws configure")
            raise
    
    def extrair_texto_aws(self, caminho_imagem: str) -> str:
        """
        Extrai texto de uma imagem usando AWS Textract.
        
        Args:
            caminho_imagem: Caminho para o arquivo de imagem
            
        Returns:
            Texto extraído da imagem
        """
        try:
            # Lê o arquivo de imagem
            with open(caminho_imagem, 'rb') as image_file:
                image_bytes = image_file.read()
            
            # Chama AWS Textract
            response = self.textract.detect_document_text(
                Document={'Bytes': image_bytes}
            )
            
            # Extrai o texto dos blocos
            texto_completo = []
            for block in response['Blocks']:
                if block['BlockType'] == 'LINE':
                    texto_completo.append(block['Text'])
            
            return '\n'.join(texto_completo)
            
        except Exception as e:
            print(f"❌ Erro ao processar imagem com AWS Textract: {e}")
            return ""
    
    def extrair_cnpj(self, texto: str) -> Optional[str]:
        """
        Extrai CNPJ do texto usando expressões regulares.
        
        Args:
            texto: Texto extraído do OCR
            
        Returns:
            CNPJ encontrado (apenas números) ou None se não encontrado
        """
        # Limpa o texto
        texto_limpo = re.sub(r'[^\w\s\.\-\/]', ' ', texto)
        texto_limpo = re.sub(r'\s+', ' ', texto_limpo)
        
        # Padrões para CNPJ
        padroes_cnpj = [
            # CNPJ formatado completo
            r'CNPJ[:\s]*(\d{2}\.?\d{3}\.?\d{3}\/?\d{4}-?\d{2})',
            # CNPJ sem formatação após palavra CNPJ
            r'CNPJ[:\s]*(\d{14})',
            # Sequência de 14 dígitos isolada
            r'(?:^|\s)(\d{14})(?:\s|$)',
            # Padrão formatado isolado
            r'(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})',
        ]
        
        for padrao in padroes_cnpj:
            matches = re.findall(padrao, texto_limpo, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                # Remove formatação e mantém apenas números
                cnpj_limpo = re.sub(r'[^\d]', '', match)
                # Verifica se tem exatamente 14 dígitos
                if len(cnpj_limpo) == 14:
                    # Validação básica de CNPJ
                    if not cnpj_limpo.startswith('00000') and not all(d == cnpj_limpo[0] for d in cnpj_limpo):
                        return cnpj_limpo
        
        return None
    
    def extrair_valor_total(self, texto: str) -> float:
        """
        Extrai o valor total da compra do texto.
        
        Args:
            texto: Texto extraído do OCR
            
        Returns:
            Valor total encontrado ou 0.0 se não encontrado
        """
        # Padrões para valores monetários
        padroes_valor = [
            # Padrões com palavras-chave
            r'(?:TOTAL|VALOR\s*TOTAL|TOTAL\s*GERAL)[:\s]*R?\$?\s*(\d{1,6}[,.]?\d{2})',
            r'(?:TOTAL|VALOR)[:\s]*R?\$?\s*(\d{1,6}[,.]?\d{2})',
            # Padrões com R$
            r'R\$\s*(\d{1,6}[,.]?\d{2})',
            r'RS\s*(\d{1,6}[,.]?\d{2})',
            # Valores no final de linhas
            r'(\d{1,6}[,.]?\d{2})\s*$',
            # Valores isolados com formato monetário
            r'(?:^|\s)(\d{1,4}[,.]\d{2})(?:\s|$)',
        ]
        
        valores_encontrados = []
        
        # Processa linha por linha
        linhas = texto.split('\n')
        
        for linha in linhas:
            linha = linha.strip()
            if not linha:
                continue
                
            for padrao in padroes_valor:
                matches = re.findall(padrao, linha, re.IGNORECASE)
                for match in matches:
                    try:
                        # Trata diferentes formatos de decimal
                        valor_str = match.replace(',', '.')
                        
                        # Remove pontos que não são decimais (ex: 1.234,50 -> 1234.50)
                        if '.' in valor_str and ',' in match:
                            valor_str = match.replace('.', '').replace(',', '.')
                        
                        valor = float(valor_str)
                        
                        # Filtra valores válidos
                        if 0.01 <= valor <= 999999.99:
                            peso = 1
                            linha_upper = linha.upper()
                            
                            # Aumenta peso baseado no contexto
                            if any(palavra in linha_upper for palavra in ['TOTAL', 'VALOR TOTAL', 'TOTAL GERAL']):
                                peso += 10
                            if 'R$' in linha or 'RS' in linha:
                                peso += 5
                            if linha.strip().endswith(f'{valor:.2f}'.replace('.', ',')):
                                peso += 3
                                
                            valores_encontrados.append((valor, peso))
                            
                    except ValueError:
                        continue
        
        if not valores_encontrados:
            return 0.0
        
        # Retorna o valor com maior peso
        valores_encontrados.sort(key=lambda x: (x[1], x[0]), reverse=True)
        return valores_encontrados[0][0]
    
    def extrair_dados_canhoto(self, caminho_imagem: str) -> Dict:
        """
        Função principal para extrair CNPJ e valor total de um canhoto.
        
        Args:
            caminho_imagem: Caminho para o arquivo de imagem
            
        Returns:
            Dicionário com 'cnpj', 'valor' e 'texto_completo'
        """
        print(f"🔍 Processando: {os.path.basename(caminho_imagem)}")
        
        # Extrai texto da imagem usando AWS Textract
        texto = self.extrair_texto_aws(caminho_imagem)
        
        if not texto:
            print(f"  ⚠️  Não foi possível extrair texto da imagem")
            return {'cnpj': None, 'valor': 0.0, 'texto_completo': ''}
        
        # Extrai CNPJ e valor
        cnpj = self.extrair_cnpj(texto)
        valor = self.extrair_valor_total(texto)
        
        print(f"  📄 CNPJ: {cnpj if cnpj else 'Não encontrado'}")
        print(f"  💰 Valor: R$ {valor:.2f}")
        
        return {
            'cnpj': cnpj,
            'valor': valor,
            'texto_completo': texto
        }


# Função de conveniência
def extrair_dados_canhoto_aws(caminho_imagem: str, region_name: str = 'us-east-1') -> Dict:
    """
    Função de conveniência para usar AWS Textract.
    
    Args:
        caminho_imagem: Caminho para o arquivo de imagem
        region_name: Região AWS para usar o serviço
        
    Returns:
        Dicionário com dados extraídos
    """
    ocr = OCRAws(region_name=region_name)
    return ocr.extrair_dados_canhoto(caminho_imagem)
