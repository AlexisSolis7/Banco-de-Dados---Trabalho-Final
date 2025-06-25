# -*- coding: utf-8 -*-
"""
Script para Queries Personalizadas - SiCoPluE
Use este arquivo para testar suas próprias consultas SQL
"""

import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import os
warnings.filterwarnings('ignore')

# Configuração do matplotlib para Windows
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# Configurar matplotlib para funcionar sem interface gráfica (terminal)
try:
    # Tentar usar interface gráfica (VS Code)
    plt.figure()
    plt.close()
except:
    # Se não conseguir, usar modo não-interativo (terminal)
    import matplotlib
    matplotlib.use('Agg')
    print("Modo não-interativo ativado - gráficos serão salvos como arquivos")

# Configurações de conexão
DB_CONFIG = {
    'host': 'localhost',
    'database': 'T2BancoDeDados',  # Substitua pelo nome do seu banco
    'user': 'postgres',      # Substitua pelo seu usuário
    'password': '123456',       # Substitua pela sua senha
    'port': '5432'
}

def conectar_banco():
    """Conecta ao banco PostgreSQL"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("Conectado ao banco!")
        return conn
    except Exception as e:
        print(f"Erro: {e}")
        return None

def gerar_graficos(df):
    """Gera gráficos automaticamente baseados nos dados da query"""
    if df.empty:
        print("Sem dados para gerar gráficos")
        return
    
    # Configurar estilo
    sns.set_style("whitegrid")
    
    print("\nAnalisando dados para gerar gráficos...")
    print(f"Colunas disponíveis: {list(df.columns)}")
    print(f"Número de linhas: {len(df)}")
    
    graficos_gerados = []
    
    # Detectar colunas numéricas e texto
    colunas_numericas = df.select_dtypes(include=['number']).columns.tolist()
    colunas_texto = df.select_dtypes(include=['object']).columns.tolist()
    
    print(f"Colunas numéricas: {colunas_numericas}")
    print(f"Colunas de texto: {colunas_texto}")
    
    # Se temos nome_escola e dados numéricos, gerar gráficos específicos
    if 'nome_escola' in df.columns:
        print("\nDetectada coluna 'nome_escola' - gerando gráficos por escola...")
        
        # Gráfico 1: Total de coletas por escola
        if 'total_coletas' in df.columns:
            plt.figure(figsize=(12, 8))
            bars = plt.bar(df['nome_escola'], df['total_coletas'], color='skyblue', edgecolor='navy')
            
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                        f'{int(height)}', ha='center', va='bottom', fontweight='bold')
            
            plt.title('Total de Coletas por Escola', fontsize=16, fontweight='bold')
            plt.xlabel('Escola', fontsize=12)
            plt.ylabel('Número de Coletas', fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            filename = 'resultados/graficos/grafico_total_coletas.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            graficos_gerados.append(filename)
            
            try:
                plt.show()
            except:
                pass
            plt.close()
            print(f"Gráfico salvo: {filename}")
        
        # Gráfico 2: Média de chuva por escola
        if 'media_chuva' in df.columns:
            plt.figure(figsize=(10, 6))
            bars = plt.barh(df['nome_escola'], df['media_chuva'], color='lightgreen', edgecolor='darkgreen')
            
            for i, bar in enumerate(bars):
                width = bar.get_width()
                plt.text(width + 0.5, bar.get_y() + bar.get_height()/2,
                        f'{width:.1f}mm', ha='left', va='center', fontweight='bold')
            
            plt.title('Média de Chuva por Escola', fontsize=16, fontweight='bold')
            plt.xlabel('Média de Chuva (mm)', fontsize=12)
            plt.ylabel('Escola', fontsize=12)
            plt.tight_layout()
            
            filename = 'resultados/graficos/grafico_media_chuva.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            graficos_gerados.append(filename)
            
            try:
                plt.show()
            except:
                pass
            plt.close()
            print(f"Gráfico salvo: {filename}")
        
        # Gráfico 3: Total de alunos por escola
        if 'total_alunos' in df.columns:
            plt.figure(figsize=(10, 8))
            colors = plt.cm.Set3(range(len(df)))
            
            wedges, texts, autotexts = plt.pie(df['total_alunos'], 
                                              labels=df['nome_escola'],
                                              autopct='%1.1f%%',
                                              colors=colors,
                                              startangle=90)
            
            plt.title('Distribuição de Alunos por Escola', fontsize=16, fontweight='bold')
            
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            
            plt.axis('equal')
            plt.tight_layout()
            
            filename = 'resultados/graficos/grafico_alunos_escola.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            graficos_gerados.append(filename)
            
            try:
                plt.show()
            except:
                pass
            plt.close()
            print(f"Gráfico salvo: {filename}")
    
    # Gráfico genérico para dados que não sejam por escola
    else:
        print("\nNão foi detectada coluna 'nome_escola' - tentando gerar gráfico genérico...")
        
        # Se há pelo menos uma coluna de texto e uma numérica, fazer gráfico de barras
        if len(colunas_texto) >= 1 and len(colunas_numericas) >= 1:
            coluna_x = colunas_texto[0]  # Primeira coluna de texto como eixo X
            coluna_y = colunas_numericas[0]  # Primeira coluna numérica como eixo Y
            
            plt.figure(figsize=(12, 8))
            bars = plt.bar(df[coluna_x], df[coluna_y], color='coral', edgecolor='darkred')
            
            # Adicionar valores nas barras
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                        f'{height:.1f}', ha='center', va='bottom', fontweight='bold')
            
            plt.title(f'{coluna_y.replace("_", " ").title()} por {coluna_x.replace("_", " ").title()}', 
                     fontsize=16, fontweight='bold')
            plt.xlabel(coluna_x.replace("_", " ").title(), fontsize=12)
            plt.ylabel(coluna_y.replace("_", " ").title(), fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            filename = f'resultados/graficos/grafico_{coluna_x}_{coluna_y}.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            graficos_gerados.append(filename)
            
            try:
                plt.show()
            except:
                pass
            plt.close()
            print(f"Gráfico genérico salvo: {filename}")
        
        # Se há múltiplas colunas numéricas, fazer gráfico comparativo
        if len(colunas_numericas) >= 2:
            primeira_col = colunas_numericas[0]
            segunda_col = colunas_numericas[1]
            
            plt.figure(figsize=(10, 6))
            plt.scatter(df[primeira_col], df[segunda_col], alpha=0.7, s=100, color='purple')
            
            plt.title(f'{segunda_col.replace("_", " ").title()} vs {primeira_col.replace("_", " ").title()}',
                     fontsize=16, fontweight='bold')
            plt.xlabel(primeira_col.replace("_", " ").title(), fontsize=12)
            plt.ylabel(segunda_col.replace("_", " ").title(), fontsize=12)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            
            filename = f'resultados/graficos/grafico_scatter_{primeira_col}_{segunda_col}.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            graficos_gerados.append(filename)
            
            try:
                plt.show()
            except:
                pass
            plt.close()
            print(f"Gráfico de dispersão salvo: {filename}")
    
    # Relatório final
    if graficos_gerados:
        print(f"\n{len(graficos_gerados)} gráfico(s) gerado(s) com sucesso!")
        print("Arquivos criados:")
        for grafico in graficos_gerados:
            if os.path.exists(grafico):
                size = os.path.getsize(grafico) / 1024  # KB
                print(f"   {grafico} ({size:.1f} KB)")
            else:
                print(f"   {grafico} (erro ao salvar)")
    else:
        print("\nNenhum gráfico foi gerado.")
        print("Motivos possíveis:")
        print("- Não há dados suficientes")
        print("- Estrutura dos dados não é adequada para gráficos")
        print("- Colunas esperadas não foram encontradas")
        print("\nDica: Para gráficos automáticos por escola, sua query deve ter:")
        print("- Uma coluna chamada 'nome_escola'")
        print("- Pelo menos uma coluna numérica como 'total_coletas', 'media_chuva' ou 'total_alunos'")

def executar_query_personalizada():
    """Execute sua query personalizada aqui"""
    
    # ESCREVA SUA QUERY AQUI:
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
    
    conn = conectar_banco()
    if not conn:
        return
    
    try:
        # Executar query
        df = pd.read_sql_query(query, conn)
        
        # Mostrar resultados
        print("\nRESULTADOS DA SUA QUERY:")
        print("="*50)
        print(df.to_string(index=False))
        
        # Opcional: Salvar em CSV
        df.to_csv('resultado_query.csv', index=False)
        print(f"\nResultado salvo em 'resultado_query.csv'")
        
        # GERAR GRÁFICOS AUTOMATICAMENTE
        gerar_graficos(df)
        
    except Exception as e:
        print(f"Erro na query: {e}")
    
    finally:
        conn.close()

def main():
    """Função principal"""
    print("EXECUTAR QUERY PERSONALIZADA")
    print("="*40)
    
    executar_query_personalizada()
    
    input("\nPressione Enter para sair...")

if __name__ == "__main__":
    main()
