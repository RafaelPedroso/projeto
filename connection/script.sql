-- Active: 1718481116508@@127.0.0.1@3306
-- Active: 1717801157945@@127.0.0.1@3306
PRAGMA foreign_keys = ON;

CREATE TABLE cidade(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    nome TEXT NOT NULL,
    estado VARCHAR(2) NOT NULL
)

CREATE TABLE fabricante(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    nome TEXT NOT NULL,
    site TEXT
)

CREATE TABLE cliente(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    nome TEXT NOT NULL,
    endereco TEXT NOT NULL,
    telefone TEXT NOT NULL,
    email TEXT,
    id_cidade INTEGER NOT NULL,
    Foreign Key (id_cidade) REFERENCES cidade(id)
)

CREATE TABLE produto(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    descricao TEXT NOT NULL,
    estoque FLOAT NOT NULL,
    preco_compra FLOAT NOT NULL,
    preco_venda FLOAT NOT NULL,
    marca TEXT,
    id_fabricante INTEGER NOT NULL,
    Foreign Key (id_fabricante) REFERENCES fabricante(id)
)

CREATE TABLE venda(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    data DATE NOT NULL,
    valor_total FLOAT NOT NULL,
    valor_pago FLOAT NOT NULL,
    desconto FLOAT NOT NULL,
    id_cliente INTEGER NOT NULL,
    Foreign Key (id_cliente) REFERENCES cliente(id)
)

CREATE TABLE item_venda(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    quantidade FLOAT NOT NULL,
    id_produto INTEGER NOT NULL,
    id_venda INTEGER NOT NULL,
    Foreign Key (id_produto) REFERENCES produto(id),
    Foreign Key (id_venda) REFERENCES venda(id)
)

CREATE TABLE fornecedor(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    nome TEXT NOT NULL,
    endereco TEXT NOT NULL,
    telefone TEXT NOT NULL,
    email TEXT,
    id_cidade NOT NULL,
    Foreign Key (id_cidade) REFERENCES cidade(id)
)

CREATE TABLE compra(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    data DATE NOT NULL,
    valor_total FLOAT NOT NULL,
    valor_pago FLOAT NOT NULL,
    desconto FLOAT NOT NULL,
    id_fornecedor INTEGER NOT NULL,
    Foreign Key (id_fornecedor) REFERENCES fornecedor(id)
)

CREATE TABLE item_compra(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    quantidade FLOAT NOT NULL,
    valor_total FLOAT NOT NULL,
    id_produto INTEGER NOT NULL,
    id_compra INTEGER NOT NULL,
    Foreign Key (id_produto) REFERENCES produto(id),
    Foreign Key (id_compra) REFERENCES compra(id)
)