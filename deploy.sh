#!/bin/bash

# Script de Deploy para GitHub
# Uso: ./deploy.sh "mensagem do commit"

echo "🚀 DEPLOY PARA GITHUB"
echo "====================="

# Verifica se foi passada uma mensagem de commit
if [ -z "$1" ]; then
    echo "❌ Erro: Forneça uma mensagem de commit"
    echo "💡 Uso: ./deploy.sh \"sua mensagem aqui\""
    exit 1
fi

# Adiciona todos os arquivos
echo "📦 Adicionando arquivos..."
git add .

# Verifica se há mudanças para commitar
if git diff --staged --quiet; then
    echo "ℹ️  Nenhuma mudança detectada para commit"
    exit 0
fi

# Faz o commit
echo "💾 Fazendo commit..."
git commit -m "$1"

# Faz o push
echo "🌐 Enviando para GitHub..."
git push origin main

echo "✅ Deploy concluído!"
echo "🔗 Verifique em: https://github.com/seu-usuario/analisador-fiscal-ocr"
