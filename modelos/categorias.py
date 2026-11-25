
from modelos.veiculo import Veiculo


def _validar_dias(dias):
    if dias <= 0:
        raise ValueError("A quantidade de dias deve ser positiva.")


class CarroEconomico(Veiculo):
    """Hatches compactos. Ex.: Fiat Mobi, Renault Kwid."""

    def calcular_valor(self, dias):
        _validar_dias(dias)
        return self.valor_diaria * dias


class CarroSedan(Veiculo):
    """Sedãs. Ex.: Toyota Corolla, Honda Civic."""

    def calcular_valor(self, dias):
        _validar_dias(dias)
        return round(self.valor_diaria * dias * 1.05, 2)


class CarroSUV(Veiculo):
    """Utilitários esportivos. Ex.: Jeep Compass, Hyundai Creta."""

    def calcular_valor(self, dias):
        _validar_dias(dias)
        return round(self.valor_diaria * dias * 1.10, 2)


class CarroPicape(Veiculo):
    """Picapes. Ex.: Toyota Hilux, Fiat Toro."""

    def calcular_valor(self, dias):
        _validar_dias(dias)
        return round(self.valor_diaria * dias * 1.15, 2)


# Nome exibido na tela -> (classe, descrição do cálculo)
CATEGORIAS = {
    "Econômico": (CarroEconomico, "Sem acréscimo. Ex.: Mobi, Kwid."),
    "Sedan": (CarroSedan, "Acréscimo de 5%. Ex.: Corolla, Civic."),
    "SUV": (CarroSUV, "Acréscimo de 10%. Ex.: Compass, Creta."),
    "Picape": (CarroPicape, "Acréscimo de 15%. Ex.: Hilux, Toro."),
}


def criar_veiculo(categoria, placa, modelo, valor_diaria):
    if categoria not in CATEGORIAS:
        raise ValueError(f"Categoria desconhecida: {categoria}")

    classe, _descricao = CATEGORIAS[categoria]
    return classe(placa, modelo, valor_diaria)
