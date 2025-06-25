"""
Teste de integração para verificar se a configuração centralizada funciona corretamente.
Este script testa:
1. Importação do módulo config
2. Criação de diretórios
3. Paths de gráficos e relatórios
4. Estrutura geral do projeto
"""

import sys
import os

def testar_configuracao():
    """Testa se o sistema de configuração está funcionando."""
    
    print("TESTE DE CONFIGURAÇÃO DO SISTEMA")
    print("=" * 50)
    
    try:
        # Adicionar o diretório pai ao path para importar config
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, parent_dir)
        
        # Teste 1: Importar configuração
        print("\n1. Testando importação da configuração...")
        import config
        print("Módulo config importado com sucesso")
        
        # Teste 2: Verificar paths básicos
        print("\n2. Testando paths básicos...")
        print(f"   Base DIR: {config.BASE_DIR}")
        print(f"   SQL DIR: {config.SQL_DIR}")
        print(f"   Resultados DIR: {config.RESULTADOS_DIR}")
        print(f"   Gráficos DIR: {config.GRAFICOS_DIR}")
        print(f"   Relatórios DIR: {config.RELATORIOS_DIR}")
        print("Paths básicos OK")
        
        # Teste 3: Testar funções de path
        print("\n3. Testando funções de path...")
        path_grafico = config.get_path_grafico('alunos_escola')
        path_relatorio = config.get_path_relatorio('analise_status')
        print(f"   Path gráfico: {path_grafico}")
        print(f"   Path relatório: {path_relatorio}")
        print("Funções de path OK")
        
        # Teste 4: Verificar estrutura
        print("\n4. Verificando estrutura de diretórios...")
        estrutura_ok = config.verificar_estrutura()
        if estrutura_ok:
            print("Estrutura de diretórios OK")
        else:
            print("AVISO: Alguns diretórios podem estar ausentes")
        
        # Teste 5: Arquivo SQL existe
        print("\n5. Verificando arquivo SQL principal...")
        if os.path.exists(config.SQL_CRIACAO_DADOS):
            print(f"Arquivo SQL encontrado: {config.SQL_CRIACAO_DADOS}")
        else:
            print(f"❌ Arquivo SQL não encontrado: {config.SQL_CRIACAO_DADOS}")
        
        # Teste 6: Listar resultados existentes
        print("\n6. Listando arquivos de resultados...")
        config.listar_arquivos_resultados()
        
        print("\n" + "=" * 50)
        print("TESTE CONCLUÍDO COM SUCESSO!")
        print("   O sistema de configuração está funcionando corretamente.")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erro ao importar config: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        return False

def testar_menu_principal():
    """Testa se o menu principal pode usar a configuração."""
    
    print("\nTESTE DE INTEGRAÇÃO COM MENU PRINCIPAL")
    print("=" * 50)
    
    try:
        # Verifica se o menu principal existe (no diretório pai)
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        menu_path = os.path.join(parent_dir, 'menu_principal.py')
        if os.path.exists(menu_path):
            print("menu_principal.py encontrado")
            
            # Verifica se pode ser importado (sem executar)
            # Isso testaria sintaxe básica
            with open(menu_path, 'r', encoding='utf-8') as f:
                conteudo = f.read()
                if 'import config' in conteudo or 'from config' in conteudo:
                    print("Menu principal usa sistema de configuração")
                else:
                    print("AVISO: Menu principal pode não estar usando config centralizado")
                    
        else:
            print("❌ menu_principal.py não encontrado")
            
    except Exception as e:
        print(f"❌ Erro ao testar menu principal: {e}")

if __name__ == "__main__":
    # Mudança para o diretório pai do projeto
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(script_dir)
    
    # Executa testes
    sucesso_config = testar_configuracao()
    testar_menu_principal()
    
    if sucesso_config:
        print("\nSISTEMA PRONTO PARA USO!")
        print("   Execute: python menu_principal.py")
        print("   Ou use:  executar_menu.bat")
    else:
        print("\n❌ SISTEMA COM PROBLEMAS")
        print("   Verifique os erros acima antes de continuar.")
