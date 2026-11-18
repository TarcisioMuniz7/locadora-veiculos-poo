
from banco.conexao import conectar, criar_tabelas


class ClienteDAO:

    def cadastrar(self, cliente):
        with conectar() as conexao:
            cursor = conexao.cursor()

            cursor.execute("""
                INSERT INTO clientes (nome, cpf, telefone)
                VALUES (?, ?, ?)
            """, (
                cliente.nome,
                cliente.cpf,
                cliente.telefone
            ))

            return cursor.lastrowid

    def listar(self):
        with conectar() as conexao:
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT id, nome, cpf, telefone
                FROM clientes
                ORDER BY nome
            """)

            return cursor.fetchall()
