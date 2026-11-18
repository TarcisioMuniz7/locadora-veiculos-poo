
from modelos.cliente import Cliente
from banco.cliente_dao import ClienteDAO
from banco.conexao import criar_tabelas

criar_tabelas()

dao = ClienteDAO()

cliente = Cliente(
    "Maria Oliveira",
    "98765432100",
    "71988887777"
)

dao.cadastrar(cliente)

print("=== CLIENTE CADASTRADO ===")

for registro in dao.listar():
    print(registro)
