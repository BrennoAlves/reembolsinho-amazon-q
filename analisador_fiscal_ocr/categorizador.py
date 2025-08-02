"""
Módulo para categorização de despesas baseado na descrição do CNAE.
"""

import requests


def consultar_cnpj_brasilapi(cnpj):
    """
    Consulta informações de um CNPJ na BrasilAPI.
    
    Args:
        cnpj (str): CNPJ com 14 dígitos (apenas números)
        
    Returns:
        dict: Informações da empresa ou None se não encontrado
    """
    try:
        url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"  ⚠️  CNPJ {cnpj} não encontrado na BrasilAPI")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Erro ao consultar CNPJ {cnpj}: {str(e)}")
        return None


def categorizar_por_cnae(descricao_cnae):
    """
    Categoriza uma despesa baseada na descrição do CNAE.
    
    Args:
        descricao_cnae (str): Descrição da atividade econômica
        
    Returns:
        str: Categoria da despesa
    """
    if not descricao_cnae:
        return "Outros"
    
    descricao_lower = descricao_cnae.lower()
    
    # Dicionário de categorização baseado em palavras-chave
    categorias = {
        "Alimentação": [
            "restaurante", "lanchonete", "padaria", "confeitaria", "pizzaria",
            "hamburgueria", "sorveteria", "açaí", "comida", "alimento",
            "bebida", "bar", "pub", "cervejaria", "cafeteria", "café",
            "pastelaria", "doceria", "panificação", "mercearia", "supermercado",
            "hipermercado", "minimercado", "empório", "delicatessen"
        ],
        
        "Transporte": [
            "taxi", "uber", "transporte", "combustível", "gasolina", "etanol",
            "diesel", "posto", "estacionamento", "pedágio", "ônibus",
            "metrô", "trem", "avião", "passagem", "locação de veículos",
            "aluguel de carros", "moto", "bicicleta"
        ],
        
        "Hospedagem": [
            "hotel", "pousada", "hostel", "motel", "resort", "hospedagem",
            "alojamento", "pensão", "apart-hotel", "flat"
        ],
        
        "Saúde": [
            "farmácia", "drogaria", "medicamento", "hospital", "clínica",
            "consultório", "médico", "dentista", "laboratório", "exame",
            "fisioterapia", "psicologia", "veterinário", "ótica", "óculos"
        ],
        
        "Educação": [
            "escola", "universidade", "faculdade", "curso", "treinamento",
            "educação", "ensino", "livraria", "papelaria", "material escolar",
            "biblioteca", "seminário", "workshop"
        ],
        
        "Tecnologia": [
            "informática", "computador", "software", "hardware", "eletrônico",
            "celular", "smartphone", "tablet", "notebook", "impressora",
            "internet", "telecomunicações", "telefonia", "dados"
        ],
        
        "Vestuário": [
            "roupa", "vestuário", "calçado", "sapato", "tênis", "sandália",
            "confecção", "moda", "boutique", "loja de roupas", "alfaiataria",
            "sapataria", "acessórios"
        ],
        
        "Serviços": [
            "consultoria", "advocacia", "contabilidade", "auditoria",
            "engenharia", "arquitetura", "design", "publicidade", "marketing",
            "limpeza", "segurança", "manutenção", "reparo", "instalação"
        ],
        
        "Entretenimento": [
            "cinema", "teatro", "show", "evento", "festa", "entretenimento",
            "diversão", "parque", "museu", "exposição", "jogo", "esporte",
            "academia", "ginástica", "clube", "recreação"
        ],
        
        "Material de Escritório": [
            "papelaria", "escritório", "material de escritório", "impressão",
            "gráfica", "fotocópia", "encadernação", "papel", "caneta",
            "arquivo", "pasta", "organizador"
        ]
    }
    
    # Verifica cada categoria
    for categoria, palavras_chave in categorias.items():
        for palavra in palavras_chave:
            if palavra in descricao_lower:
                return categoria
    
    return "Outros"


def processar_cnpj_e_categorizar(cnpj):
    """
    Consulta um CNPJ na BrasilAPI e retorna a categoria da despesa.
    
    Args:
        cnpj (str): CNPJ com 14 dígitos
        
    Returns:
        tuple: (categoria, nome_empresa, descricao_cnae)
    """
    if not cnpj:
        return "Outros", "Empresa não identificada", "CNAE não disponível"
    
    print(f"  🔍 Consultando CNPJ: {cnpj}")
    
    dados_empresa = consultar_cnpj_brasilapi(cnpj)
    
    if not dados_empresa:
        return "Outros", "Empresa não encontrada", "CNAE não disponível"
    
    nome_empresa = dados_empresa.get('razao_social', 'Nome não disponível')
    descricao_cnae = dados_empresa.get('cnae_fiscal_descricao', '')
    
    categoria = categorizar_por_cnae(descricao_cnae)
    
    print(f"  🏢 Empresa: {nome_empresa}")
    print(f"  📋 CNAE: {descricao_cnae}")
    print(f"  🏷️  Categoria: {categoria}")
    
    return categoria, nome_empresa, descricao_cnae


class CategorizadorDespesas:
    """Classe para categorização de despesas baseada em CNPJ e CNAE."""
    
    def __init__(self):
        """Inicializa o categorizador."""
        pass
    
    def consultar_cnpj(self, cnpj):
        """
        Consulta informações de um CNPJ na BrasilAPI.
        
        Args:
            cnpj: CNPJ com 14 dígitos
            
        Returns:
            Dicionário com informações da empresa ou None
        """
        dados = consultar_cnpj_brasilapi(cnpj)
        if dados:
            return {
                'nome': dados.get('razao_social', 'Nome não disponível'),
                'atividade_principal': dados.get('cnae_fiscal_descricao', ''),
                'cnae_codigo': dados.get('cnae_fiscal', '')
            }
        return None
    
    def categorizar_despesa(self, cnae_codigo):
        """
        Categoriza uma despesa baseada no código CNAE.
        
        Args:
            cnae_codigo: Código CNAE da empresa
            
        Returns:
            Categoria da despesa
        """
        # Busca a descrição do CNAE para categorizar
        # Em uma implementação mais robusta, teríamos um mapeamento código->descrição
        # Por enquanto, retornamos "Outros" e deixamos a categorização para o main.py
        return "Outros"


def gerar_relatorio_categorias(gastos_por_categoria):
    """
    Gera um relatório visual das categorias de gastos.
    
    Args:
        gastos_por_categoria (dict): Dicionário com categoria: valor
        
    Returns:
        str: Relatório formatado
    """
    if not gastos_por_categoria:
        return "Nenhum gasto categorizado encontrado."
    
    total_geral = sum(gastos_por_categoria.values())
    
    # Ordena categorias por valor (maior para menor)
    categorias_ordenadas = sorted(
        gastos_por_categoria.items(), 
        key=lambda x: x[1], 
        reverse=True
    )
    
    relatorio = []
    relatorio.append("=" * 60)
    relatorio.append("📊 RELATÓRIO DE GASTOS POR CATEGORIA")
    relatorio.append("=" * 60)
    relatorio.append(f"💰 TOTAL GERAL: R$ {total_geral:.2f}")
    relatorio.append("")
    relatorio.append("📈 GASTOS POR CATEGORIA:")
    relatorio.append("-" * 40)
    
    # Calcula a largura máxima para o gráfico
    valor_maximo = max(gastos_por_categoria.values()) if gastos_por_categoria else 1
    largura_maxima = 30
    
    for categoria, valor in categorias_ordenadas:
        percentual = (valor / total_geral) * 100
        
        # Calcula o tamanho da barra
        tamanho_barra = int((valor / valor_maximo) * largura_maxima)
        barra = "█" * tamanho_barra
        
        relatorio.append(f"{categoria:<20} R$ {valor:>8.2f} ({percentual:>5.1f}%)")
        relatorio.append(f"{'':20} {barra}")
        relatorio.append("")
    
    relatorio.append("=" * 60)
    
    return "\n".join(relatorio)
