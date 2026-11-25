
import customtkinter as ctk
import sqlite3

from tkinter import messagebox
from modelos.cliente import Cliente
from modelos.validacoes import (
    mascara_cpf, mascara_telefone, formatar_cpf, formatar_telefone
)
from banco.cliente_dao import ClienteDAO
from interface import estilo


class TelaClientes(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.dao = ClienteDAO()

        estilo.cabecalho(
            self, "Clientes", "Cadastre e consulte os clientes da locadora."
        )

        corpo = estilo.corpo_em_colunas(self)

        formulario = estilo.card(corpo)
        formulario.grid(row=0, column=0, sticky="n", padx=(0, 24))

        estilo.titulo_card(formulario, "Novo cliente")
        self.entrada_nome = estilo.campo(
            formulario, "Nome completo", placeholder="Ex.: Maria Oliveira"
        )
        self.entrada_cpf = estilo.campo(
            formulario, "CPF", placeholder="000.000.000-00",
            mascara=mascara_cpf
        )
        self.entrada_telefone = estilo.campo(
            formulario, "Telefone", placeholder="(00) 00000-0000",
            mascara=mascara_telefone
        )
        estilo.botao_primario(
            formulario, "Cadastrar cliente", self.cadastrar_cliente
        )

        painel_lista = estilo.card(corpo)
        painel_lista.grid(row=0, column=1, sticky="nsew")

        estilo.titulo_card(painel_lista, "Clientes cadastrados")
        self.resultado = estilo.lista(painel_lista)

    def ao_mostrar(self):
        self.listar_clientes()

    def cadastrar_cliente(self):
        nome = self.entrada_nome.get().strip()
        cpf = self.entrada_cpf.get().strip()
        telefone = self.entrada_telefone.get().strip()

        if not nome or not cpf or not telefone:
            messagebox.showwarning(
                "Atenção", "Preencha todos os campos!"
            )
            return

        try:
            cliente = Cliente(nome, cpf, telefone)
            self.dao.cadastrar(cliente)

            messagebox.showinfo(
                "Sucesso", "Cliente cadastrado!"
            )

            self.entrada_nome.delete(0, "end")
            self.entrada_cpf.delete(0, "end")
            self.entrada_telefone.delete(0, "end")

            self.listar_clientes()

        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Erro", "CPF já cadastrado!"
            )

        except ValueError as erro:
            messagebox.showerror("Erro", str(erro))

    def listar_clientes(self):
        linhas = [
            f"#{id_cliente}  {nome}\n"
            f"CPF {formatar_cpf(cpf)}  ·  "
            f"Tel. {formatar_telefone(telefone)}\n"
            for id_cliente, nome, cpf, telefone in self.dao.listar()
        ]

        estilo.escrever_lista(
            self.resultado,
            "\n".join(linhas) or "Nenhum cliente cadastrado."
        )
