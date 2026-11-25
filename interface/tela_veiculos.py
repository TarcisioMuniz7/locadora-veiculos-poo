
import customtkinter as ctk
import sqlite3

from tkinter import messagebox
from banco.veiculo_dao import VeiculoDAO
from modelos.categorias import CATEGORIAS, criar_veiculo
from modelos.validacoes import (
    validar_placa, tipo_placa, formatar_placa, mascara_placa,
    normalizar_placa
)
from interface import estilo

DICA_PLACA = "Mercosul (ABC1D23) ou modelo antigo (ABC-1234)."


class TelaVeiculos(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.dao = VeiculoDAO()

        estilo.cabecalho(
            self, "Veículos", "Cadastre e acompanhe a frota da locadora."
        )

        corpo = estilo.corpo_em_colunas(self)

        formulario = estilo.card(corpo)
        formulario.grid(row=0, column=0, sticky="n", padx=(0, 24))

        estilo.titulo_card(formulario, "Novo veículo")
        self.entrada_placa = estilo.campo(
            formulario, "Placa", placeholder="ABC1D23", com_dica=True
        )
        estilo.aplicar_mascara(
            self.entrada_placa, mascara_placa,
            ao_mudar=self._mostrar_tipo_placa
        )
        self._mostrar_tipo_placa("")

        self.entrada_modelo = estilo.campo(
            formulario, "Modelo", placeholder="Ex.: Toyota Corolla"
        )

        self.categoria = estilo.menu(
            formulario, "Categoria", list(CATEGORIAS),
            comando=self._mostrar_descricao_categoria
        )
        self.categoria.pack_configure(pady=(4, 2))
        self.dica_categoria = estilo.dica(formulario)
        self._mostrar_descricao_categoria(self.categoria.get())

        self.entrada_valor = estilo.campo(
            formulario, "Valor da diária (R$)", placeholder="Ex.: 150,00"
        )
        estilo.botao_primario(
            formulario, "Cadastrar veículo", self.cadastrar_veiculo
        )

        painel_lista = estilo.card(corpo)
        painel_lista.grid(row=0, column=1, sticky="nsew")

        estilo.titulo_card(painel_lista, "Frota")
        self.resultado = estilo.lista(painel_lista)

    def ao_mostrar(self):
        self.listar_veiculos()

    def _mostrar_tipo_placa(self, texto):
        placa = normalizar_placa(texto)
        tipo = tipo_placa(placa)

        if tipo == "Mercosul":
            mensagem, cor = "✓ Placa padrão Mercosul", "#059669"
        elif tipo == "Antiga":
            mensagem, cor = "✓ Placa modelo antigo", "#059669"
        elif len(placa) == 7:
            mensagem, cor = "Formato de placa inválido", estilo.COR_ERRO
        else:
            mensagem, cor = DICA_PLACA, estilo.COR_SUAVE

        self.entrada_placa.dica.configure(text=mensagem, text_color=cor)

    def _mostrar_descricao_categoria(self, categoria):
        _classe, descricao = CATEGORIAS[categoria]
        self.dica_categoria.configure(text=descricao)

    def cadastrar_veiculo(self):
        modelo = self.entrada_modelo.get().strip()
        categoria = self.categoria.get()

        try:
            placa = validar_placa(self.entrada_placa.get())

            if not modelo:
                raise ValueError("Informe o modelo do veículo.")

            try:
                valor = float(
                    self.entrada_valor.get().strip().replace(",", ".")
                )
            except ValueError:
                raise ValueError(
                    "Informe um valor de diária válido. Ex.: 150,00"
                ) from None

            if valor <= 0:
                raise ValueError(
                    "O valor da diária deve ser positivo."
                )

            veiculo = criar_veiculo(categoria, placa, modelo, valor)

            self.dao.cadastrar(veiculo, categoria)

            messagebox.showinfo(
                "Sucesso", "Veículo cadastrado!"
            )

            estilo.limpar_campo(self.entrada_placa)
            self.entrada_modelo.delete(0, "end")
            self.entrada_valor.delete(0, "end")

            self.listar_veiculos()

        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Erro", "Placa já cadastrada!"
            )

        except ValueError as erro:
            messagebox.showerror("Erro", str(erro))

    def listar_veiculos(self):
        linhas = []

        for registro in self.dao.listar():
            id_veiculo, placa, modelo, categoria, valor, disponivel = registro

            status = "Disponível" if disponivel else "Alugado"
            tipo = tipo_placa(placa)
            tipo_texto = f" ({tipo})" if tipo else ""

            linhas.append(
                f"#{id_veiculo}  {modelo}  ·  {status}\n"
                f"Placa {formatar_placa(placa)}{tipo_texto}  ·  "
                f"{categoria}  ·  R$ {valor:.2f}/dia\n"
            )

        estilo.escrever_lista(
            self.resultado,
            "\n".join(linhas) or "Nenhum veículo cadastrado."
        )
