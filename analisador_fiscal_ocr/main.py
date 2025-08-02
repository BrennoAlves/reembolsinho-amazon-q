#!/usr/bin/env python3
"""
Analisador Fiscal OCR - Versão AWS Textract
Automatiza a análise de canhotos de maquininha usando AWS Textract para OCR.
"""

import os
import sys
from pathlib import Path

# Adiciona o diretório do projeto ao path
sys.path.append(str(Path(__file__).parent.parent))

from analisador_fiscal_ocr.ocr_aws import extrair_dados_canhoto_aws
from analisador_fiscal_ocr.categorizador import CategorizadorDespesas, categorizar_por_cnae


def encontrar_imagens_canhotos(pasta_canhotos="canhotos"):
    """
    Encontra todas as imagens de canhotos na pasta especificada.
    
    Args:
        pasta_canhotos: Caminho para a pasta com as imagens
        
    Returns:
        Lista de caminhos para as imagens encontradas
    """
    pasta = Path(pasta_canhotos)
    
    if not pasta.exists():
        print(f"❌ Pasta '{pasta_canhotos}' não encontrada!")
        print(f"💡 Crie a pasta e adicione as imagens dos canhotos.")
        return []
    
    # Extensões de imagem suportadas
    extensoes = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']
    imagens = []
    
    for ext in extensoes:
        imagens.extend(pasta.glob(f"*{ext}"))
        imagens.extend(pasta.glob(f"*{ext.upper()}"))
    
    return sorted(imagens)


def processar_canhotos(imagens, region_name='us-east-1'):
    """
    Processa uma lista de imagens de canhotos.
    
    Args:
        imagens: Lista de caminhos para as imagens
        region_name: Região AWS para usar o Textract
        
    Returns:
        Lista de dicionários com os dados extraídos
    """
    resultados = []
    categorizador = CategorizadorDespesas()
    
    print(f"🔍 Encontradas {len(imagens)} imagens para processar")
    print("=" * 60)
    
    for i, caminho_imagem in enumerate(imagens, 1):
        print(f"\n📸 [{i}/{len(imagens)}] Processando imagem...")
        
        try:
            # Extrai dados usando AWS Textract
            dados = extrair_dados_canhoto_aws(str(caminho_imagem), region_name)
            
            if dados['cnpj']:
                # Consulta informações da empresa
                print(f"  🔍 Consultando CNPJ: {dados['cnpj']}")
                info_empresa = categorizador.consultar_cnpj(dados['cnpj'])
                
                if info_empresa:
                    print(f"  🏢 Empresa: {info_empresa['nome']}")
                    print(f"  📋 CNAE: {info_empresa['atividade_principal']}")
                    
                    # Categoriza a despesa
                    categoria = categorizar_por_cnae(info_empresa['atividade_principal'])
                    print(f"  🏷️  Categoria: {categoria}")
                    
                    dados.update({
                        'empresa': info_empresa['nome'],
                        'atividade': info_empresa['atividade_principal'],
                        'categoria': categoria
                    })
                else:
                    print(f"  ⚠️  Não foi possível consultar informações da empresa")
                    dados.update({
                        'empresa': 'Não identificada',
                        'atividade': 'Não identificada',
                        'categoria': 'Outros'
                    })
            else:
                dados.update({
                    'empresa': 'CNPJ não encontrado',
                    'atividade': 'Não identificada',
                    'categoria': 'Outros'
                })
            
            dados['arquivo'] = caminho_imagem.name
            resultados.append(dados)
            print(f"  ✅ Processado com sucesso!")
            
        except Exception as e:
            print(f"  ❌ Erro ao processar: {str(e)}")
            # Adiciona resultado com erro
            resultados.append({
                'arquivo': caminho_imagem.name,
                'cnpj': None,
                'valor': 0.0,
                'empresa': 'Erro no processamento',
                'atividade': 'Erro',
                'categoria': 'Outros',
                'texto_completo': ''
            })
    
    return resultados


def gerar_relatorio(resultados):
    """
    Gera relatório de gastos por categoria.
    
    Args:
        resultados: Lista de resultados do processamento
    """
    print("\n" + "=" * 60)
    print("📊 RELATÓRIO DE GASTOS POR CATEGORIA")
    print("=" * 60)
    
    # Agrupa por categoria
    gastos_por_categoria = {}
    total_geral = 0.0
    
    for resultado in resultados:
        categoria = resultado.get('categoria', 'Outros')
        valor = resultado.get('valor', 0.0)
        
        if categoria not in gastos_por_categoria:
            gastos_por_categoria[categoria] = 0.0
        
        gastos_por_categoria[categoria] += valor
        total_geral += valor
    
    print(f"💰 TOTAL GERAL: R$ {total_geral:.2f}")
    
    if total_geral > 0:
        print(f"\n📈 GASTOS POR CATEGORIA:")
        print("-" * 40)
        
        # Ordena por valor decrescente
        categorias_ordenadas = sorted(gastos_por_categoria.items(), key=lambda x: x[1], reverse=True)
        
        for categoria, valor in categorias_ordenadas:
            if valor > 0:
                percentual = (valor / total_geral) * 100
                print(f"{categoria:<20} R$ {valor:>8.2f} ({percentual:>5.1f}%)")
                
                # Gráfico de barras simples
                barras = int(percentual / 3.33)  # Máximo 30 caracteres
                print(f"{'':20} {'█' * barras}")
    
    print("=" * 60)


def salvar_relatorio_detalhado(resultados, nome_arquivo="relatorio_fiscal.txt"):
    """
    Salva relatório detalhado em arquivo.
    
    Args:
        resultados: Lista de resultados do processamento
        nome_arquivo: Nome do arquivo para salvar
    """
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            f.write("RELATÓRIO FISCAL DETALHADO\n")
            f.write("=" * 50 + "\n\n")
            
            total_geral = sum(r.get('valor', 0.0) for r in resultados)
            f.write(f"TOTAL GERAL: R$ {total_geral:.2f}\n")
            f.write(f"TOTAL DE CANHOTOS: {len(resultados)}\n\n")
            
            # Detalhes por canhoto
            f.write("DETALHES POR CANHOTO:\n")
            f.write("-" * 50 + "\n")
            
            for i, resultado in enumerate(resultados, 1):
                f.write(f"\n{i}. {resultado['arquivo']}\n")
                f.write(f"   CNPJ: {resultado.get('cnpj', 'Não encontrado')}\n")
                f.write(f"   Empresa: {resultado.get('empresa', 'N/A')}\n")
                f.write(f"   Valor: R$ {resultado.get('valor', 0.0):.2f}\n")
                f.write(f"   Categoria: {resultado.get('categoria', 'N/A')}\n")
                f.write(f"   Atividade: {resultado.get('atividade', 'N/A')}\n")
            
            # Resumo por categoria
            gastos_por_categoria = {}
            for resultado in resultados:
                categoria = resultado.get('categoria', 'Outros')
                valor = resultado.get('valor', 0.0)
                gastos_por_categoria[categoria] = gastos_por_categoria.get(categoria, 0.0) + valor
            
            f.write(f"\n\nRESUMO POR CATEGORIA:\n")
            f.write("-" * 50 + "\n")
            
            for categoria, valor in sorted(gastos_por_categoria.items(), key=lambda x: x[1], reverse=True):
                if valor > 0:
                    percentual = (valor / total_geral) * 100 if total_geral > 0 else 0
                    f.write(f"{categoria}: R$ {valor:.2f} ({percentual:.1f}%)\n")
        
        print(f"📄 Relatório detalhado salvo em: {nome_arquivo}")
        
    except Exception as e:
        print(f"❌ Erro ao salvar relatório: {str(e)}")


def main():
    """Função principal da aplicação."""
    print("🧾 ANALISADOR FISCAL OCR - AWS TEXTRACT")
    print("Análise automática de canhotos de maquininha")
    print("=" * 60)
    
    # Verifica se AWS CLI está configurado
    try:
        import boto3
        # Testa credenciais AWS
        sts = boto3.client('sts')
        sts.get_caller_identity()
        print("✅ Credenciais AWS configuradas")
    except Exception as e:
        print("❌ Erro nas credenciais AWS!")
        print("💡 Configure com: aws configure")
        print(f"   Erro: {str(e)}")
        return
    
    # Encontra imagens
    imagens = encontrar_imagens_canhotos()
    
    if not imagens:
        return
    
    # Pergunta sobre região AWS
    print(f"\n🌍 Região AWS atual: us-east-1")
    usar_outra = input("Deseja usar outra região? (s/N): ").strip().lower()
    
    region_name = 'us-east-1'
    if usar_outra == 's':
        region_name = input("Digite a região (ex: us-west-2, eu-west-1): ").strip()
        if not region_name:
            region_name = 'us-east-1'
    
    # Processa canhotos
    resultados = processar_canhotos(imagens, region_name)
    
    # Gera relatório
    gerar_relatorio(resultados)
    
    # Salva relatório detalhado
    salvar_relatorio_detalhado(resultados)
    
    print(f"\n✅ Processamento concluído!")
    print(f"📊 {len(resultados)} canhotos processados")
    print(f"💰 Total de gastos: R$ {sum(r.get('valor', 0.0) for r in resultados):.2f}")


if __name__ == "__main__":
    main()
