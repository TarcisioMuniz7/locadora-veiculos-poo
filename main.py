
import customtkinter as ctk


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

        botao_veiculos = ctk.CTkButton(
            self,
            text="Gerenciar Veículos",
            width=220
        )
        botao_veiculos.pack(pady=10)

        botao_clientes = ctk.CTkButton(
            self,
            text="Gerenciar Clientes",
            width=220
        )
        botao_clientes.pack(pady=10)

        botao_locacoes = ctk.CTkButton(
            self,
            text="Gerenciar Locações",
            width=220
        )
        botao_locacoes.pack(pady=10)


if __name__ == "__main__":
    app = SistemaLocadora()
    app.mainloop()
