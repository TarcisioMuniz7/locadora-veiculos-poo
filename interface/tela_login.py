
import customtkinter as ctk

from banco.usuario_dao import UsuarioDAO
from interface import estilo

LARGURA = 460
ALTURA = 560


class TelaLogin(ctk.CTkToplevel):

    def __init__(self, master, ao_entrar):
        super().__init__(master)

        self.ao_entrar = ao_entrar
        self.dao = UsuarioDAO()

        self.title("Entrar")
        x = (self.winfo_screenwidth() - LARGURA) // 2
        y = (self.winfo_screenheight() - ALTURA) // 2
        self.geometry(f"{LARGURA}x{ALTURA}+{x}+{max(y - 30, 0)}")
        self.resizable(False, False)
        self.configure(fg_color=estilo.COR_CARD)

        self.protocol("WM_DELETE_WINDOW", master.destroy)

        conteudo = ctk.CTkFrame(self, fg_color="transparent")
        conteudo.pack(expand=True, fill="both", padx=48, pady=56)

        ctk.CTkLabel(
            conteudo,
            text="Locadora",
            font=(estilo.FONTE, 30, "bold"),
            text_color=estilo.COR_TEXTO
        ).pack(anchor="w")

        ctk.CTkLabel(
            conteudo,
            text="Entre para continuar",
            font=(estilo.FONTE, 14),
            text_color=estilo.COR_SUAVE
        ).pack(anchor="w", pady=(0, 40))

        self.entrada_usuario = self._criar_campo(conteudo, "Usuário")
        self.entrada_senha = self._criar_campo(conteudo, "Senha", show="•")

        self.mensagem_erro = ctk.CTkLabel(
            conteudo,
            text="",
            font=(estilo.FONTE, 12),
            text_color=estilo.COR_ERRO
        )
        self.mensagem_erro.pack(anchor="w", pady=(0, 10))

        ctk.CTkButton(
            conteudo,
            text="Entrar",
            height=46,
            corner_radius=8,
            font=(estilo.FONTE, 15, "bold"),
            fg_color=estilo.COR_PRIMARIA,
            hover_color=estilo.COR_PRIMARIA_HOVER,
            command=self.entrar
        ).pack(fill="x")

        self.bind("<Return>", lambda _evento: self.entrar())

        # No Windows, a janela pode abrir atrás de outras.
        self.after(150, self._trazer_para_frente)

    def _criar_campo(self, master, rotulo, show=None):
        ctk.CTkLabel(
            master,
            text=rotulo,
            font=(estilo.FONTE, 13),
            text_color=estilo.COR_SUAVE
        ).pack(anchor="w")

        campo = ctk.CTkEntry(
            master,
            height=44,
            corner_radius=8,
            border_width=1,
            border_color=estilo.COR_BORDA,
            fg_color=estilo.COR_CAMPO,
            text_color=estilo.COR_TEXTO,
            font=(estilo.FONTE, 14),
            show=show
        )
        campo.pack(fill="x", pady=(4, 18))
        campo.bind("<Key>", lambda _evento: self._limpar_erro())
        return campo

    def _trazer_para_frente(self):
        self.lift()
        self.focus_force()
        self.entrada_usuario.focus()

    def _limpar_erro(self):
        self.mensagem_erro.configure(text="")
        self.entrada_usuario.configure(border_color=estilo.COR_BORDA)
        self.entrada_senha.configure(border_color=estilo.COR_BORDA)

    def _mostrar_erro(self, texto):
        self.mensagem_erro.configure(text=texto)
        self.entrada_usuario.configure(border_color=estilo.COR_ERRO)
        self.entrada_senha.configure(border_color=estilo.COR_ERRO)

    def entrar(self):
        usuario = self.entrada_usuario.get().strip()
        senha = self.entrada_senha.get()

        if not usuario or not senha:
            self._mostrar_erro("Preencha usuário e senha.")
            return

        if not self.dao.autenticar(usuario, senha):
            self._mostrar_erro("Usuário ou senha incorretos.")
            self.entrada_senha.delete(0, "end")
            self.entrada_senha.focus()
            return

        self.destroy()
        self.ao_entrar()
