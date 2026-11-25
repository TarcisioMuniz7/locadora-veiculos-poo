
from pathlib import Path

import customtkinter as ctk

PASTA_IMAGENS = Path(__file__).resolve().parent.parent / "assets" / "imagens"
CAMINHO_LOGO = PASTA_IMAGENS / "logo.png"

FONTE = "Segoe UI"

COR_SIDEBAR = "#111827"
COR_SIDEBAR_ATIVO = "#1F2937"
COR_SIDEBAR_TEXTO = "#D1D5DB"
COR_SIDEBAR_SUAVE = "#6B7280"

COR_FUNDO_APP = "#F3F4F6"
COR_CARD = "#FFFFFF"
COR_CAMPO = "#F9FAFB"
COR_TEXTO = "#1F2937"
COR_SUAVE = "#6B7280"
COR_BORDA = "#E5E7EB"
COR_PRIMARIA = "#111827"
COR_PRIMARIA_HOVER = "#374151"
COR_ERRO = "#DC2626"

LARGURA_FORM = 312


def carregar_logo(largura):
    """Retorna a logo como CTkImage, ou None se não puder carregar."""
    try:
        from PIL import Image

        imagem = Image.open(CAMINHO_LOGO)
        # Remove a área transparente em volta da logo.
        imagem = imagem.crop(imagem.getbbox())
        altura = round(largura * imagem.height / imagem.width)

        return ctk.CTkImage(
            light_image=imagem, dark_image=imagem, size=(largura, altura)
        )
    except (ImportError, OSError):
        return None


def cabecalho(master, titulo, subtitulo):
    frame = ctk.CTkFrame(master, fg_color="transparent")
    frame.pack(fill="x", pady=(0, 24))

    ctk.CTkLabel(
        frame, text=titulo,
        font=(FONTE, 26, "bold"), text_color=COR_TEXTO
    ).pack(anchor="w")

    ctk.CTkLabel(
        frame, text=subtitulo,
        font=(FONTE, 13), text_color=COR_SUAVE
    ).pack(anchor="w")


def corpo_em_colunas(master):
    corpo = ctk.CTkFrame(master, fg_color="transparent")
    corpo.pack(fill="both", expand=True)
    corpo.grid_columnconfigure(1, weight=1)
    corpo.grid_rowconfigure(0, weight=1)
    return corpo


def card(master):
    return ctk.CTkFrame(
        master, fg_color=COR_CARD, corner_radius=12,
        border_width=1, border_color=COR_BORDA
    )


def titulo_card(master, texto):
    ctk.CTkLabel(
        master, text=texto,
        font=(FONTE, 15, "bold"), text_color=COR_TEXTO
    ).pack(anchor="w", padx=24, pady=(20, 16))


def rotulo(master, texto):
    ctk.CTkLabel(
        master, text=texto,
        font=(FONTE, 12), text_color=COR_SUAVE
    ).pack(anchor="w", padx=24)


def campo(master, texto, show=None, placeholder="", mascara=None,
          com_dica=False):
    rotulo(master, texto)

    entrada = ctk.CTkEntry(
        master, width=LARGURA_FORM, height=40, corner_radius=8,
        border_width=1, border_color=COR_BORDA,
        fg_color=COR_CAMPO, text_color=COR_TEXTO,
        placeholder_text=placeholder, placeholder_text_color="#9CA3AF",
        font=(FONTE, 13), show=show
    )
    entrada.pack(fill="x", padx=24, pady=(4, 2 if com_dica else 14))

    if com_dica:
        entrada.dica = dica(master)

    if mascara:
        aplicar_mascara(entrada, mascara)

    return entrada


def dica(master, texto=""):
    rotulo_dica = ctk.CTkLabel(
        master, text=texto, height=18,
        font=(FONTE, 11), text_color=COR_SUAVE
    )
    rotulo_dica.pack(anchor="w", padx=24, pady=(0, 10))
    return rotulo_dica


TECLAS_IGNORADAS = {
    "Left", "Right", "Up", "Down", "Home", "End", "Tab",
    "Shift_L", "Shift_R", "Control_L", "Control_R",
}


def aplicar_mascara(entrada, formatar, ao_mudar=None):
    """Reformata o texto do campo a cada tecla digitada."""

    def atualizar(evento=None):
        if evento is not None and evento.keysym in TECLAS_IGNORADAS:
            return

        texto = entrada.get()
        novo = formatar(texto)

        if novo != texto:
            entrada.delete(0, "end")
            entrada.insert(0, novo)
            entrada.icursor("end")

        if ao_mudar:
            ao_mudar(novo)

    entrada.bind("<KeyRelease>", atualizar, add="+")
    entrada.atualizar_mascara = atualizar


def limpar_campo(entrada):
    entrada.delete(0, "end")
    if hasattr(entrada, "atualizar_mascara"):
        entrada.atualizar_mascara()


def menu(master, texto, valores, comando=None):
    rotulo(master, texto)

    opcoes = ctk.CTkOptionMenu(
        master, values=valores, command=comando,
        width=LARGURA_FORM, height=40,
        corner_radius=8, dynamic_resizing=False,
        fg_color=COR_CAMPO, text_color=COR_TEXTO,
        button_color=COR_BORDA, button_hover_color="#D1D5DB",
        dropdown_fg_color=COR_CARD, dropdown_text_color=COR_TEXTO,
        dropdown_hover_color=COR_FUNDO_APP,
        font=(FONTE, 13), dropdown_font=(FONTE, 13)
    )
    opcoes.pack(fill="x", padx=24, pady=(4, 14))
    return opcoes


def seletor(master, texto, valores):
    rotulo(master, texto)

    botoes = ctk.CTkSegmentedButton(
        master, values=valores, height=40, corner_radius=8,
        fg_color=COR_BORDA, unselected_color=COR_BORDA,
        unselected_hover_color="#D1D5DB",
        selected_color=COR_CARD,
        selected_hover_color=COR_CARD,
        text_color=COR_TEXTO,
        font=(FONTE, 13, "bold")
    )
    botoes.pack(fill="x", padx=24, pady=(4, 14))
    botoes.set(valores[0])
    return botoes


def botao_primario(master, texto, comando):
    botao = ctk.CTkButton(
        master, text=texto, command=comando,
        width=LARGURA_FORM, height=42, corner_radius=8,
        fg_color=COR_PRIMARIA, hover_color=COR_PRIMARIA_HOVER,
        font=(FONTE, 14, "bold")
    )
    botao.pack(fill="x", padx=24, pady=(6, 24))
    return botao


def lista(master):
    caixa = ctk.CTkTextbox(
        master, fg_color=COR_CARD, text_color=COR_TEXTO,
        font=(FONTE, 13), border_width=0, wrap="word"
    )
    caixa.pack(fill="both", expand=True, padx=16, pady=(0, 16))
    caixa.configure(state="disabled")
    return caixa


def escrever_lista(caixa, texto):
    caixa.configure(state="normal")
    caixa.delete("1.0", "end")
    caixa.insert("end", texto)
    caixa.configure(state="disabled")
