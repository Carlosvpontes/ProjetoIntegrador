-- =====================================================================
-- EstoqueFácil: projeto físico do banco de dados
-- SGBD: MySQL 8.0+ (InnoDB, utf8mb4)
-- Documentação: docs/situacao-1/04-banco-de-dados.md
--
-- Uso: selecione o banco de dados e execute este script.
--   Ex. (PythonAnywhere): USE `carlosvpontes$estoque`;
-- =====================================================================

SET NAMES utf8mb4;

-- Remove as tabelas na ordem inversa das dependências (permite recriar do zero)
DROP TABLE IF EXISTS movimentacao;
DROP TABLE IF EXISTS produto;
DROP TABLE IF EXISTS fornecedor;
DROP TABLE IF EXISTS categoria;
DROP TABLE IF EXISTS usuario;

-- ---------------------------------------------------------------------
-- usuario: pessoas que acessam o sistema
-- ---------------------------------------------------------------------
CREATE TABLE usuario (
    id          INT UNSIGNED NOT NULL AUTO_INCREMENT,
    nome        VARCHAR(100) NOT NULL,
    email       VARCHAR(120) NOT NULL,
    senha_hash  VARCHAR(255) NOT NULL,
    criado_em   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_usuario       PRIMARY KEY (id),
    CONSTRAINT uk_usuario_email UNIQUE (email)                      -- RN08
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------------------------------------------------
-- categoria: agrupamento de produtos
-- ---------------------------------------------------------------------
CREATE TABLE categoria (
    id          INT UNSIGNED NOT NULL AUTO_INCREMENT,
    nome        VARCHAR(60)  NOT NULL,
    descricao   VARCHAR(255) NULL,
    CONSTRAINT pk_categoria      PRIMARY KEY (id),
    CONSTRAINT uk_categoria_nome UNIQUE (nome)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------------------------------------------------
-- fornecedor: empresas que fornecem produtos
-- ---------------------------------------------------------------------
CREATE TABLE fornecedor (
    id          INT UNSIGNED NOT NULL AUTO_INCREMENT,
    nome        VARCHAR(100) NOT NULL,
    cnpj        CHAR(14)     NULL,
    telefone    VARCHAR(20)  NULL,
    email       VARCHAR(120) NULL,
    CONSTRAINT pk_fornecedor      PRIMARY KEY (id),
    CONSTRAINT uk_fornecedor_cnpj UNIQUE (cnpj),
    CONSTRAINT ck_fornecedor_cnpj CHECK (cnpj IS NULL OR cnpj REGEXP '^[0-9]{14}$')
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------------------------------------------------
-- produto: itens controlados no estoque
-- ---------------------------------------------------------------------
CREATE TABLE produto (
    id                INT UNSIGNED  NOT NULL AUTO_INCREMENT,
    codigo            VARCHAR(30)   NOT NULL,
    nome              VARCHAR(100)  NOT NULL,
    descricao         VARCHAR(255)  NULL,
    categoria_id      INT UNSIGNED  NOT NULL,
    fornecedor_id     INT UNSIGNED  NULL,
    preco_custo       DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    preco_venda       DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    estoque_minimo    INT UNSIGNED  NOT NULL DEFAULT 0,
    quantidade_atual  INT UNSIGNED  NOT NULL DEFAULT 0,             -- RN03: só muda via movimentação
    criado_em         DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em     DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT pk_produto             PRIMARY KEY (id),
    CONSTRAINT uk_produto_codigo      UNIQUE (codigo),              -- RN05
    CONSTRAINT ck_produto_preco_custo CHECK (preco_custo >= 0),     -- RN12
    CONSTRAINT ck_produto_preco_venda CHECK (preco_venda >= 0),     -- RN12
    CONSTRAINT fk_produto_categoria   FOREIGN KEY (categoria_id)
        REFERENCES categoria (id) ON DELETE RESTRICT ON UPDATE CASCADE,   -- RN06
    CONSTRAINT fk_produto_fornecedor  FOREIGN KEY (fornecedor_id)
        REFERENCES fornecedor (id) ON DELETE RESTRICT ON UPDATE CASCADE   -- RN06
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_produto_nome ON produto (nome);                    -- RF10

-- ---------------------------------------------------------------------
-- movimentacao: entradas e saídas de mercadoria (registros imutáveis, RN11)
-- ---------------------------------------------------------------------
CREATE TABLE movimentacao (
    id          INT UNSIGNED NOT NULL AUTO_INCREMENT,
    produto_id  INT UNSIGNED NOT NULL,
    usuario_id  INT UNSIGNED NOT NULL,
    tipo        ENUM('ENTRADA', 'SAIDA') NOT NULL,
    quantidade  INT UNSIGNED NOT NULL,
    observacao  VARCHAR(255) NULL,
    data_hora   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,    -- RN10
    CONSTRAINT pk_movimentacao            PRIMARY KEY (id),
    CONSTRAINT ck_movimentacao_quantidade CHECK (quantidade > 0),   -- RN02
    CONSTRAINT fk_movimentacao_produto    FOREIGN KEY (produto_id)
        REFERENCES produto (id) ON DELETE RESTRICT ON UPDATE CASCADE,     -- RN07
    CONSTRAINT fk_movimentacao_usuario    FOREIGN KEY (usuario_id)
        REFERENCES usuario (id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_mov_produto_data ON movimentacao (produto_id, data_hora);  -- RF08
CREATE INDEX idx_mov_data         ON movimentacao (data_hora);              -- RF09
