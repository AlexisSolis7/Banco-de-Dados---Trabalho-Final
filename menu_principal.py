# -*- coding: utf-8 -*-
"""
Menu Principal - Sistema SiCoPluE
Sistema de Consulta de Pluviometria Escolar
"""

import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import os
import sys
import json
import google.generativeai as genai
warnings.filterwarnings('ignore')

# Importar configurações centralizadas e funções do script de testes
import config
from testes.teste_query_personalizada import conectar_banco, gerar_graficos, DB_CONFIG

# Configurar API do Gemini
GEMINI_API_KEY = "AIzaSyA83Xy_avI2LjPBISqoBdhrMPdgyzNCNxU"
genai.configure(api_key=GEMINI_API_KEY)

def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    """Pausa para o usuário ler"""
    input("\nPressione Enter para continuar...")

def exibir_menu():
    """Exibe o menu principal"""
    print("="*60)
    print("           SISTEMA SiCoPluE - MENU PRINCIPAL")
    print("      Sistema de Consulta de Pluviometria Escolar")
    print("="*60)
    print("  1.  CRIAR TODAS AS TABELAS (CASO NAO ESTEJA FEITO)")
    print("  2.  INSERIR DADOS SIMPLES (SEM DEPENDÊNCIAS)") 
    print("  3.  CONSULTA - Estatísticas por Escola")
    print("  4.  CONSULTA - Ranking de Participação")
    print("  5.  CONSULTA - Top 10 Alunos Ativos")
    print("  6.  CONSULTA - Análise por Status")
    print("  7.  CONSULTA - Distribuição de Chuva")
    print("  8.  CONSULTA PERSONALIZADA")
    print("  9.  ANALISE DE OBSERVACAO COM IA")
    print(" 10.  LISTAR TODAS AS TABELAS")
    print(" 11.  VERIFICAR DADOS DAS TABELAS")
    print(" 12.  ATUALIZAR DADOS")
    print(" 13.  LIMPAR TODOS OS DADOS")
    print("  0.  SAIR DO SISTEMA")
    print("="*60)

def executar_sql(query, descricao, mostrar_resultado=True):
    """Executa uma query SQL"""
    conn = conectar_banco()
    if not conn:
        return None
    
    try:
        print(f"\nExecutando: {descricao}")
        
        if mostrar_resultado:
            df = pd.read_sql_query(query, conn)
            print("\nRESULTADOS:")
            print("-" * 50)
            if not df.empty:
                print(df.to_string(index=False))
                
                # Salvar CSV
                arquivo_csv = config.get_path_relatorio(descricao.lower().replace(' ', '_'))
                df.to_csv(arquivo_csv, index=False)
                print(f"\nResultado salvo em: {arquivo_csv}")
                
                # Gerar gráficos
                print("\nAnalisando dados para gráficos...")
                gerar_graficos(df)
            else:
                print("Nenhum resultado encontrado.")
            return df
        else:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            print(f"{descricao} executada com sucesso!")
            cursor.close()
            return True
            
    except Exception as e:
        print(f"Erro: {e}")
        return None
    finally:
        conn.close()

def executar_insercao(query, descricao):
    """Executa uma query de inserção SEM gerar gráficos"""
    conn = conectar_banco()
    if not conn:
        return False
    
    try:
        print(f"\nExecutando: {descricao}")
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        print(f"{descricao} executada com sucesso!")
        cursor.close()
        return True
            
    except Exception as e:
        print(f"Erro: {e}")
        return False
    finally:
        conn.close()

def listar_dados(query, descricao):
    """Lista dados SEM gerar gráficos - apenas para consulta rápida"""
    conn = conectar_banco()
    if not conn:
        return None
    
    try:
        print(f"\n{descricao}:")
        df = pd.read_sql_query(query, conn)
        if not df.empty:
            print(df.to_string(index=False))
        else:
            print("Nenhum resultado encontrado.")
        return df
            
    except Exception as e:
        print(f"Erro: {e}")
        return None
    finally:
        conn.close()

def criar_tabelas():
    """Opção 1: Criar todas as tabelas"""
    print("\nCRIANDO ESTRUTURA DO BANCO DE DADOS")
    print("-" * 50)
    
    # Ler e executar o script SQL
    try:
        with open(config.SQL_CRIACAO_DADOS, 'r', encoding='utf-8') as file:
            sql_script = file.read()
        
        conn = conectar_banco()
        if conn:
            cursor = conn.cursor()
            cursor.execute(sql_script)
            conn.commit()
            cursor.close()
            conn.close()
            print("Todas as tabelas foram criadas e populadas com sucesso!")
        else:
            print("Erro na conexão com o banco.")
            
    except FileNotFoundError:
        print(f"Arquivo '{config.SQL_CRIACAO_DADOS}' não encontrado!")
    except Exception as e:
        print(f"Erro: {e}")

def inserir_dados_exemplo():
    """Opção 2: Inserir dados simples (independentes)"""
    print("\nINSERIR DADOS SIMPLES")
    print("=" * 60)
    print("Insira apenas os dados que você quer, sem dependências!")
    print("=" * 60)
    
    print("\n1. ESCOLHA O QUE INSERIR:")
    print("-" * 50)
    print("A. Inserir CIDADE (independente)")
    print("B. Inserir dados de EXEMPLO completos (automático)")
    print("C. Inserir ALUNO (em escola existente)")
    print("D. Inserir COLETA (de aluno existente)")
    
    while True:
        escolha = input("\nDigite A, B, C ou D: ").upper().strip()
        if escolha in ['A', 'B', 'C', 'D']:
            break
        print("Digite apenas A, B, C ou D!")
    
    if escolha == 'A':
        # Inserir apenas cidade
        print("\nINSERINDO CIDADE:")
        print("-" * 30)
        nome_cidade = input("Nome da cidade: ").strip()
        uf = input("UF (ex: SP, RJ): ").strip().upper()
        
        if nome_cidade and uf:
            query = f"INSERT INTO Cidade (nome_cidade, uf) VALUES ('{nome_cidade}', '{uf}') ON CONFLICT (nome_cidade) DO NOTHING;"
            executar_insercao(query, "Inserção de Cidade")
        else:
            print("Dados incompletos!")
            
    elif escolha == 'B':
        # Inserção automática completa (como antes)
        print("\nINSERINDO DADOS COMPLETOS DE EXEMPLO:")
        print("-" * 50)
        
        queries = [
            "INSERT INTO Cidade (nome_cidade, uf) VALUES ('São Paulo', 'SP') ON CONFLICT (nome_cidade) DO NOTHING;",
            "INSERT INTO Bairro (nome_bairro, id_cidade) VALUES ('Centro', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'São Paulo'));",
            "INSERT INTO Escola (nome_escola, endereco_completo, id_bairro) VALUES ('Escola Municipal João da Silva', 'Rua das Flores, 456', (SELECT id_bairro FROM Bairro WHERE nome_bairro = 'Centro')) ON CONFLICT (nome_escola) DO NOTHING;",
            "INSERT INTO Pluviometro (latitude, longitude, id_escola) VALUES (-23.5505, -46.6333, (SELECT id_escola FROM Escola WHERE nome_escola = 'Escola Municipal João da Silva'));",
            "INSERT INTO Aluno (nome_completo_aluno, email_aluno, senha_aluno, turma_aluno, id_escola) VALUES ('Maria Santos', 'maria@escola.com', 'senha123', '9A', (SELECT id_escola FROM Escola WHERE nome_escola = 'Escola Municipal João da Silva')) ON CONFLICT (email_aluno) DO NOTHING;",
            "INSERT INTO ColetaPluviometrica (data_hora_coleta, valor_medido_mm, observacoes_aluno, id_pluviometro, id_aluno_coleta, status_validacao) VALUES (NOW(), 15.7, 'Chuva muito forte com granizo e vento, vi alguns alagamentos começando na rua da frente.', (SELECT id_pluviometro FROM Pluviometro WHERE id_escola = (SELECT id_escola FROM Escola WHERE nome_escola = 'Escola Municipal João da Silva')), (SELECT id_aluno FROM Aluno WHERE email_aluno = 'maria@escola.com'), 'aprovado');"
        ]
        
        for i, query in enumerate(queries, 1):
            executar_insercao(query, f"Exemplo {i}/6")
        print("\nTodos os dados de exemplo inseridos!")
        
    elif escolha == 'C':
        # Inserir aluno em escola existente
        print("\nINSERINDO ALUNO:")
        print("-" * 30)
        
        # Mostrar escolas disponíveis
        print("Escolas disponíveis:")
        query_escolas = "SELECT id_escola, nome_escola FROM Escola ORDER BY nome_escola;"
        listar_dados(query_escolas, "Escolas Disponíveis")
        
        id_escola = input("\nDigite o ID da escola: ").strip()
        nome_aluno = input("Nome completo do aluno: ").strip()
        email_aluno = input("Email do aluno: ").strip()
        senha_aluno = input("Senha do aluno: ").strip()
        turma_aluno = input("Turma (opcional): ").strip()
        
        if id_escola and nome_aluno and email_aluno and senha_aluno:
            turma_sql = f"'{turma_aluno}'" if turma_aluno else "NULL"
            query = f"INSERT INTO Aluno (nome_completo_aluno, email_aluno, senha_aluno, turma_aluno, id_escola) VALUES ('{nome_aluno}', '{email_aluno}', '{senha_aluno}', {turma_sql}, {id_escola});"
            executar_insercao(query, "Inserção de Aluno")
        else:
            print("Dados obrigatórios não fornecidos!")
            
    elif escolha == 'D':
        # Inserir coleta de aluno existente
        print("\nINSERINDO COLETA:")
        print("-" * 30)
        
        # Mostrar alunos disponíveis
        print("Alunos disponíveis:")
        query_alunos = "SELECT id_aluno, nome_completo_aluno FROM Aluno ORDER BY nome_completo_aluno;"
        listar_dados(query_alunos, "Alunos Disponíveis")
        
        id_aluno = input("\nDigite o ID do aluno: ").strip()
        valor_chuva = input("Valor da chuva (mm): ").strip()
        observacoes = input("Observações do aluno (opcional): ").strip()
        status = input("Status (pendente/aprovado/rejeitado): ").strip().lower()
        
        if id_aluno and valor_chuva:
            if status not in ['pendente', 'aprovado', 'rejeitado']:
                status = 'pendente'
            
            observacoes_sql = f"'{observacoes}'" if observacoes else "NULL"
            query = f"""
            INSERT INTO ColetaPluviometrica 
            (data_hora_coleta, valor_medido_mm, observacoes_aluno, id_pluviometro, id_aluno_coleta, status_validacao) 
            VALUES 
            (NOW(), {valor_chuva}, {observacoes_sql}, 
             (SELECT p.id_pluviometro FROM Pluviometro p JOIN Aluno a ON a.id_escola = p.id_escola WHERE a.id_aluno = {id_aluno} LIMIT 1), 
             {id_aluno}, '{status}');
            """
            executar_insercao(query, "Inserção de Coleta")
        else:
            print("Dados obrigatórios não fornecidos!")
    
    print("\n2. DICAS:")
    print("-" * 50)
    print("- Use opção A para criar cidades independentemente")
    print("- Use opção B para dados completos de teste")
    print("- Use opção C para adicionar alunos a escolas existentes")
    print("- Use opção D para adicionar coletas de alunos existentes")
    print("- Use OPÇÃO 8 (Consulta Personalizada) para inserções mais complexas")

def consulta_estatisticas_escola():
    """Opção 3: Estatísticas completas por escola"""
    query = """
    SELECT 
        e.nome_escola,
        COUNT(DISTINCT a.id_aluno) as total_alunos,
        COUNT(c.id_coleta) as total_coletas,
        ROUND(AVG(c.valor_medido_mm), 2) as media_chuva
    FROM 
        Escola e
        LEFT JOIN Aluno a ON a.id_escola = e.id_escola
        LEFT JOIN ColetaPluviometrica c ON c.id_aluno_coleta = a.id_aluno
    WHERE 
        c.status_validacao = 'aprovado'
    GROUP BY 
        e.id_escola, e.nome_escola
    ORDER BY 
        total_coletas DESC;
    """
    executar_sql(query, "Estatísticas por Escola")

def consulta_ranking_participacao():
    """Opção 4: Ranking de participação"""
    query = """
    SELECT 
        e.nome_escola,
        COUNT(c.id_coleta) as total_coletas
    FROM 
        Escola e
        LEFT JOIN Aluno a ON a.id_escola = e.id_escola
        LEFT JOIN ColetaPluviometrica c ON c.id_aluno_coleta = a.id_aluno
    GROUP BY 
        e.id_escola, e.nome_escola
    ORDER BY 
        total_coletas DESC;
    """
    executar_sql(query, "Ranking de Participação")

def consulta_top_alunos():
    """Opção 5: Top 10 alunos mais ativos"""
    query = """
    SELECT 
        a.nome_completo_aluno,
        COUNT(c.id_coleta) as total_coletas
    FROM 
        Aluno a
        JOIN ColetaPluviometrica c ON c.id_aluno_coleta = a.id_aluno
    WHERE 
        c.status_validacao = 'aprovado'
    GROUP BY 
        a.id_aluno, a.nome_completo_aluno
    ORDER BY 
        total_coletas DESC
    LIMIT 10;
    """
    executar_sql(query, "Top 10 Alunos Ativos")

def consulta_status():
    """Opção 6: Análise por status de validação"""
    query = """
    SELECT 
        c.status_validacao,
        COUNT(c.id_coleta) as total_coletas,
        ROUND(AVG(c.valor_medido_mm), 2) as media_chuva
    FROM 
        ColetaPluviometrica c
    GROUP BY 
        c.status_validacao
    ORDER BY 
        total_coletas DESC;
    """
    executar_sql(query, "Análise por Status")

def consulta_distribuicao_chuva():
    """Opção 7: Distribuição de valores de chuva"""
    query = """
    SELECT 
        CASE 
            WHEN c.valor_medido_mm <= 10 THEN 'Baixa (0-10mm)'
            WHEN c.valor_medido_mm <= 30 THEN 'Média (11-30mm)'
            ELSE 'Alta (31mm+)'
        END as faixa_precipitacao,
        COUNT(c.id_coleta) as total_coletas,
        ROUND(AVG(c.valor_medido_mm), 2) as media_na_faixa
    FROM 
        ColetaPluviometrica c
    WHERE 
        c.status_validacao = 'aprovado'
    GROUP BY 
        CASE 
            WHEN c.valor_medido_mm <= 10 THEN 'Baixa (0-10mm)'
            WHEN c.valor_medido_mm <= 30 THEN 'Média (11-30mm)'
            ELSE 'Alta (31mm+)'
        END
    ORDER BY 
        total_coletas DESC;
    """
    executar_sql(query, "Distribuição de Chuva")

def consulta_personalizada():
    """Opção 8: Permite ao usuário escrever sua própria query"""
    print("\nCONSULTA PERSONALIZADA")
    print("-" * 50)
    print("Digite sua query SQL (termine com ';' e pressione Enter duas vezes):")
    
    lines = []
    while True:
        line = input()
        if line.strip() == '' and lines:
            break
        lines.append(line)
    
    query = '\n'.join(lines)
    
    if query.strip():
        executar_sql(query, "Consulta Personalizada")
    else:
        print("Query vazia!")

def listar_tabelas():
    """Opção 9: Lista todas as tabelas do banco"""
    query = """
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
    ORDER BY table_name;
    """
    listar_dados(query, "Lista de Tabelas")

def verificar_dados():
    """Opção 10: Verifica dados das principais tabelas"""
    print("\nVERIFICANDO DADOS DAS TABELAS")
    print("-" * 50)
    
    tabelas = ['Cidade', 'Bairro', 'Escola', 'Aluno', 'ColetaPluviometrica']
    
    for tabela in tabelas:
        query = f"SELECT COUNT(*) as total_registros FROM {tabela};"
        print(f"\nTabela: {tabela}")
        listar_dados(query, f"Contagem {tabela}")

def atualizar_dados():
    """Opção 11: Atualizar dados (exemplo)"""
    print("\nATUALIZAR DADOS")
    print("-" * 50)
    print("Exemplo: Atualizando status de validação pendente para aprovado")
    
    query = """
    UPDATE ColetaPluviometrica 
    SET status_validacao = 'aprovado' 
    WHERE status_validacao = 'pendente' 
    AND valor_medido_mm BETWEEN 10 AND 50;
    """
    
    executar_insercao(query, "Atualização de Status")

def limpar_dados():
    """Opção 12: Limpar todos os dados"""
    print("\nLIMPAR TODOS OS DADOS")
    print("-" * 50)
    
    confirmacao = input("ATENÇÃO: Isso irá deletar TODOS os dados! Digite 'CONFIRMAR' para continuar: ")
    
    if confirmacao == 'CONFIRMAR':
        queries = [
            "DELETE FROM ColetaPluviometrica;",
            "DELETE FROM Aluno;", 
            "DELETE FROM Escola;"
        ]
        
        for query in queries:
            executar_insercao(query, "Limpando dados")
        print("Todos os dados foram removidos!")
    else:
        print("Operação cancelada.")

def analisar_observacao_ia():
    """Opção 9: Análise de observação com IA Gemini"""
    print("\nANALISE DE OBSERVACAO COM IA")
    print("=" * 60)
    print("Transforme observações qualitativas em dados estruturados")
    print("=" * 60)
    
    # Primeiro, listar coletas com observações disponíveis
    print("\nColetas com observações disponíveis:")
    query_coletas = """
    SELECT 
        c.id_coleta,
        a.nome_completo_aluno,
        c.valor_medido_mm,
        c.status_validacao,
        LEFT(c.observacoes_aluno, 50) || '...' as observacao_resumo
    FROM 
        ColetaPluviometrica c
        JOIN Aluno a ON a.id_aluno = c.id_aluno_coleta
    WHERE 
        c.observacoes_aluno IS NOT NULL 
        AND TRIM(c.observacoes_aluno) != ''
    ORDER BY 
        c.data_hora_coleta DESC
    LIMIT 20;
    """
    
    coletas_df = listar_dados(query_coletas, "Coletas com Observações")
    
    if coletas_df is None or coletas_df.empty:
        print("\nNenhuma coleta com observações encontrada!")
        print("Dica: Use a Opção 2D para inserir coletas com observações.")
        return
    
    # Solicitar ID da coleta para análise
    try:
        id_coleta = int(input("\nDigite o ID da coleta para análise: "))
    except ValueError:
        print("ID inválido!")
        return
    
    # Buscar a observação completa
    query_observacao = f"""
    SELECT 
        c.observacoes_aluno,
        c.valor_medido_mm,
        c.status_validacao,
        a.nome_completo_aluno,
        c.data_hora_coleta
    FROM 
        ColetaPluviometrica c
        JOIN Aluno a ON a.id_aluno = c.id_aluno_coleta
    WHERE 
        c.id_coleta = {id_coleta};
    """
    
    conn = conectar_banco()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        cursor.execute(query_observacao)
        resultado = cursor.fetchone()
        
        if not resultado:
            print(f"Coleta com ID {id_coleta} não encontrada!")
            return
        
        observacao, valor_mm, status, nome_aluno, data_coleta = resultado
        
        if not observacao or observacao.strip() == '':
            print("Esta coleta não possui observações para análise!")
            return
        
        print(f"\nDADOS DA COLETA:")
        print("-" * 50)
        print(f"ID: {id_coleta}")
        print(f"Aluno: {nome_aluno}")
        print(f"Data: {data_coleta}")
        print(f"Valor medido: {valor_mm}mm")
        print(f"Status: {status}")
        print(f"\nObservação original:")
        print(f'"{observacao}"')
        
        print(f"\nProcessando com IA Gemini...")
        print("-" * 50)
        
        # Chamar a IA para análise
        resultado_ia = processar_observacao_com_ia(observacao)
        
        if resultado_ia:
            exibir_resultado_ia(resultado_ia, observacao)
        else:
            print("Erro no processamento com IA!")
            
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        conn.close()

def processar_observacao_com_ia(observacao_texto):
    """Processa a observação com IA Gemini e retorna dados estruturados"""
    
    # Prompt engenheirado para análise meteorológica
    prompt = f"""
Você é um assistente de análise de dados meteorológicos para um projeto escolar de monitoramento de chuva.

Sua tarefa é analisar a observação de um aluno sobre um evento climático e extrair informações estruturadas.

A observação a ser analisada é:
"{observacao_texto}"

Analise o texto e retorne suas conclusões estritamente no formato JSON abaixo, sem texto adicional:

{{
    "resumo": "Resuma tecnicamente a observação em uma frase clara e objetiva",
    "sentimento": "Classifique a severidade como: Normal, Preocupante, ou Severo",
    "palavras_chave": ["lista", "de", "fenômenos", "relevantes"],
    "impacto_observado": "Descreva os impactos mencionados pelo observador",
    "fenomenos_identificados": ["lista", "dos", "fenômenos", "meteorológicos"],
    "nivel_confianca": "Alto, Médio, ou Baixo - baseado na clareza da observação"
}}

Considere:
- Normal: chuva comum, sem impactos
- Preocupante: chuva forte, início de problemas
- Severo: tempestade, alagamentos, danos

Retorne apenas a estrutura JSON.
"""
    
    try:
        # Configurar o modelo Gemini
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Enviar prompt para a IA
        response = model.generate_content(prompt)
        
        if response and response.text:
            # Limpar resposta removendo markdown
            texto_resposta = response.text.strip()
            
            # Remover blocos de código markdown se existirem
            if "```json" in texto_resposta:
                inicio = texto_resposta.find("```json") + 7
                fim = texto_resposta.find("```", inicio)
                if fim != -1:
                    texto_resposta = texto_resposta[inicio:fim].strip()
            elif "```" in texto_resposta:
                inicio = texto_resposta.find("```") + 3
                fim = texto_resposta.find("```", inicio)
                if fim != -1:
                    texto_resposta = texto_resposta[inicio:fim].strip()
            
            # Tentar fazer parse do JSON
            resultado_json = json.loads(texto_resposta)
            return resultado_json
        else:
            print("Resposta vazia da IA!")
            return None
            
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON da IA: {e}")
        print(f"Resposta da IA: {response.text if response else 'Sem resposta'}")
        return None
    except Exception as e:
        print(f"Erro na comunicação com IA: {e}")
        return None

def exibir_resultado_ia(resultado, observacao_original):
    """Exibe o resultado da análise de IA de forma organizada"""
    
    print("\nRESULTADO DA ANALISE COM IA")
    print("=" * 60)
    
    print(f"\nResumo Técnico:")
    print(f"  {resultado.get('resumo', 'N/A')}")
    
    print(f"\nClassificação de Severidade:")
    severidade = resultado.get('sentimento', 'N/A')
    if severidade == 'Severo':
        print(f"  🔴 {severidade}")
    elif severidade == 'Preocupante':
        print(f"  🟡 {severidade}")
    else:
        print(f"  🟢 {severidade}")
    
    print(f"\nImpacto Observado:")
    print(f"  {resultado.get('impacto_observado', 'N/A')}")
    
    print(f"\nFenômenos Meteorológicos Identificados:")
    fenomenos = resultado.get('fenomenos_identificados', [])
    if fenomenos:
        for fenomeno in fenomenos:
            print(f"  • {fenomeno}")
    else:
        print("  Nenhum fenômeno específico identificado")
    
    print(f"\nPalavras-chave Extraídas:")
    palavras = resultado.get('palavras_chave', [])
    if palavras:
        print(f"  {', '.join(palavras)}")
    else:
        print("  Nenhuma palavra-chave identificada")
    
    print(f"\nNível de Confiança da Análise:")
    confianca = resultado.get('nivel_confianca', 'N/A')
    print(f"  {confianca}")
    
    print(f"\nObservação Original:")
    print(f'  "{observacao_original}"')
    
    print("\n" + "=" * 60)
    print("TRANSFORMACAO QUALITATIVO → QUANTITATIVO CONCLUIDA")
    print("=" * 60)

def main():
    """Função principal do menu"""
    while True:
        limpar_tela()
        exibir_menu()
        
        try:
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == '0':
                print("\nSaindo do sistema... Até logo!")
                break
            elif opcao == '1':
                criar_tabelas()
            elif opcao == '2':
                inserir_dados_exemplo()
            elif opcao == '3':
                consulta_estatisticas_escola()
            elif opcao == '4':
                consulta_ranking_participacao()
            elif opcao == '5':
                consulta_top_alunos()
            elif opcao == '6':
                consulta_status()
            elif opcao == '7':
                consulta_distribuicao_chuva()
            elif opcao == '8':
                consulta_personalizada()
            elif opcao == '9':
                analisar_observacao_ia()
            elif opcao == '10':
                listar_tabelas()
            elif opcao == '11':
                verificar_dados()
            elif opcao == '12':
                atualizar_dados()
            elif opcao == '13':
                limpar_dados()
            else:
                print("Opção inválida! Tente novamente.")
            
            pausar()
            
        except KeyboardInterrupt:
            print("\n\nSaindo do sistema...")
            break
        except Exception as e:
            print(f"Erro inesperado: {e}")
            pausar()

if __name__ == "__main__":
    # Configurar matplotlib para Windows
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['axes.unicode_minus'] = False
    
    try:
        plt.figure()
        plt.close()
    except:
        import matplotlib
        matplotlib.use('Agg')
    
    main()
