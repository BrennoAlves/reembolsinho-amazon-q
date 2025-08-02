#!/usr/bin/env python3
"""
Script de teste simples para verificar se AWS Textract está funcionando.
"""

import os
from pathlib import Path
from analisador_fiscal_ocr.ocr_aws import extrair_dados_canhoto_aws

def main():
    print("🧪 TESTE SIMPLES - AWS TEXTRACT")
    print("=" * 50)
    
    # Verifica se há imagens na pasta canhotos
    pasta_canhotos = Path("canhotos")
    if not pasta_canhotos.exists():
        print("❌ Pasta 'canhotos' não encontrada!")
        return
    
    # Busca primeira imagem
    extensoes = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']
    imagem = None
    
    for ext in extensoes:
        imagens = list(pasta_canhotos.glob(f"*{ext}"))
        if imagens:
            imagem = imagens[0]
            break
    
    if not imagem:
        print("❌ Nenhuma imagem encontrada na pasta 'canhotos'!")
        return
    
    print(f"📸 Testando com: {imagem.name}")
    print("-" * 50)
    
    try:
        # Testa extração
        resultado = extrair_dados_canhoto_aws(str(imagem))
        
        print(f"✅ Teste concluído!")
        print(f"📄 CNPJ: {resultado['cnpj'] or 'Não encontrado'}")
        print(f"💰 Valor: R$ {resultado['valor']:.2f}")
        print(f"📝 Texto extraído: {len(resultado['texto_completo'])} caracteres")
        
        if resultado['texto_completo']:
            print(f"📋 Primeiras linhas do texto:")
            linhas = resultado['texto_completo'].split('\n')[:5]
            for linha in linhas:
                if linha.strip():
                    print(f"   {linha.strip()}")
        
    except Exception as e:
        print(f"❌ Erro no teste: {str(e)}")
        if "credentials" in str(e).lower():
            print("💡 Configure suas credenciais AWS com: aws configure")

if __name__ == "__main__":
    main()
