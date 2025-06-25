-- ========================================================================
-- SISTEMA DE COLETA PLUVIOMÉTRICA (SiCoPluE)
-- Criação de todas as tabelas e inserção de dados iniciais
-- ========================================================================

-- 1. CRIAÇÃO DAS TABELAS (na ordem correta das dependências)

-- Tabela Cidade
CREATE TABLE Cidade (
    id_cidade SERIAL PRIMARY KEY,
    nome_cidade VARCHAR(100) NOT NULL UNIQUE,
    uf VARCHAR(2) NOT NULL
);

-- Tabela Bairro
CREATE TABLE Bairro (
    id_bairro SERIAL PRIMARY KEY,
    nome_bairro VARCHAR(100) NOT NULL,
    id_cidade INTEGER NOT NULL,
    FOREIGN KEY (id_cidade) REFERENCES Cidade(id_cidade) ON DELETE RESTRICT
);

-- Tabela Escola
CREATE TABLE Escola (
    id_escola SERIAL PRIMARY KEY,
    nome_escola VARCHAR(255) NOT NULL UNIQUE,
    endereco_completo VARCHAR(255) NOT NULL,
    id_bairro INTEGER NOT NULL,
    FOREIGN KEY (id_bairro) REFERENCES Bairro(id_bairro) ON DELETE RESTRICT
);

-- Tabela Administrador
CREATE TABLE Administrador (
    id_admin SERIAL PRIMARY KEY,
    nome_completo_admin VARCHAR(150) NOT NULL,
    email_admin VARCHAR(100) NOT NULL UNIQUE,
    senha_admin VARCHAR(255) NOT NULL
);

-- Tabela Professor
CREATE TABLE Professor (
    id_professor SERIAL PRIMARY KEY,
    nome_completo_professor VARCHAR(150) NOT NULL,
    email_professor VARCHAR(100) NOT NULL UNIQUE,
    senha_professor VARCHAR(255) NOT NULL,
    id_escola INTEGER NOT NULL,
    FOREIGN KEY (id_escola) REFERENCES Escola(id_escola) ON DELETE CASCADE
);

-- Tabela Aluno
CREATE TABLE Aluno (
    id_aluno SERIAL PRIMARY KEY,
    nome_completo_aluno VARCHAR(150) NOT NULL,
    email_aluno VARCHAR(100) NOT NULL UNIQUE,
    senha_aluno VARCHAR(255) NOT NULL,
    turma_aluno VARCHAR(20),
    id_escola INTEGER NOT NULL,
    FOREIGN KEY (id_escola) REFERENCES Escola(id_escola) ON DELETE CASCADE
);

-- Tabela Pluviometro
CREATE TABLE Pluviometro (
    id_pluviometro SERIAL PRIMARY KEY,
    modelo_pluviometro VARCHAR(100),
    data_instalacao DATE,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    status_operacional VARCHAR(15) NOT NULL DEFAULT 'ativo' 
        CHECK (status_operacional IN ('ativo', 'em_manutencao', 'desativado')),
    id_escola INTEGER NOT NULL,
    FOREIGN KEY (id_escola) REFERENCES Escola(id_escola) ON DELETE CASCADE
);

-- Tabela ColetaPluviometrica
CREATE TABLE ColetaPluviometrica (
    id_coleta SERIAL PRIMARY KEY,
    data_hora_coleta TIMESTAMP NOT NULL,
    valor_medido_mm DECIMAL(6, 2) NOT NULL,
    observacoes_aluno TEXT,
    status_validacao VARCHAR(10) NOT NULL DEFAULT 'pendente' 
        CHECK (status_validacao IN ('pendente', 'aprovado', 'rejeitado')),
    id_pluviometro INTEGER NOT NULL,
    id_aluno_coleta INTEGER NOT NULL,
    id_professor_validacao INTEGER,
    FOREIGN KEY (id_pluviometro) REFERENCES Pluviometro(id_pluviometro) ON DELETE RESTRICT,
    FOREIGN KEY (id_aluno_coleta) REFERENCES Aluno(id_aluno) ON DELETE SET NULL,
    FOREIGN KEY (id_professor_validacao) REFERENCES Professor(id_professor) ON DELETE SET NULL
);

-- Tabela ParametroAlerta
CREATE TABLE ParametroAlerta (
    id_parametro SERIAL PRIMARY KEY,
    tipo_risco_parametro VARCHAR(30) NOT NULL,
    limite_mm_hora DECIMAL(6, 2),
    id_bairro_monitorado INTEGER NOT NULL,
    UNIQUE (id_bairro_monitorado, tipo_risco_parametro),
    FOREIGN KEY (id_bairro_monitorado) REFERENCES Bairro(id_bairro) ON DELETE CASCADE
);

-- Tabela AlertaMeteorologico
CREATE TABLE AlertaMeteorologico (
    id_alerta SERIAL PRIMARY KEY,
    tipo_alerta VARCHAR(30) NOT NULL,
    data_hora_emissao TIMESTAMP NOT NULL,
    descricao_alerta_gerado TEXT,
    nivel_severidade VARCHAR(10) NOT NULL 
        CHECK (nivel_severidade IN ('baixo', 'moderado', 'alto')),
    id_bairro_afetado INTEGER NOT NULL,
    FOREIGN KEY (id_bairro_afetado) REFERENCES Bairro(id_bairro)
);

-- ========================================================================
-- 2. INSERÇÃO DOS DADOS INICIAIS (na ordem correta das dependências)
-- ========================================================================

-- Inserir Cidades
INSERT INTO Cidade (nome_cidade, uf) VALUES
    ('Araranguá', 'SC'), 
    ('Sombrio', 'SC'), 
    ('Criciúma', 'SC');

-- Inserir Bairros
INSERT INTO Bairro (nome_bairro, id_cidade) VALUES
    ('Centro', 1), 
    ('Cidade Alta', 1), 
    ('Mato Alto', 1), 
    ('Centro', 2), 
    ('Centro', 3);

-- Inserir Escolas
INSERT INTO Escola (nome_escola, endereco_completo, id_bairro) VALUES
    ('UFSC - Campus Araranguá', 'Rua Pedro João Pereira, 150', 2),
    ('Colégio Murialdo', 'Praça Hercílio Luz, 135', 1),
    ('EEB Castro Alves', 'Av. XV de Novembro, 1234', 1);

-- Inserir Administrador
INSERT INTO Administrador (nome_completo_admin, email_admin, senha_admin) VALUES
    ('Admin Geral', 'admin@sicoplue.com', 'senha_forte_123');

-- Inserir Professores
INSERT INTO Professor (nome_completo_professor, email_professor, senha_professor, id_escola) VALUES
    ('Alexandre Gonçalves', 'alexandre.g@ufsc.br', 'senha_prof1', 1),
    ('Maria Silva', 'maria.silva@murialdo.com', 'senha_prof2', 2),
    ('João Santos', 'joao.santos@sed.sc.gov.br', 'senha_prof3', 3);

-- Inserir Alunos
INSERT INTO Aluno (nome_completo_aluno, email_aluno, senha_aluno, turma_aluno, id_escola) VALUES
    ('Carlos Souza', 'carlos.s@aluno.ufsc.br', 'senha_aluno1', 'TADS', 1),
    ('Ana Pereira', 'ana.p@aluno.ufsc.br', 'senha_aluno2', 'TADS', 1),
    ('Beatriz Costa', 'beatriz.c@murialdo.com', 'senha_aluno3', '8A', 2),
    ('Lucas Ferreira', 'lucas.f@murialdo.com', 'senha_aluno4', '9B', 2),
    ('Juliana Almeida', 'juliana.a@sed.sc.gov.br', 'senha_aluno5', '1C', 3);

-- Inserir Pluviômetros
INSERT INTO Pluviometro (modelo_pluviometro, data_instalacao, latitude, longitude, id_escola) VALUES
    ('Incoterm-Eco', '2025-03-10', -28.941657, -49.492067, 1),
    ('Ville de Paris', '2025-03-15', -28.937215, -49.486245, 2),
    ('Incoterm-Eco', '2025-03-20', -28.939871, -49.488312, 3);

-- Inserir Coletas Pluviométricas
INSERT INTO ColetaPluviometrica (data_hora_coleta, valor_medido_mm, observacoes_aluno, status_validacao, id_pluviometro, id_aluno_coleta, id_professor_validacao) VALUES
    ('2025-05-10 08:00:00', 15.5, 'Chuva moderada durante a noite.', 'aprovado', 1, 1, 1),
    ('2025-05-11 08:00:00', 5.0, 'Chuvisco pela manhã.', 'aprovado', 1, 2, 1),
    ('2025-05-11 08:05:00', 10.0, 'Coleta da escola Murialdo.', 'aprovado', 2, 3, 2),
    ('2025-05-12 08:00:00', 35.2, 'Tempestade forte com vento.', 'aprovado', 1, 1, 1),
    ('2025-05-12 08:10:00', 40.0, 'Chuva muito forte.', 'aprovado', 3, 5, 3),
    ('2025-06-15 08:00:00', 2.0, 'Nenhuma chuva significativa.', 'pendente', 1, 2, NULL),
    ('2025-06-15 08:02:00', 22.0, 'Chuva constante.', 'aprovado', 2, 4, 2),
    ('2025-06-16 08:00:00', 55.8, 'Chuva torrencial que causou alagamentos na rua.', 'aprovado', 2, 3, 2);

-- Inserir Parâmetros de Alerta
INSERT INTO ParametroAlerta (tipo_risco_parametro, limite_mm_hora, id_bairro_monitorado) VALUES
    ('risco_inundacao', 50.0, 1),
    ('risco_inundacao', 45.0, 2);

-- Inserir Alertas Meteorológicos
INSERT INTO AlertaMeteorologico (tipo_alerta, data_hora_emissao, descricao_alerta_gerado, nivel_severidade, id_bairro_afetado) VALUES
    ('risco_inundacao', '2025-06-16 08:30:00', 'Alerta gerado devido a coleta de 55.8mm em curto período de tempo no pluviômetro da escola Murialdo. Alto risco de alagamentos na região central.', 'alto', 1);

-- ========================================================================
-- VERIFICAÇÃO DOS DADOS INSERIDOS
-- ========================================================================

-- Verificar estrutura das tabelas criadas
SELECT 
    table_name,
    table_type
FROM information_schema.tables 
WHERE table_schema = 'public'
ORDER BY table_name;

-- Contar registros em cada tabela
SELECT 'Cidade' as tabela, COUNT(*) as registros FROM Cidade
UNION ALL
SELECT 'Bairro', COUNT(*) FROM Bairro
UNION ALL
SELECT 'Escola', COUNT(*) FROM Escola
UNION ALL
SELECT 'Administrador', COUNT(*) FROM Administrador
UNION ALL
SELECT 'Professor', COUNT(*) FROM Professor
UNION ALL
SELECT 'Aluno', COUNT(*) FROM Aluno
UNION ALL
SELECT 'Pluviometro', COUNT(*) FROM Pluviometro
UNION ALL
SELECT 'ColetaPluviometrica', COUNT(*) FROM ColetaPluviometrica
UNION ALL
SELECT 'ParametroAlerta', COUNT(*) FROM ParametroAlerta
UNION ALL
SELECT 'AlertaMeteorologico', COUNT(*) FROM AlertaMeteorologico;