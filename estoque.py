"""
Controle de Estoque - Documentação

Este programa permite o controle de um estoque de produtos. Ele oferece funcionalidades básicas, como adicionar, atualizar, pesquisar, exibir e excluir produtos do estoque.

Autor: [Robert Toledo]
Data: [6/09/2023]

Instruções de Uso:
1. Certifique-se de ter as bibliotecas SQLite3 e PySimpleGUI instaladas em seu ambiente Python.
2. Execute este arquivo usando o Python.

Este arquivo contém a classe EstoqueApp, que é responsável pelo controle do estoque e pela interface gráfica do programa.

Classe EstoqueApp:
- __init__(): Inicializa a conexão com o banco de dados SQLite e cria a tabela 'produtos' se ela não existir.
- fechar_conexao(): Fecha a conexão com o banco de dados.
- adicionar_produto(nome, quantidade): Adiciona um produto ao estoque.
- atualizar_estoque(id_produto, nova_quantidade): Atualiza a quantidade em estoque de um produto existente.
- listar_produtos(): Retorna uma lista de todos os produtos no estoque.
- pesquisar_produto(nome_produto): Pesquisa produtos com base no nome.
- excluir_produto(id_produto): Exclui um produto do estoque.
- criar_tabela(): Cria uma interface gráfica para exibir o estoque em uma tabela.
- run(): Executa o programa, exibindo a interface gráfica e respondendo às interações do usuário.

Para executar o programa, crie uma instância da classe EstoqueApp e chame o método run().

"""

import sqlite3
import PySimpleGUI as sg

class EstoqueApp:
    def __init__(self):
        self.conn = sqlite3.connect('alpha.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS produtos
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          nome TEXT NOT NULL,
                          quantidade INTEGER NOT NULL)''')
        self.conn.commit()
        self.fullscreen = False
        self.produtos = self.listar_produtos()  # Carrega os produtos do banco de dados

    def fechar_conexao(self):
        self.conn.close()

    def adicionar_produto(self, nome, quantidade):
        self.c.execute("INSERT INTO produtos (nome, quantidade) VALUES (?, ?)", (nome, quantidade))
        self.conn.commit()
        produto_id = self.c.lastrowid
        self.produtos.append((produto_id, nome, quantidade))  # Atualiza a lista de produtos

    def atualizar_estoque(self, id_produto, nova_quantidade):
        self.c.execute("UPDATE produtos SET quantidade = ? WHERE id = ?", (nova_quantidade, id_produto))
        self.conn.commit()
        # Atualiza a lista de produtos após a atualização
        for i, produto in enumerate(self.produtos):
            if produto[0] == id_produto:
                self.produtos[i] = (id_produto, produto[1], nova_quantidade)
                break

    def listar_produtos(self):
        self.c.execute("SELECT * FROM produtos")
        return self.c.fetchall()  # Retorna os produtos diretamente do banco de dados

    def pesquisar_produto(self, termo_pesquisa):
        # Pesquisa por nome ou ID e retorna os resultados
        resultados = []
        for produto in self.produtos:
            id_produto, nome, quantidade = produto
            if str(id_produto) == termo_pesquisa or termo_pesquisa.lower() in nome.lower():
                resultados.append(produto)
        return resultados

    def excluir_produto(self, id_produto):
        self.c.execute("DELETE FROM produtos WHERE id = ?", (id_produto,))
        self.conn.commit()
        # Remove o produto da lista após a exclusão
        self.produtos = [produto for produto in self.produtos if produto[0] != id_produto]

    def criar_tabela(self):
        header = ['ID', 'Nome', 'Quantidade']
        data = self.produtos

        layout = [
            [sg.Text('Sistema de Controle de Estoque', font=('Arial', 18))],
            [sg.InputText('', key='-PESQUISA-', size=(20, 1)), sg.Button('Pesquisar')],
            [sg.Table(values=data, headings=header, auto_size_columns=False,
                      justification='right', num_rows=min(25, len(data)))],
            [sg.Button('Fechar')]
        ]

        window = sg.Window('Estoque', layout, finalize=True, no_titlebar=True, resizable=True)

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Fechar':
                break
            elif event == 'Pesquisar':
                termo_pesquisa = values['-PESQUISA-']
                if termo_pesquisa:
                    resultados = self.pesquisar_produto(termo_pesquisa)
                    window['Table'].update(values=resultados)

        window.close()

    def run(self):
        sg.theme('LightBlue2')

        while True:
            if self.fullscreen:
                layout = [
                    [sg.Text('Sistema de Controle de Estoque', font=('Arial', 18))],
                    [sg.Button('Alternar Tela Cheia', size=(15, 2))],
                    [sg.Button('Sair', size=(15, 2))],
                ]
            else:
                layout = [
                    [sg.Text('Sistema de Controle de Estoque', font=('Arial', 18))],
                    [sg.Button('Adicionar Produto', size=(15, 2))],
                    [sg.Button('Atualizar Estoque', size=(15, 2))],
                    [sg.Button('Exibir Estoque', size=(15, 2))],
                    [sg.Button('Excluir Produto', size=(15, 2))],
                    [sg.Button('Alternar Tela Cheia', size=(15, 2))],
                    [sg.Button('Sair', size=(15, 2))],
                ]

            window = sg.Window('Controle de Estoque', layout, resizable=True, finalize=True)

            while True:
                event, values = window.read()

                if event == sg.WINDOW_CLOSED or event == 'Sair':
                    window.close()
                    self.fechar_conexao()
                    return
                elif event == 'Adicionar Produto':
                    nome = sg.popup_get_text('Digite o nome do produto:')
                    quantidade_text = sg.popup_get_text('Digite a quantidade em estoque:')
                    if nome and quantidade_text:
                        try:
                            quantidade = int(quantidade_text)
                            self.adicionar_produto(nome, quantidade)
                            sg.popup(f"Produto '{nome}' adicionado com sucesso!")
                        except ValueError:
                            sg.popup("Quantidade inválida. Digite um número inteiro válido.")
                elif event == 'Atualizar Estoque':
                    id_produto_text = sg.popup_get_text('Digite o ID do produto a ser atualizado:')
                    nova_quantidade_text = sg.popup_get_text(f"Digite a nova quantidade em estoque para o produto ID {id_produto_text}:")
                    if id_produto_text and nova_quantidade_text:
                        try:
                            id_produto = int(id_produto_text)
                            nova_quantidade = int(nova_quantidade_text)
                            self.atualizar_estoque(id_produto, nova_quantidade)
                            sg.popup("Estoque atualizado!")
                        except ValueError:
                            sg.popup("ID ou quantidade inválida. Digite números inteiros válidos.")
                elif event == 'Exibir Estoque':
                    if not self.fullscreen:
                        self.criar_tabela()
                elif event == 'Excluir Produto':
                    id_produto_text = sg.popup_get_text('Digite o ID do produto a ser excluído:')
                    if id_produto_text:
                        try:
                            id_produto = int(id_produto_text)
                            self.excluir_produto(id_produto)
                            sg.popup("Produto excluído com sucesso!")

                        except ValueError:
                            sg.popup("ID inválido. Digite um número inteiro válido.")
                elif event == 'Alternar Tela Cheia':
                    self.fullscreen = not self.fullscreen
                    window.TKroot.attributes('-fullscreen', self.fullscreen)

if __name__ == "__main__":
    app = EstoqueApp()
    app.run()