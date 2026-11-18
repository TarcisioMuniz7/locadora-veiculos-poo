
from banco.conexao import conectar


class VeiculoDAO:

    def cadastrar(self, veiculo, categoria):
        with conectar() as conexao:
            cursor = conexao.cursor()

            cursor.execute("""
                INSERT INTO veiculos
                (placa, modelo, categoria, valor_diaria, disponivel)
                VALUES (?, ?, ?, ?, ?)
            """, (
                veiculo.placa,
                veiculo.modelo,
                categoria,
                veiculo.valor_diaria,
                int(veiculo.disponivel)
            ))

            return cursor.lastrowid

    def listar(self):
        with conectar() as conexao:
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT id, placa, modelo, categoria,
                       valor_diaria, disponivel
                FROM veiculos
                ORDER BY modelo
            """)

            return cursor.fetchall()
