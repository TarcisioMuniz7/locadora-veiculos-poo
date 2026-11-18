
import customtkinter as ctk
from tkinter import messagebox

from banco.locacao_dao import LocacaoDAO


class TelaLocacoes(ctk.CTkToplevel):

    def __init__(self, master):
        super().__init__(master)

        self.title("Gerenciamento de Locações")
        self.geometry("650x650")

        self.dao = LocacaoDAO()
        self.clientes = {}
        self.veiculos = {}

        ctk.CTkLabel(
            self,
            text="Gerenciamento de Locações",
            font=("Arial", 22, "bold")
        ).pack(pady=15)

        ctk.CTkLabel(
            self,
            text="Selecione o cliente"
        ).pack(pady=5)

        self.menu_clientes = ctk.CTkOptionMenu(
            self,
            values=["Nenhum cliente"],
            width=400
        )
        self.menu_clientes.pack(pady=5)

        ctk.CTkLabel(
            self,
            text="Selecione o veículo disponível"
        ).pack(pady=5)

        self.menu_veiculos = ctk.CTkOptionMenu(
            self,
            values=["Nenhum veículo disponível"],
            width=400
        )
        self.menu_veiculos.pack(pady=5)

        self.entrada_dias = ctk.CTkEntry(
            self,
            placeholder_text="Quantidade de diárias",
            width=400
        )
        self.entrada_dias.pack(pady=15)

        ctk.CTkButton(
            self,
            text="Registrar Locação",
            width=250,
            command=self.registrar_locacao
        ).pack(pady=5)

        ctk.CTkButton(
            self,
            text="Atualizar Dados",
            width=250,
            command=self.atualizar_dados
        ).pack(pady=5)

        ctk.CTkLabel(
            self,
            text="Histórico de Locações",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        self.resultado = ctk.CTkTextbox(
            self,
            width=550,
            height=150
        )
        self.resultado.pack(pady=5)

        self.entrada_id = ctk.CTkEntry(
            self,
            placeholder_text="ID da locação para finalizar",
            width=300
        )
        self.entrada_id.pack(pady=10)

        ctk.CTkButton(
            self,
            text="Finalizar Locação",
            width=250,
            command=self.finalizar_locacao
        ).pack(pady=5)

        self.atualizar_dados()

    def atualizar_dados(self):
        self.clientes = {}
        self.veiculos = {}

        for id_cliente, nome, cpf in self.dao.listar_clientes():
            texto = f"{id_cliente} - {nome} ({cpf})"
            self.clientes[texto] = id_cliente

        for registro in self.dao.listar_veiculos_disponiveis():
            id_veiculo, placa, modelo, categoria, valor = registro
            texto = f"{id_veiculo} - {modelo} ({placa})"
            self.veiculos[texto] = id_veiculo

        self.menu_clientes.configure(
            values=list(self.clientes) or ["Nenhum cliente"]
        )
        self.menu_clientes.set(
            next(iter(self.clientes), "Nenhum cliente")
        )

        self.menu_veiculos.configure(
            values=list(self.veiculos) or ["Nenhum veículo disponível"]
        )
        self.menu_veiculos.set(
            next(iter(self.veiculos), "Nenhum veículo disponível")
        )

        self.listar_locacoes()

    def registrar_locacao(self):
        try:
            cliente = self.menu_clientes.get()
            veiculo = self.menu_veiculos.get()

            if cliente not in self.clientes:
                raise ValueError("Cadastre um cliente primeiro.")

            if veiculo not in self.veiculos:
                raise ValueError("Não há veículos disponíveis.")

            dias = int(self.entrada_dias.get().strip())

            locacao_id, valor = self.dao.registrar_locacao(
                self.clientes[cliente],
                self.veiculos[veiculo],
                dias
            )

            messagebox.showinfo(
                "Locação registrada",
                f"Locação nº {locacao_id} registrada!\n"
                f"Valor total: R$ {valor:.2f}"
            )

            self.entrada_dias.delete(0, "end")
            self.atualizar_dados()

        except ValueError as erro:
            messagebox.showerror("Erro", str(erro))
            self.atualizar_dados()

    def listar_locacoes(self):
        self.resultado.delete("1.0", "end")

        locacoes = self.dao.listar_locacoes()

        if not locacoes:
            self.resultado.insert(
                "end", "Nenhuma locação cadastrada."
            )
            return

        for registro in locacoes:
            id_locacao, cliente, modelo, placa, dias, valor, status = registro

            self.resultado.insert(
                "end",
                f"ID: {id_locacao} | {status}\n"
                f"Cliente: {cliente}\n"
                f"Veículo: {modelo} - {placa}\n"
                f"Diárias: {dias} | Total: R$ {valor:.2f}\n\n"
            )

    def finalizar_locacao(self):
        try:
            locacao_id = int(self.entrada_id.get().strip())

            self.dao.finalizar_locacao(locacao_id)

            messagebox.showinfo(
                "Sucesso",
                "Locação finalizada! Veículo disponível novamente."
            )

            self.entrada_id.delete(0, "end")
            self.atualizar_dados()

        except ValueError as erro:
            messagebox.showerror("Erro", str(erro))
