
from banco.conexao import conectar


class LocacaoDAO:

    def listar_clientes(self):
        with conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("""
                SELECT id, nome, cpf
                FROM clientes
                ORDER BY nome
            """)
            return cursor.fetchall()

    def listar_veiculos_disponiveis(self):
        with conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("""
                SELECT id, placa, modelo, categoria, valor_diaria
                FROM veiculos
                WHERE disponivel = 1
                ORDER BY modelo
            """)
            return cursor.fetchall()

    def registrar_locacao(self, cliente_id, veiculo_id, dias):
        if dias <= 0:
            raise ValueError("A quantidade de diárias deve ser positiva.")

        with conectar() as conexao:
            conexao.execute("BEGIN IMMEDIATE")
            cursor = conexao.cursor()

            cursor.execute(
                "SELECT id FROM clientes WHERE id = ?",
                (cliente_id,)
            )
            if cursor.fetchone() is None:
                raise ValueError("Cliente não encontrado.")

            cursor.execute("""
                SELECT categoria, valor_diaria
                FROM veiculos
                WHERE id = ? AND disponivel = 1
            """, (veiculo_id,))

            veiculo = cursor.fetchone()

            if veiculo is None:
                raise ValueError("Veículo indisponível ou não encontrado.")

            categoria, valor_diaria = veiculo

            from modelos.categorias import criar_veiculo

            objeto_veiculo = criar_veiculo(
                categoria, "", "", valor_diaria
            )

            valor_total = objeto_veiculo.calcular_valor(dias)

            cursor.execute("""
                INSERT INTO locacoes
                (cliente_id, veiculo_id, dias, valor_total, status)
                VALUES (?, ?, ?, ?, 'Ativa')
            """, (cliente_id, veiculo_id, dias, valor_total))

            locacao_id = cursor.lastrowid

            cursor.execute("""
                UPDATE veiculos
                SET disponivel = 0
                WHERE id = ? AND disponivel = 1
            """, (veiculo_id,))

            if cursor.rowcount != 1:
                raise ValueError("Não foi possível reservar o veículo.")

            conexao.commit()
            return locacao_id, valor_total

    def listar_locacoes(self):
        with conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("""
                SELECT
                    l.id,
                    c.nome,
                    v.modelo,
                    v.placa,
                    l.dias,
                    l.valor_total,
                    l.status
                FROM locacoes l
                INNER JOIN clientes c ON c.id = l.cliente_id
                INNER JOIN veiculos v ON v.id = l.veiculo_id
                ORDER BY l.id DESC
            """)
            return cursor.fetchall()

    def finalizar_locacao(self, locacao_id):
        with conectar() as conexao:
            conexao.execute("BEGIN IMMEDIATE")
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT veiculo_id
                FROM locacoes
                WHERE id = ? AND status = 'Ativa'
            """, (locacao_id,))

            resultado = cursor.fetchone()

            if resultado is None:
                raise ValueError("Locação ativa não encontrada.")

            veiculo_id = resultado[0]

            cursor.execute("""
                UPDATE locacoes
                SET status = 'Finalizada'
                WHERE id = ? AND status = 'Ativa'
            """, (locacao_id,))

            cursor.execute("""
                UPDATE veiculos
                SET disponivel = 1
                WHERE id = ?
            """, (veiculo_id,))

            conexao.commit()
            return True
