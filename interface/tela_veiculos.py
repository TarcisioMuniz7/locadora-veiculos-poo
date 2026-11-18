
import customtkinter as ctk
import sqlite3

from tkinter import messagebox
from banco.veiculo_dao import VeiculoDAO
from modelos.categorias import CarroEconomico, CarroSUV

class TelaVeiculos(ctk.CTkToplevel):

    def __init__(self, master):
        super().__init__(master)

        self.title("Gerenciamento de Veículos")
        self.geometry("500x600")

        self.dao = VeiculoDAO()

        ctk.CTkLabel(
            self,
            text="Cadastro de Veículos",
            font=("Arial", 20, "bold")
        ).pack(pady=20)

        self.entrada_placa = ctk.CTkEntry(
            self, placeholder_text="Placa",
            width=300
        )
        self.entrada_placa.pack(pady=5)

        self.entrada_modelo = ctk.CTkEntry(
            self, placeholder_text="Modelo",
            width=300
        )
        self.entrada_modelo.pack(pady=5)

        self.categoria = ctk.CTkOptionMenu(
            self,
            values=["Econômico", "SUV"],
            width=300
        )
        self.categoria.pack(pady=5)

        self.entrada_valor = ctk.CTkEntry(
            self, placeholder_text="Valor da diária",
            width=300
        )
        self.entrada_valor.pack(pady=5)

        ctk.CTkButton(
            self,
            text="Cadastrar Veículo",
            command=self.cadastrar_veiculo
        ).pack(pady=15)

        ctk.CTkButton(
            self,
            text="Listar Veículos",
            command=self.listar_veiculos
        ).pack(pady=5)

        self.resultado = ctk.CTkTextbox(
            self, width=420, height=200
        )
        self.resultado.pack(pady=15)

    def cadastrar_veiculo(self):
        placa = self.entrada_placa.get().strip().upper()
        modelo = self.entrada_modelo.get().strip()
        categoria = self.categoria.get()

        try:
            if not placa or not modelo:
                raise ValueError("Preencha todos os campos!")

            valor = float(
                self.entrada_valor.get().strip().replace(",", ".")
            )

            if valor <= 0:
                raise ValueError(
                    "O valor da diária deve ser positivo."
                )

            if categoria == "Econômico":
                veiculo = CarroEconomico(placa, modelo, valor)
            else:
                veiculo = CarroSUV(placa, modelo, valor_diaria)

            self.dao.cadastrar(veiculo, categoria)

            messagebox.showinfo(
                "Sucesso", "Veículo cadastrado!"
            )

            self.entrada_placa.delete(0, "end")
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
        self.resultado.delete("1.0", "end")

        for registro in self.dao.listar():
            id_veiculo, placa, modelo, categoria, valor, disponivel = registro

            status = "Disponível" if disponivel else "Alugado"

            self.resultado.insert(
                "end",
                f"ID: {id_veiculo} | {modelo}\n"
                f"Placa: {placa} | Categoria: {categoria}\n"
                f"Diária: R$ {valor:.2f} | {status}\n\n"
            )
