
import customtkinter as ctk

from interface import estilo
from interface.tela_clientes import TelaClientes
from interface.tela_veiculos import TelaVeiculos
from interface.tela_locacoes import TelaLocacoes
from interface.tela_login import TelaLogin
from banco.conexao import criar_tabelas


def centralizar(janela, largura, altura):
    x = (janela.winfo_screenwidth() - largura) // 2
    y = (janela.winfo_screenheight() - altura) // 2
    janela.geometry(f"{largura}x{altura}+{x}+{max(y - 30, 0)}")


class SistemaLocadora(ctk.CTk):

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("light")

        self.title("Sistema de Locadora de Veículos")
        centralizar(self, 1200, 760)
        self.minsize(1000, 660)
        self.configure(fg_color=estilo.COR_FUNDO_APP)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._criar_sidebar()

        area = ctk.CTkFrame(
            self, fg_color=estilo.COR_FUNDO_APP, corner_radius=0
        )
        area.grid(row=0, column=1, sticky="nsew")

        self.paginas = {
            "Veículos": TelaVeiculos(area),
            "Clientes": TelaClientes(area),
            "Locações": TelaLocacoes(area),
        }

        self.botoes_menu = {}
        for nome in self.paginas:
            self.botoes_menu[nome] = self._botao_menu(nome)

        self.mostrar("Veículos")

    def _criar_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self, width=240, corner_radius=0,
            fg_color=estilo.COR_SIDEBAR
        )
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.pack_propagate(False)

        self.logo = estilo.carregar_logo(largura=192)

        if self.logo:
            ctk.CTkLabel(
                self.sidebar, text="", image=self.logo
            ).pack(anchor="w", padx=24, pady=(32, 32))
        else:
            # Se a imagem não carregar, mostra o nome em texto.
            ctk.CTkLabel(
                self.sidebar, text="Locadora TM",
                font=(estilo.FONTE, 22, "bold"), text_color="#FFFFFF"
            ).pack(anchor="w", padx=24, pady=(32, 32))

        ctk.CTkLabel(
            self.sidebar, text="MENU",
            font=(estilo.FONTE, 11, "bold"),
            text_color=estilo.COR_SIDEBAR_SUAVE
        ).pack(anchor="w", padx=24, pady=(0, 8))

        ctk.CTkButton(
            self.sidebar, text="Sair", anchor="w", height=40,
            corner_radius=8, fg_color="transparent",
            hover_color=estilo.COR_SIDEBAR_ATIVO,
            text_color=estilo.COR_SIDEBAR_SUAVE,
            font=(estilo.FONTE, 14), command=self.sair
        ).pack(side="bottom", fill="x", padx=12, pady=24)

    def _botao_menu(self, nome):
        botao = ctk.CTkButton(
            self.sidebar, text=nome, anchor="w", height=42,
            corner_radius=8, fg_color="transparent",
            hover_color=estilo.COR_SIDEBAR_ATIVO,
            text_color=estilo.COR_SIDEBAR_TEXTO,
            font=(estilo.FONTE, 14),
            command=lambda: self.mostrar(nome)
        )
        botao.pack(fill="x", padx=12, pady=2)
        return botao

    def mostrar(self, nome):
        for pagina in self.paginas.values():
            pagina.pack_forget()

        pagina = self.paginas[nome]
        pagina.pack(fill="both", expand=True, padx=40, pady=36)
        pagina.ao_mostrar()

        for nome_botao, botao in self.botoes_menu.items():
            ativo = nome_botao == nome
            botao.configure(
                fg_color=estilo.COR_SIDEBAR_ATIVO if ativo else "transparent",
                text_color="#FFFFFF" if ativo else estilo.COR_SIDEBAR_TEXTO,
                font=(estilo.FONTE, 14, "bold" if ativo else "normal")
            )

    def sair(self):
        self.withdraw()
        TelaLogin(self, ao_entrar=self.entrar)

    def entrar(self):
        self.mostrar("Veículos")
        self.deiconify()


if __name__ == "__main__":
    criar_tabelas()
    app = SistemaLocadora()
    app.withdraw()
    TelaLogin(app, ao_entrar=app.deiconify)
    app.mainloop()
