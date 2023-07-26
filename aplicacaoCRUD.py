import tkinter as tk
from tkinter import ttk
import crud as crud

class PrincipalBD:
    def __init__(self, win):
        self.objBD = crud.AppBD()
        #COMPONENTES
        self.lbCodigo = tk.Label(win, text="Codigo do Produto: ")
        self.lbNome = tk.Label(win, text="Nome do Produto: ")
        self.lbPreco = tk.Label(win, text="Preco")

        self.txtCodigo = tk.Entry(bd=3)
        self.txtNome = tk.Entry()        
        self.txtPreco = tk.Entry()
        self.btnCadastrar = tk.Button(win, text='Cadastrar', command=self.fCadastrarProduto)
        self.btnAtualizar = tk.Button(win, text='Atualizar', command=self.fAtualizarProduto)
        self.btnExcluir = tk.Button(win, text='Excluir', command=self.fExcluirProduto)
        self.btnLimpar = tk.Button(win, text='Limpar', command=self.fLimparTela)

#=================================================================== COMPONENTES TreeView ==========================================================================================
        
        self.dadosColunas = ("Codigo", "Nome", "Preco")

        self.treeProdutos = ttk.Treeview(win, columns=self.dadosColunas, selectmode='browse')
        
        self.verscrlbar = ttk.Scrollbar(win, orient="vertical", command=self.treeProdutos.yview)
        self.treeProdutos.configure(yscrollcommand=self.verscrlbar.set)

        self.treeProdutos.heading("Codigo", text="Codigo")
        self.treeProdutos.heading("Nome", text="Nome")
        self.treeProdutos.heading("Preco", text="Preco")

        self.treeProdutos.column("Codigo", minwidth=0, width=100)
        self.treeProdutos.column("Nome", minwidth=0, width=100)
        self.treeProdutos.column("Preco", minwidth=0, width=100)

        self.treeProdutos.pack(padx=10, pady=10)

        self.treeProdutos.bind("<<TreeviewSelect>>", self.apresentarRegistrosSelecionados)

#=================================================================== POSICIONANDO COMPONENTES NA JANELA ============================================================================================================================

        self.lbCodigo.place(x=100, y=50)
        self.txtCodigo.place(x=250, y=50)

        self.lbNome.place(x=100, y=100)
        self.txtNome.place(x=250, y=100)

        self.lbPreco.place(x=100, y=150)
        self.txtPreco.place(x=250, y=150)

        self.btnCadastrar.place(x=100, y=200)
        self.btnAtualizar.place(x=200, y=200)
        self.btnExcluir.place(x=300, y=200)
        self.btnLimpar.place(x=400, y=200)

        self.treeProdutos.place(x=100, y=250, width=700, height=300)  # Ajuste de tamanho da Treeview
        self.verscrlbar.place(x=805, y=250, height=300)  # Corrigido aqui

        self.carregarDadosIniciais()

#-------------------------------------------------------------------------------

    def apresentarRegistrosSelecionados(self, event):
        self.fLimparTela()
        for selection in self.treeProdutos.selection():
            item = self.treeProdutos.item(selection)
            codigo, nome, preco = item["values"][0:3]
            self.txtCodigo.insert(0, codigo)
            self.txtNome.insert(0, nome)
            self.txtPreco.insert(0, preco)
        
#-------------------------------------------------------------------------------

    def carregarDadosIniciais(self):
        try:
            self.id = 0
            self.iid = 0
            registros = self.objBD.selecionarDados()
            print("************************  dados disponiveis no BD ************************")
            for item in registros:
                codigo = item[0]
                nome = item[1]
                preco = item[2]
                print("Codigo =", codigo)
                print("Nome =", nome)
                print("Preco =", preco)

                self.treeProdutos.insert('', 'end', iid=self.iid, values=(codigo, nome, preco))
                self.iid = self.iid + 1
                self.id = self.id + 1
            print('Dados da Base')
        except:
            print('Ainda nao Existem dados para carregar')

#===================================================================================
#LerDados da Tela
#===================================================================================
    def fLerCampos(self):
        try:
            print("************************  dados disponiveis ************************ ")
            codigo = int(self.txtCodigo.get())
            print('codigo', codigo)
            nome = self.txtNome.get()
            print('nome', nome)
            preco = float(self.txtPreco.get())
            print('preco', preco)
            print('Leitura dos Dados com Sucesso')
        except:
            print('Nao foi possivel ler os dados')
        return codigo, nome, preco

#====================================================================================
#Cadastrar Produtos
#====================================================================================
    def fCadastrarProduto(self):
        try:
            print('************************  dados disponiveis ************************ ')
            codigo, nome, preco = self.fLerCampos()
            self.objBD.inserirDados(codigo, nome, preco)
            self.treeProdutos.insert('', 'end', iid=self.iid, values=(codigo, nome, preco))
            self.iid = self.iid + 1 
            self.id = self.id + 1
            self.fLimparTela()
            print('Produto Cadastrado com Sucesso')
        except:
            print('Nao foi possivel realizar o cadastro')

    def fAtualizarProduto(self):
        try: 
            print("************************  dados disponiveis ************************ ")
            codigo, nome, preco = self.fLerCampos()
            self.objBD.atualizarDados(codigo, nome, preco)
            #RECARREGAR DADOS NA TELA
            self.treeProdutos.delete(*self.treeProdutos.get_children())
            self.carregarDadosIniciais()
            self.fLimparTela()
            print("Produto Atualizado com sucesso!!")
        except:
            print("Nao foi possivel fazer a atualizacao.")

#=============================================================================================
#EXCLUIR PRODUTO
#=============================================================================================

    def fExcluirProduto(self):
        try:
            print("*************************  dados disponiveis ************************ ")
            codigo, nome, preco = self.fLerCampos()
            self.objBD.excluirDados(codigo)
            #RECARREGAR DADOS NA TELA
            self.treeProdutos.delete(*self.treeProdutos.get_children())
            self.carregarDadosIniciais()
            self.fLimparTela()
            print('Produto Excluido com Sucesso!!')
        except:
            print('nao foi possovel fazer a exclusao do produto.')

    def fLimparTela(self):
        try:
            print("************************  dados disponiveis ************************ ")
            self.txtCodigo.delete(0, tk.END)
            self.txtNome.delete(0, tk.END)
            self.txtPreco.delete(0, tk.END)
            print('Campos Limpos!')
        except:
            print('Nao foi possivel limpar os campos')

janela = tk.Tk()
principal = PrincipalBD(janela)
janela.title('Bem-vindo à Aplicação de Banco de Dados')
janela.geometry("820x600+10+10")
janela.mainloop()
