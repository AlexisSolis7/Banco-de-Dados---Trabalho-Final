"""
Configurações centralizadas para o projeto de análise de banco de dados.
Este arquivo centraliza todos os paths e configurações do sistema.
"""

import os

# Diretório base do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Diretórios principais
SQL_DIR = os.path.join(BASE_DIR, 'sql')
RESULTADOS_DIR = os.path.join(BASE_DIR, 'resultados')
GRAFICOS_DIR = os.path.join(RESULTADOS_DIR, 'graficos')
RELATORIOS_DIR = os.path.join(RESULTADOS_DIR, 'relatorios')
TESTES_DIR = os.path.join(BASE_DIR, 'testes')

# Arquivos específicos
SQL_CRIACAO_DADOS = os.path.join(SQL_DIR, 'CriandoInserindoDados.sql')

# Configurações de gráficos
GRAFICOS_CONFIG = {
    'dpi': 300,
    'format': 'png',
    'bbox_inches': 'tight',
    'facecolor': 'white'
}

# Nomes padrão dos arquivos de gráficos
NOMES_GRAFICOS = {
    'alunos_escola': 'grafico_alunos_escola.png',
    'faixa_precipitacao': 'grafico_faixa_precipitacao_total_coletas.png',
    'media_chuva': 'grafico_media_chuva.png',
    'nome_completo_aluno': 'grafico_nome_completo_aluno_id_aluno.png',
    'scatter_aluno_escola': 'grafico_scatter_id_aluno_id_escola.png',
    'scatter_coletas_chuva': 'grafico_scatter_total_coletas_media_chuva.png',
    'scatter_coletas_faixa': 'grafico_scatter_total_coletas_media_na_faixa.png',
    'status_validacao': 'grafico_status_validacao_total_coletas.png',
    'total_coletas': 'grafico_total_coletas.png'
}

# Nomes padrão dos arquivos de relatórios
NOMES_RELATORIOS = {
    'analise_status': 'resultado_análise_por_status.csv',
    'consulta_personalizada': 'resultado_consulta_personalizada.csv',
    'distribuicao_chuva': 'resultado_distribuição_de_chuva.csv',
    'estatisticas_escola': 'resultado_estatísticas_por_escola.csv',
    'ranking_participacao': 'resultado_ranking_de_participação.csv'
}

def criar_diretorios():
    """
    Cria todos os diretórios necessários se não existirem.
    """
    diretorios = [
        SQL_DIR,
        RESULTADOS_DIR,
        GRAFICOS_DIR,
        RELATORIOS_DIR,
        TESTES_DIR
    ]
    
    for diretorio in diretorios:
        os.makedirs(diretorio, exist_ok=True)
        print(f"Diretório verificado/criado: {diretorio}")

def get_path_grafico(nome_grafico):
    """
    Retorna o path completo para um gráfico específico.
    
    Args:
        nome_grafico (str): Nome do gráfico conforme definido em NOMES_GRAFICOS
        
    Returns:
        str: Path completo para o arquivo do gráfico
    """
    if nome_grafico in NOMES_GRAFICOS:
        return os.path.join(GRAFICOS_DIR, NOMES_GRAFICOS[nome_grafico])
    else:
        return os.path.join(GRAFICOS_DIR, f"{nome_grafico}.png")

def get_path_relatorio(nome_relatorio):
    """
    Retorna o path completo para um relatório específico.
    
    Args:
        nome_relatorio (str): Nome do relatório conforme definido em NOMES_RELATORIOS
        
    Returns:
        str: Path completo para o arquivo do relatório
    """
    if nome_relatorio in NOMES_RELATORIOS:
        return os.path.join(RELATORIOS_DIR, NOMES_RELATORIOS[nome_relatorio])
    else:
        return os.path.join(RELATORIOS_DIR, f"{nome_relatorio}.csv")

def verificar_estrutura():
    """
    Verifica se todos os diretórios necessários existem.
    
    Returns:
        bool: True se todos os diretórios existem, False caso contrário
    """
    diretorios = [SQL_DIR, RESULTADOS_DIR, GRAFICOS_DIR, RELATORIOS_DIR, TESTES_DIR]
    
    for diretorio in diretorios:
        if not os.path.exists(diretorio):
            print(f"Diretório não encontrado: {diretorio}")
            return False
    
    print("Estrutura de diretórios verificada com sucesso!")
    return True

def listar_arquivos_resultados():
    """
    Lista todos os arquivos de resultados (gráficos e relatórios) existentes.
    """
    print("\n=== ARQUIVOS DE RESULTADOS ===")
    
    print("\nGráficos:")
    if os.path.exists(GRAFICOS_DIR):
        graficos = [f for f in os.listdir(GRAFICOS_DIR) if f.endswith('.png')]
        for grafico in sorted(graficos):
            print(f"  - {grafico}")
    else:
        print("  Diretório de gráficos não encontrado")
    
    print("\nRelatórios:")
    if os.path.exists(RELATORIOS_DIR):
        relatorios = [f for f in os.listdir(RELATORIOS_DIR) if f.endswith('.csv')]
        for relatorio in sorted(relatorios):
            print(f"  - {relatorio}")
    else:
        print("  Diretório de relatórios não encontrado")

if __name__ == "__main__":
    print("=== CONFIGURAÇÃO DO PROJETO ===")
    print(f"Diretório base: {BASE_DIR}")
    print(f"Diretório SQL: {SQL_DIR}")
    print(f"Diretório resultados: {RESULTADOS_DIR}")
    print(f"Diretório gráficos: {GRAFICOS_DIR}")
    print(f"Diretório relatórios: {RELATORIOS_DIR}")
    print(f"Diretório testes: {TESTES_DIR}")
    
    print("\n=== VERIFICANDO ESTRUTURA ===")
    verificar_estrutura()
    
    print("\n=== CRIANDO DIRETÓRIOS NECESSÁRIOS ===")
    criar_diretorios()
    
    listar_arquivos_resultados()
