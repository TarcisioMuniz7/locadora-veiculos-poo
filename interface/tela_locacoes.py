
import customtkinter as ctk
from tkinter import messagebox

from banco.locacao_dao import LocacaoDAO
from interface import estilo


class TelaLocacoes(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.dao = LocacaoDAO()
        self.clientes = {}
        self.veiculos = {}

        estilo.cabecalho(
            self, "Locações", "Registre aluguéis e finalize devoluções."
        )

        corpo = estilo.corpo_em_colunas(self)

        nova = estilo.card(corpo)
        nova.grid(row=0, column=0, sticky="n", padx=(0, 24))

        estilo.titulo_card(nova, "Nova locação")
        self.menu_clientes = estilo.menu(
            nova, "Cliente", ["Nenhum cliente"]
        )
        self.menu_veiculos = estilo.menu(
            nova, "Veículo disponível", ["Nenhum veículo disponível"]
        )
        self.entrada_dias = estilo.campo(nova, "Quantidade de diárias")
        estilo.botao_primario(
            nova, "Registrar locação", self.registrar_locacao
        )

        historico = estilo.card(corpo)
        historico.grid(row=0, column=1, sticky="nsew")

        estilo.titulo_card(historico, "Histórico de locações")

        # O rodapé é empacotado antes da lista para não ser cortado.
        rodape = ctk.CTkFrame(historico, fg_color="transparent")
        rodape.pack(side="bottom", fill="x", padx=24, pady=(8, 20))

        ctk.CTkLabel(
            rodape, text="Finalizar locação",
            font=(estilo.FONTE, 13, "bold"), text_color=estilo.COR_TEXTO
        ).pack(side="left", padx=(0, 12))

        self.entrada_id = ctk.CTkEntry(
            rodape, placeholder_text="ID", width=90, height=40,
            corner_radius=8, border_width=1,
            border_color=estilo.COR_BORDA, fg_color=estilo.COR_CAMPO,
            text_color=estilo.COR_TEXTO, font=(estilo.FONTE, 13)
        )
        self.entrada_id.pack(side="left", padx=(0, 12))

        ctk.CTkButton(
            rodape, text="Finalizar", width=120, height=40,
            corner_radius=8, fg_color=estilo.COR_PRIMARIA,
            hover_color=estilo.COR_PRIMARIA_HOVER,
            font=(estilo.FONTE, 13, "bold"),
            command=self.finalizar_locacao
        ).pack(side="left")

        self.resultado = estilo.lista(historico)

    def ao_mostrar(self):
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
        linhas = []

        for registro in self.dao.listar_locacoes():
            id_locacao, cliente, modelo, placa, dias, valor, status = registro

            linhas.append(
                f"#{id_locacao}  {cliente}  ·  {status}\n"
                f"{modelo} ({placa})  ·  {dias} diária(s)  ·  "
                f"R$ {valor:.2f}\n"
            )

        estilo.escrever_lista(
            self.resultado,
            "\n".join(linhas) or "Nenhuma locação cadastrada."
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
