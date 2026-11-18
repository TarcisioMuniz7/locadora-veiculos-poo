
class Cliente:

    def __init__(self, nome, cpf, telefone):
        self.nome = nome
        self.__cpf = cpf
        self.telefone = telefone

    @property
    def cpf(self):
        return self.__cpf

    def exibir_dados(self):
        return (
            f"Nome: {self.nome}\n"
            f"CPF: {self.cpf}\n"
            f"Telefone: {self.telefone}"
        )
