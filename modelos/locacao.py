
class Locacao:

    def __init__(self, cliente, veiculo, dias):
        if dias <= 0:
            raise ValueError("Quantidade de dias inválida.")

        if not veiculo.alugar():
            raise ValueError("Veículo indisponível.")

        self.cliente = cliente
        self.veiculo = veiculo
        self.dias = dias
        self.valor_total = veiculo.calcular_valor(dias)
        self.status = "Ativa"

    def finalizar(self):
        if self.status == "Finalizada":
            return False

        self.veiculo.devolver()
        self.status = "Finalizada"
        return True

    def exibir_resumo(self):
        return (
            f"Cliente: {self.cliente.nome}\n"
            f"Veículo: {self.veiculo.modelo}\n"
            f"Diárias: {self.dias}\n"
            f"Valor total: R$ {self.valor_total:.2f}\n"
            f"Status: {self.status}"
        )
