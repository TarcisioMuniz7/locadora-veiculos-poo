
import customtkinter as ctk
import sqlite3

from tkinter import messagebox
from modelos.cliente import Cliente
from banco.cliente_dao import ClienteDAO


class TelaClientes(ctk.CTkToplevel):

    def __init__(self, master):
        super().__init__(master)

        self.title("Cadastro de Clientes")
        self.geometry("500x500")

        self.dao = ClienteDAO()

        ctk.CTkLabel(
            self,
            text="Cadastro de Clientes",
            font=("Arial", 20, "bold")
        ).pack(pady=20)

        self.entrada_nome = ctk.CTkEntry(
            self, placeholder_text="Nome completo",
            width=300
        )
        self.entrada_nome.pack(pady=5)

        self.entrada_cpf = ctk.CTkEntry(
            self, placeholder_text="CPF",
            width=300
        )
        self.entrada_cpf.pack(pady=5)

        self.entrada_telefone = ctk.CTkEntry(
            self, placeholder_text="Telefone",
            width=300
        )
        self.entrada_telefone.pack(pady=5)

        ctk.CTkButton(
            self,
            text="Cadastrar Cliente",
            command=self.cadastrar_cliente
        ).pack(pady=15)

        ctk.CTkButton(
            self,
            text="Listar Clientes",
            command=self.listar_clientes
        ).pack(pady=5)

        self.resultado = ctk.CTkTextbox(
            self, width=420, height=150
        )
        self.resultado.pack(pady=15)

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
        self.resultado.delete("1.0", "end")

        for id_cliente, nome, cpf, telefone in self.dao.listar():
            self.resultado.insert(
                "end",
                f"ID: {id_cliente} | {nome}\n"
                f"CPF: {cpf} | Tel: {telefone}\n\n"
            )
