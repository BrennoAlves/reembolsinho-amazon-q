# 🧾 Analisador Fiscal OCR - AWS Textract

Uma aplicação de linha de comando em Python que automatiza a análise de canhotos de maquininha de cartão usando **AWS Textract**, extraindo dados fiscais, categorizando despesas e gerando relatórios detalhados.

## 📋 Descrição

O **Analisador Fiscal OCR** utiliza o serviço AWS Textract para:

- Extrair texto de imagens de canhotos de maquininha com alta precisão
- Identificar CNPJs e valores das transações
- Consultar informações das empresas na BrasilAPI
- Categorizar automaticamente as despesas por tipo de atividade
- Gerar relatórios visuais com gráficos de barras em texto

## 🚀 Funcionalidades

- ✅ **AWS Textract**: OCR em nuvem com alta precisão e confiabilidade
- ✅ **Extração Inteligente**: Identifica CNPJs e valores usando expressões regulares otimizadas
- ✅ **Consulta Automática**: Integração com BrasilAPI para dados empresariais
- ✅ **Categorização Automática**: Classifica despesas baseado no CNAE
- ✅ **Relatórios Visuais**: Gráficos de barras em ASCII no terminal
- ✅ **Exportação**: Salva relatórios detalhados em arquivo texto
- ✅ **Suporte Múltiplos Formatos**: JPG, PNG, BMP, TIFF
- ✅ **Escalabilidade**: Processa grandes volumes usando infraestrutura AWS

## 📦 Instalação

### 1. Configuração AWS

#### Instalar AWS CLI
```bash
# Linux/macOS
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Windows
# Baixe e instale de: https://aws.amazon.com/cli/
```

#### Configurar Credenciais
```bash
aws configure
```

Você precisará fornecer:
- **Access Key ID**: Sua chave de acesso AWS
- **Secret Access Key**: Sua chave secreta AWS
- **Default region**: Região AWS (ex: us-east-1, sa-east-1)
- **Default output format**: json

#### Permissões Necessárias
Sua conta AWS precisa ter permissão para usar o **Amazon Textract**. Certifique-se de que sua política IAM inclui:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "textract:DetectDocumentText"
            ],
            "Resource": "*"
        }
    ]
}
```

### 2. Dependências Python

```bash
# Clone ou baixe o projeto
cd analisador-fiscal-ocr

# Instale as dependências Python
pip install -r requirements.txt
```

### 3. Verificação da Instalação

Para verificar se tudo está configurado:

```bash
# Teste AWS CLI
aws sts get-caller-identity

# Teste AWS Textract (opcional)
aws textract help
```

## 📁 Estrutura do Projeto

```
analisador-fiscal-ocr/
├── analisador_fiscal_ocr/
│   ├── main.py              # Lógica principal da aplicação
│   ├── ocr_aws.py           # Integração com AWS Textract
│   └── categorizador.py     # Categorização e consulta de CNPJs
├── canhotos/                # Pasta para as imagens dos canhotos
├── requirements.txt         # Dependências Python
└── README.md               # Esta documentação
```

## 🖥️ Como Usar

### 1. Preparar as Imagens

1. Crie a pasta `canhotos` na raiz do projeto (se não existir)
2. Adicione as imagens dos canhotos de maquininha na pasta `canhotos/`
3. Formatos suportados: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`, `.tif`

### 2. Executar a Aplicação

```bash
python analisador_fiscal_ocr/main.py
```

### 3. Exemplo de Saída

```
🧾 ANALISADOR FISCAL OCR - AWS TEXTRACT
Análise automática de canhotos de maquininha
============================================================

✅ Credenciais AWS configuradas
🌍 Região AWS atual: us-east-1
Deseja usar outra região? (s/N): n

🔍 Encontradas 3 imagens para processar
============================================================

📸 [1/3] Processando imagem...
🔍 Processando: canhoto_restaurante.jpg
  📄 CNPJ: 12345678000195
  💰 Valor: R$ 45.90
  🔍 Consultando CNPJ: 12345678000195
  🏢 Empresa: RESTAURANTE EXEMPLO LTDA
  📋 CNAE: Restaurantes e similares
  🏷️  Categoria: Alimentação
  ✅ Processado com sucesso!

============================================================
📊 RELATÓRIO DE GASTOS POR CATEGORIA
============================================================
💰 TOTAL GERAL: R$ 123.45

📈 GASTOS POR CATEGORIA:
----------------------------------------
Alimentação          R$    78.90 ( 63.9%)
                     ██████████████████████████████

Transporte           R$    44.55 ( 36.1%)
                     ████████████████████

============================================================
📄 Relatório detalhado salvo em: relatorio_fiscal.txt
✅ Processamento concluído!
```

## ⚙️ Configurações

### Regiões AWS Recomendadas

- **sa-east-1** (São Paulo): Melhor latência para Brasil
- **us-east-1** (N. Virginia): Região padrão, mais barata
- **us-west-2** (Oregon): Alternativa com boa performance

### Custos AWS Textract

O AWS Textract cobra por página processada:
- **Primeiras 1 milhão de páginas/mês**: $1.50 por 1.000 páginas
- **Acima de 1 milhão**: $0.60 por 1.000 páginas

Para canhotos típicos, o custo é aproximadamente **$0.0015 por canhoto**.

## 🎯 Categorias de Despesas

O sistema categoriza automaticamente as despesas baseado no CNAE da empresa:

- **Alimentação**: Restaurantes, lanchonetes, supermercados, bares
- **Transporte**: Postos de combustível, estacionamentos, transportes
- **Hospedagem**: Hotéis, pousadas, apart-hotéis
- **Saúde**: Farmácias, clínicas, laboratórios
- **Educação**: Escolas, cursos, livrarias
- **Tecnologia**: Informática, eletrônicos, telecomunicações
- **Vestuário**: Roupas, calçados, acessórios
- **Serviços**: Consultorias, advocacia, manutenção
- **Entretenimento**: Cinemas, eventos, academias
- **Material de Escritório**: Papelarias, gráficas
- **Outros**: Categorias não identificadas

## 🔧 Vantagens do AWS Textract

### Sobre OCR Local

- **✅ Maior Precisão**: Algoritmos de ML treinados em milhões de documentos
- **✅ Sem Instalação**: Não precisa instalar Tesseract ou outras dependências
- **✅ Escalabilidade**: Processa milhares de documentos simultaneamente
- **✅ Manutenção Zero**: AWS cuida da infraestrutura e atualizações
- **✅ Suporte Nativo**: Otimizado para documentos fiscais e comerciais

### Limitações

- **💰 Custo**: Cobra por uso (mas muito baixo para volumes pequenos)
- **🌐 Internet**: Requer conexão com internet
- **🔐 Dados**: Imagens são enviadas para AWS (criptografadas)

## 🔒 Segurança

- Todas as comunicações são criptografadas (HTTPS/TLS)
- AWS não armazena suas imagens após o processamento
- Credenciais AWS ficam apenas no seu computador
- Dados empresariais consultados via BrasilAPI (pública)

## 🆘 Troubleshooting

**Erro: "Credenciais AWS não configuradas"**
- Execute: `aws configure`
- Verifique se tem Access Key e Secret Key válidos

**Erro: "AccessDenied"**
- Verifique se sua conta tem permissão para Textract
- Confirme se a região está correta

**Erro: "CNPJ não encontrado"**
- AWS Textract tem alta precisão, mas alguns canhotos podem não ter CNPJ visível
- Verifique se a imagem está legível

**Erro: "Valor não encontrado"**
- Confirme se o valor total está claramente visível na imagem
- Alguns formatos de canhoto podem ter layouts diferentes

## 💰 Estimativa de Custos

Para uso típico de pequenas empresas:
- **100 canhotos/mês**: ~$0.15/mês
- **500 canhotos/mês**: ~$0.75/mês
- **1000 canhotos/mês**: ~$1.50/mês

## 🤝 Contribuição

Este projeto foi desenvolvido como parte de um desafio da AWS. Contribuições são bem-vindas!

## 📄 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

---

**Desenvolvido com ❤️ e AWS Textract para automatizar a análise fiscal de pequenas empresas e profissionais autônomos.**
