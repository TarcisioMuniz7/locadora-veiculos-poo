
from modelos.cliente import Cliente

cliente1 = Cliente(
    "João Silva",
    "12345678900",
    "71999999999"
)

print("=== CLIENTE CADASTRADO ===")
print(cliente1.exibir_dados())
