# Sistema de Consulta de Pluviometria Escolar

## Status: PROJETO ORGANIZADO E REFATORADO - VERSÃO FINAL

Este é o **Sistema de Consulta de Pluviometria Escolar**

## Estrutura do Projeto ORGANIZADA

```
CodigoProjeto/
├── menu_principal.py          # Sistema principal da aplicação
├── config.py                  # Configurações centralizadas
├── requirements.txt           # Dependências Python
├── executar_menu.bat         # Execução fácil no Windows
├── README.md                 # Esta documentação
├── COMO_EXECUTAR.md          # Guia de execução
├── ESTRUTURA_FINAL.md        # Documentação da estrutura
├── sql/                      # Scripts SQL
│   └── CriandoInserindoDados.sql # Estrutura do banco
├── testes/                   # Arquivos de teste
│   ├── teste_ia.py              # Teste da integração IA
│   ├── teste_query_personalizada.py # Teste conexão BD
│   └── teste_sistema_completo.py # Teste geral
├── resultados/               # Saídas do sistema
│   ├── graficos/                # Gráficos gerados (.png)
│   └── relatorios/              # Relatórios CSV
├── .venv/                    # Ambiente virtual Python
└── .vscode/                  # Configurações do VS Code
```

## Execução Rápida

### Windows (Recomendado):
```cmd
executar_menu.bat
```

### Manual:
```cmd
.venv\Scripts\activate
python menu_principal.py
```

## Principais Recursos

### INSERÇÃO DE DADOS LIMPA
- **Sem gráficos** durante inserção
- Interface profissional
- Validação de dados

### CONSULTAS AVANÇADAS
- 7 consultas pré-definidas
- Consulta personalizada
- Gráficos **apenas** quando apropriado

### GERENCIAMENTO DE DADOS
- Criar/limpar tabelas
- Verificar estrutura
- Backup automático

## Melhorias Implementadas

### **Código Limpo**
- Funções especializadas
- Separação clara de responsabilidades

### **Gráficos Inteligentes**
- Apenas em consultas de análise
- Detecta automaticamente o tipo de dados
- Salva resultados em CSV

### **Projeto Minimalista**
- Apenas arquivos essenciais
- Estrutura organizada
- Fácil manutenção

## Configuração de Banco

Antes de executar, configure as credenciais em qualquer script Python:

```python
DB_CONFIG = {
    'host': 'localhost',
    'database': 'siCoPluE',  # Seu banco
    'user': 'postgres',      # Seu usuário
    'password': '123',       # Sua senha
    'port': '5432'
}
```

## Gráficos Gerados

O sistema gera automaticamente:

1. **Distribuição de Problemas por Categoria**
2. **Status dos Problemas** (gráfico de pizza)
3. **Problemas por Usuário** (top 10)
4. **Timeline de Criação** (apenas no sistema completo)
5. **Distribuição de Prioridades** (rosca)
6. **Soluções por Técnico** (apenas no sistema completo)

## Dependências

Todas as dependências estão listadas em `requirements.txt`:
- psycopg2-binary
- pandas
- matplotlib
- seaborn
- numpy

## Validação

Execute `python validar_sistema.py` para verificar se todos os componentes estão funcionais.

## Suporte

- Windows compatível
- PostgreSQL integrado
- VS Code configurado
- Ambiente virtual ativo
- Todas as dependências instaladas

### Mudanças Implementadas:
- Criada função `executar_insercao()` específica para operações de inserção
- Todas as inserções de dados agora usam esta função especializada
- Gráficos são gerados APENAS em consultas (Opções 3-9)
- Interface mais profissional e focada no objetivo

### Como Testar:
1. Execute `python menu_principal.py`
2. Escolha Opção 2 (Inserir dados)
3. Insira qualquer tipo de dado (A, B, C ou D)
4. Confirme que NÃO há geração de gráficos
5. Use Opções 3-9 para ver gráficos (quando apropriado)


## NOVA FUNCIONALIDADE: ANÁLISE COM IA

###  **Integração com Google Gemini AI**
- **Opção 9**: Análise de Observação com IA
- **Transformação**: Dados qualitativos → Dados estruturados
- **Modelo**: Gemini-1.5-flash (Google)

###  **Como Funciona**:
1. **Input**: Texto livre do aluno (observações meteorológicas)
2. **Processamento**: IA analisa semanticamente o conteúdo
3. **Output**: JSON estruturado com insights organizados

### **Dados Extraídos pela IA**:
- **Resumo técnico** da observação
- **Classificação de severidade** (Normal/Preocupante/Severo)
- **Palavras-chave** meteorológicas
- **Impactos observados**
- **Fenômenos identificados**
- **Nível de confiança** da análise

### **Exemplo de Transformação**:
```
INPUT (qualitativo):
"Chuva muito forte com granizo e vento, vi alguns alagamentos..."

OUTPUT (estruturado):
- Resumo: "Evento severo com granizo, vento e alagamentos"
- Severidade: 🔴 Severo
- Palavras-chave: ["granizo", "vento forte", "alagamentos"]
- Confiança: Alto
```

### **Dependência Adicionada**:
- `google-generativeai==0.3.2` (API do Gemini)

---

**Status:** Pronto para produção  
**Última atualização:** Sistema completamente restaurado e validado  
**Próximos passos:** Configure as credenciais do banco e execute o sistema!
