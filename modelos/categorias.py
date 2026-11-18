
from modelos.veiculo import Veiculo


class CarroEconomico(Veiculo):

    def calcular_valor(self, dias):
        if dias <= 0:
            raise ValueError("A quantidade de dias deve ser positiva.")

        return self.valor_diaria * dias


class CarroSUV(Veiculo):

    def calcular_valor(self, dias):
        if dias <= 0:
            raise ValueError("A quantidade de dias deve ser positiva.")

        return self.valor_diaria * dias * 1.10
