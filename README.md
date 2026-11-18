# Sistema de Locadora de Veículos

Projeto acadêmico desenvolvido para a disciplina de **Programação Orientada a Objetos (POO)** do curso de Análise e Desenvolvimento de Sistemas (ADS).

## Sobre o projeto

O Sistema de Locadora de Veículos é uma aplicação desktop desenvolvida em Python para gerenciar clientes, veículos e locações de uma locadora de automóveis.

O projeto tem como objetivo aplicar os principais conceitos de Programação Orientada a Objetos, utilizando uma interface gráfica simples e um banco de dados para armazenar as informações.

## Funcionalidades

- Cadastro e listagem de clientes.
- Cadastro e listagem de veículos.
- Classificação de veículos nas categorias Econômico e SUV.
- Registro de locações vinculadas a clientes e veículos.
- Cálculo automático do valor das diárias.
- Controle da disponibilidade dos veículos.
- Finalização de locações e devolução dos veículos.
- Consulta ao histórico de locações.
- Armazenamento das informações em banco de dados SQLite.

## Tecnologias utilizadas

- **Python:** linguagem principal do projeto.
- **CustomTkinter:** biblioteca utilizada para desenvolver a interface gráfica.
- **SQLite:** banco de dados utilizado para armazenar clientes, veículos e locações.
- **Git:** ferramenta de controle de versões.
- **GitHub:** plataforma utilizada para hospedar o código-fonte.

## Conceitos de Programação Orientada a Objetos

O sistema utiliza os seguintes conceitos:

### Classes e objetos

Foram criadas classes para representar entidades do sistema, como `Cliente`, `Veiculo` e `Locacao`.

### Herança

As classes `CarroEconomico` e `CarroSUV` herdam características e comportamentos da classe `Veiculo`.

### Polimorfismo

As categorias de veículos possuem implementações próprias do método `calcular_valor()`, permitindo diferentes regras de cálculo conforme o tipo de veículo.

### Encapsulamento

A classe `Veiculo` utiliza o atributo `_disponivel` e métodos específicos para controlar a locação e a devolução dos veículos.

### Composição

A classe `Locacao` relaciona objetos de clientes e veículos para representar uma operação de aluguel.

## Estrutura do projeto

```text
locadora_veiculo/
├── banco/
│   ├── conexao.py
│   ├── cliente_dao.py
│   ├── veiculo_dao.py
│   └── locacao_dao.py
├── interface/
│   ├── tela_clientes.py
│   ├── tela_veiculos.py
│   └── tela_locacoes.py
├── modelos/
│   ├── cliente.py
│   ├── veiculo.py
│   ├── categorias.py
│   └── locacao.py
├── main.py
├── .gitignore
└── README.md
```

## Como executar o projeto

### 1. Requisitos

- Python 3 instalado.
- Biblioteca CustomTkinter instalada.

### 2. Clonar o repositório

```bash
git clone https://github.com/TarcisioMuniz7/locadora-veiculos-poo.git
```

### 3. Acessar a pasta do projeto

```bash
cd locadora-veiculos-poo
```

### 4. Instalar a biblioteca necessária

```bash
python -m pip install customtkinter
```

### 5. Executar o sistema

```bash
python main.py
```

O banco de dados SQLite é criado automaticamente na primeira execução.

## Exemplo de funcionamento

Um cliente solicita o aluguel de um veículo Econômico com diária de R$ 100,00 durante cinco dias.

O sistema calcula:

**5 × R$ 100,00 = R$ 500,00**

Após registrar a locação, o veículo fica indisponível para novos aluguéis.

Quando a locação é finalizada, o sistema atualiza seu status e disponibiliza novamente o veículo.

## Objetivo acadêmico

Demonstrar a aplicação prática dos conceitos de Programação Orientada a Objetos no desenvolvimento de um sistema desktop funcional, com persistência de dados e interface gráfica.

## Autor

**Tarcisio Muniz** **Ryan Haiala**

Curso: Análise e Desenvolvimento de Sistemas (ADS)

Projeto acadêmico — Programação Orientada a Objetos.