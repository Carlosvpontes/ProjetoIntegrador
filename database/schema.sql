-- =====================================================================
-- EstoqueFácil: projeto físico do banco de dados
-- SGBD: PostgreSQL 16+ (hospedado no Neon)
-- Documentação: docs/situacao-1/04-banco-de-dados.md
--
-- Observação: em produção as tabelas são criadas automaticamente pelo
-- script criar_banco.py (a cada publicação no Render). Este arquivo
-- documenta o mesmo modelo em SQL puro e pode ser executado no
-- "SQL Editor" do Neon para recriar o banco do zero.
-- =====================================================================

-- Remove os objetos na ordem inversa das dependências (permite recriar do zero)
DROP TABLE IF EXISTS movimentacao;
DROP TABLE IF EXISTS produto;
DROP TABLE IF EXISTS fornecedor;
DROP TABLE IF EXISTS categoria;
DROP TABLE IF EXISTS usuario;
DROP TYPE IF EXISTS tipo_movimentacao;

-- Tipo enumerado com os dois tipos de movimentação
CREATE TYPE tipo_movimentacao AS ENUM ('ENTRADA', 'SAIDA');

-- ---------------------------------------------------------------------
-- usuario: pessoas que acessam o sistema
-- ---------------------------------------------------------------------
CREATE TABLE usuario (
    id          SERIAL       PRIMARY KEY,
    nome        VARCHAR(100) NOT NULL,
    email       VARCHAR(120) NOT NULL,
    senha_hash  VARCHAR(255) NOT NULL,
    criado_em   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_usuario_email UNIQUE (email)                      -- RN08
);

-- ---------------------------------------------------------------------
-- categoria: agrupamento de produtos
-- ---------------------------------------------------------------------
CREATE TABLE categoria (
    id          SERIAL       PRIMARY KEY,
    nome        VARCHAR(60)  NOT NULL,
    descricao   VARCHAR(255),
    CONSTRAINT uk_categoria_nome UNIQUE (nome)
);

-- ---------------------------------------------------------------------
-- fornecedor: empresas que fornecem produtos
-- ---------------------------------------------------------------------
CREATE TABLE fornecedor (
    id          SERIAL       PRIMARY KEY,
    nome        VARCHAR(100) NOT NULL,
    cnpj        VARCHAR(14),
    telefone    VARCHAR(20),
    email       VARCHAR(120),
    CONSTRAINT uk_fornecedor_cnpj UNIQUE (cnpj),
    CONSTRAINT ck_fornecedor_cnpj CHECK (cnpj IS NULL OR cnpj ~ '^[0-9]{14}$')
);

-- ---------------------------------------------------------------------
-- produto: itens controlados no estoque
-- ---------------------------------------------------------------------
CREATE TABLE produto (
    id                SERIAL        PRIMARY KEY,
    codigo            VARCHAR(30)   NOT NULL,
    nome              VARCHAR(100)  NOT NULL,
    descricao         VARCHAR(255),
    categoria_id      INTEGER       NOT NULL,
    fornecedor_id     INTEGER,
    preco_custo       NUMERIC(10,2) NOT NULL DEFAULT 0.00,
    preco_venda       NUMERIC(10,2) NOT NULL DEFAULT 0.00,
    estoque_minimo    INTEGER       NOT NULL DEFAULT 0,
    quantidade_atual  INTEGER       NOT NULL DEFAULT 0,             -- RN03: só muda via movimentação
    criado_em         TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em     TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_produto_codigo           UNIQUE (codigo),          -- RN05
    CONSTRAINT ck_produto_preco_custo      CHECK (preco_custo >= 0), -- RN12
    CONSTRAINT ck_produto_preco_venda      CHECK (preco_venda >= 0), -- RN12
    CONSTRAINT ck_produto_estoque_minimo   CHECK (estoque_minimo >= 0),
    CONSTRAINT ck_produto_quantidade_atual CHECK (quantidade_atual >= 0),  -- RN03
    CONSTRAINT fk_produto_categoria  FOREIGN KEY (categoria_id)
        REFERENCES categoria (id) ON DELETE RESTRICT,               -- RN06
    CONSTRAINT fk_produto_fornecedor FOREIGN KEY (fornecedor_id)
        REFERENCES fornecedor (id) ON DELETE RESTRICT               -- RN06
);

CREATE INDEX idx_produto_nome ON produto (nome);                    -- RF10

-- ---------------------------------------------------------------------
-- movimentacao: entradas e saídas de mercadoria (registros imutáveis, RN11)
-- ---------------------------------------------------------------------
CREATE TABLE movimentacao (
    id          SERIAL            PRIMARY KEY,
    produto_id  INTEGER           NOT NULL,
    usuario_id  INTEGER           NOT NULL,
    tipo        tipo_movimentacao NOT NULL,
    quantidade  INTEGER           NOT NULL,
    observacao  VARCHAR(255),
    data_hora   TIMESTAMP         NOT NULL DEFAULT CURRENT_TIMESTAMP,  -- RN10
    CONSTRAINT ck_movimentacao_quantidade CHECK (quantidade > 0),   -- RN02
    CONSTRAINT fk_movimentacao_produto FOREIGN KEY (produto_id)
        REFERENCES produto (id) ON DELETE RESTRICT,                 -- RN07
    CONSTRAINT fk_movimentacao_usuario FOREIGN KEY (usuario_id)
        REFERENCES usuario (id) ON DELETE RESTRICT
);

CREATE INDEX idx_mov_produto_data ON movimentacao (produto_id, data_hora);  -- RF08
CREATE INDEX idx_mov_data         ON movimentacao (data_hora);              -- RF09
