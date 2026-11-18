
from modelos.categorias import CarroEconomico, CarroSUV

economico = CarroEconomico("ABC1234", "Fiat Mobi", 100)
suv = CarroSUV("XYZ5678", "Jeep Compass", 200)

print("=== TESTE DE VEÍCULOS ===")

print("Econômico:", economico.modelo)
print("Valor de 3 dias: R$", economico.calcular_valor(3))

print("SUV:", suv.modelo)
print("Valor de 3 dias: R$", suv.calcular_valor(3))

print("Disponível:", economico.disponivel)

economico.alugar()
print("Após locação:", economico.disponivel)

economico.devolver()
print("Após devolução:", economico.disponivel)
