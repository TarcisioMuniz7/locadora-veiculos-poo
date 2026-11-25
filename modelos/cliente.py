
from modelos.validacoes import (
    validar_cpf, validar_telefone, formatar_cpf, formatar_telefone
)


class Cliente:

    def __init__(self, nome, cpf, telefone):
        nome = (nome or "").strip()

        if len(nome) < 3:
            raise ValueError("Informe o nome completo do cliente.")

        self.nome = nome
        self.__cpf = validar_cpf(cpf)
        self.telefone = validar_telefone(telefone)

    @property
    def cpf(self):
        return self.__cpf

    def exibir_dados(self):
        return (
            f"Nome: {self.nome}\n"
            f"CPF: {formatar_cpf(self.cpf)}\n"
            f"Telefone: {formatar_telefone(self.telefone)}"
        )
