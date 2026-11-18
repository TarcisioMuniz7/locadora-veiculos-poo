
class Veiculo:
    def __init__(self, placa, modelo, valor_diaria):
        self.placa = placa
        self.modelo = modelo
        self.valor_diaria = valor_diaria
        self.__disponivel = True

    @property
    def disponivel(self):
        return self.__disponivel

    def alugar(self):
        if not self.__disponivel:
            return False

        self.__disponivel = False
        return True

    def devolver(self):
        self.__disponivel = True

    def calcular_valor(self, dias):
        return self.valor_diaria * dias
