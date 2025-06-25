# COMO EXECUTAR - Sistema SiCoPluE - VERSÃO ORGANIZADA

## ESTRUTURA ATUALIZADA

Este sistema foi **completamente refatorado e organizado** com:
- **Configuração centralizada** (config.py)
- **Diretórios organizados** (sql/, resultados/, testes/)
- **Paths dinâmicos** para todos os arquivos
- **Estrutura profissional** e fácil manutenção

## TESTE DO SISTEMA

Antes de usar, verifique se tudo está funcionando:
```cmd
python testes\teste_sistema_completo.py
```

## EXECUÇÃO RÁPIDA (Windows)

### Método 1: Execução Automática
```cmd
executar_menu.bat
```

### Método 2: Execução Manual
```cmd
# 1. Ativar ambiente virtual
.venv\Scripts\activate

# 2. Executar sistema
python menu_principal.py
```

## MENU PRINCIPAL - Opções Disponíveis

```
1.  CRIAR TABELAS         → Cria estrutura do banco
2.  INSERIR DADOS         → Adiciona dados (SEM gráficos)
3.  Estatísticas Escola   → Análise por escola
4.  Ranking Participação  → Ranking de coletas
5.  Top 10 Alunos        → Alunos mais ativos
6.  Análise por Status   → Validação de coletas
7.  Distribuição Chuva   → Faixas de precipitação
8.  CONSULTA PERSONALIZADA → Seu próprio SQL
9.  Listar Tabelas       → Estrutura do banco
10. Verificar Dados      → Contagem de registros
11. Atualizar Dados      → Modificar registros
12. Limpar Dados         → Remover todos os dados
0.  SAIR                 → Encerrar sistema
```

## INSERÇÃO DE DADOS (Opção 2)

### Escolhas Disponíveis:
- **A)** Inserir CIDADE → Independente
- **B)** Dados EXEMPLO → Conjunto completo para testes
- **C)** Inserir ALUNO → Em escola existente
- **D)** Inserir COLETA → De aluno existente

### Garantias:
- **NÃO gera gráficos** durante inserção
- Interface limpa e profissional
- Validação automática de dados
- Mensagens claras de sucesso/erro

## CONSULTAS COM GRÁFICOS (Opções 3-8)

### Gráficos Automáticos:
- Detecta automaticamente o tipo de dados
- Gera visualizações apropriadas
- Salva resultados em CSV
- Arquivo PNG com gráficos

### Tipos de Gráficos:
- Barras (contagens, totais)
- Pizza (distribuições)
- Scatter (correlações)
- Linha (tendências)

## ANÁLISE COM IA (Opção 9)

### **Nova Funcionalidade**: Transformação Qualitativo → Quantitativo

#### Como usar:
1. **Execute**: `executar_menu.bat`
2. **Escolha**: Opção 9 (Análise de Observação com IA)
3. **Selecione**: ID de uma coleta com observações
4. **Aguarde**: Processamento semântico com Gemini AI
5. **Veja**: Dados estruturados extraídos

#### Exemplo prático:
```
Observação do aluno:
"Chuva muito forte com granizo e vento, vi alguns alagamentos começando na rua da frente."

Resultado da IA:
🔴 Severidade: Severo
📝 Resumo: "Evento meteorológico intenso com granizo, vento e início de alagamentos"
Palavras-chave: ["granizo", "vento forte", "alagamentos"]
Confiança: Alto
```

#### Pré-requisitos:
- Coletas com observações preenchidas
- Conexão com internet (API Gemini)
- Dados de exemplo (use Opção 2B primeiro)

#### Vantagens:
- **Automação** da análise qualitativa
- **Padronização** de classificações
- **Extração** de insights estruturados
- **Escalabilidade** para grandes volumes

## REQUISITOS TÉCNICOS

### Dependências:
```txt
psycopg2-binary
pandas
matplotlib
seaborn
```

### Banco de Dados:
- PostgreSQL
- Configuração em `teste_query_personalizada.py`

## SOLUÇÃO DE PROBLEMAS

### Erro de Conexão:
1. Verificar se PostgreSQL está rodando
2. Conferir credenciais em `teste_query_personalizada.py`
3. Testar conexão manual

### Erro de Dependências:
```cmd
pip install -r requirements.txt
```

### Ambiente Virtual:
```cmd
# Criar novo ambiente
python -m venv .venv

# Ativar
.venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

## 📞 DICAS DE USO

### Para Começar:
1. Execute `executar_menu.bat`
2. Use Opção 1 para criar tabelas
3. Use Opção 2B para dados de exemplo
4. Explore as consultas (Opções 3-7)

### Para Desenvolvimento:
- Use Opção 8 para SQL personalizado
- Use Opção 9 para ver estrutura
- Use Opção 10 para verificar dados

### Para Produção:
- Use Opções 2A,C,D para dados reais
- Use Opções 3-7 para relatórios
- Use Opção 11 para atualizações
