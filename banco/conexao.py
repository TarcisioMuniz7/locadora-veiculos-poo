
import sqlite3
from pathlib import Path

CAMINHO_BANCO = Path(__file__).resolve().parent / "locadora.db"


def conectar():
    return sqlite3.connect(CAMINHO_BANCO)


def criar_tabelas():
    with conectar() as conexao:
        cursor = conexao.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT NOT NULL UNIQUE,
                telefone TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS veiculos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                placa TEXT NOT NULL UNIQUE,
                modelo TEXT NOT NULL,
                categoria TEXT NOT NULL,
                valor_diaria REAL NOT NULL,
                disponivel INTEGER DEFAULT 1
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS locacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                veiculo_id INTEGER NOT NULL,
                dias INTEGER NOT NULL,
                valor_total REAL NOT NULL,
                status TEXT DEFAULT 'Ativa',

                FOREIGN KEY (cliente_id)
                    REFERENCES clientes(id),

                FOREIGN KEY (veiculo_id)
                    REFERENCES veiculos(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL UNIQUE,
                senha_hash TEXT NOT NULL,
                sal TEXT NOT NULL
            )
        """)

        conexao.commit()

    from banco.usuario_dao import UsuarioDAO
    UsuarioDAO().criar_admin_padrao()


if __name__ == "__main__":
    criar_tabelas()
    print("Banco de dados criado com sucesso!")
