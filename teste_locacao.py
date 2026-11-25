
from modelos.cliente import Cliente
from modelos.categorias import CarroEconomico
from modelos.locacao import Locacao

cliente = Cliente("João Silva", "12345678909", "71999999999")
veiculo = CarroEconomico("ABC1234", "Fiat Mobi", 100)

locacao = Locacao(cliente, veiculo, 3)

print("=== LOCAÇÃO REALIZADA ===")
print(locacao.exibir_resumo())
print("Disponível:", veiculo.disponivel)

locacao.finalizar()

print("\n=== DEVOLUÇÃO ===")
print(locacao.exibir_resumo())
print("Disponível:", veiculo.disponivel)
