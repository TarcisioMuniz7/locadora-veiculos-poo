
import customtkinter as ctk

from interface.tela_clientes import TelaClientes
from interface.tela_veiculos import TelaVeiculos
from interface.tela_locacoes import TelaLocacoes
from banco.conexao import criar_tabelas


class SistemaLocadora(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Sistema de Locadora de Veículos")
        self.geometry("500x400")
        self.resizable(False, False)

        ctk.set_appearance_mode("light")

        titulo = ctk.CTkLabel(
            self,
            text="Sistema de Locadora de Veículos",
            font=("Arial", 20, "bold")
        )
        titulo.pack(pady=30)

        ctk.CTkButton(
            self,
            text="Gerenciar Veículos",
            width=220,
            command=self.abrir_veiculos
        ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Gerenciar Clientes",
            width=220,
            command=self.abrir_clientes
        ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Gerenciar Locações",
            width=220,
            command=self.abrir_locacoes
        ).pack(pady=10)

    def abrir_veiculos(self):
        TelaVeiculos(self)

    def abrir_clientes(self):
        TelaClientes(self)

    def abrir_locacoes(self):
        TelaLocacoes(self)


if __name__ == "__main__":
    criar_tabelas()
    app = SistemaLocadora()
    app.mainloop()
