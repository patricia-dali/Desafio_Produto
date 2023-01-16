import pyodbc
from flask import Flask, render_template, request, redirect

#Patrícia Albuquerque


app = Flask(__name__)


dados_conexao = (
    "Driver={SQL SERVER};"
    "Server=DESKTOP-BUOLEKU\SQLEXPRESS;"
    "Database=db_exposicao;"
    "Username=sa;"
    "password=123456;"
)

conexao = pyodbc.connect(dados_conexao)
cursor = conexao.cursor()



class Produto:
    def __init__(self, nome, imageUrl, unityPrice, autor, descricao, showInHomePage):
        self.nome = nome
        self.imageUrl = imageUrl
        self.unityPrice = unityPrice
        self.autor = autor
        self.descricao = descricao
        self.showInHomePage = showInHomePage


class Filtro:
    def __init__(self, filtro):
        self.filtro = filtro
         
class Pesquisa:
    def __init__(self, pesquisa):
        self.pesquisa = pesquisa





@app.route('/')
def index():
    comando = f"""
            SELECT nome, imageUrl FROM cad_produtos
            WHERE showInHomePage = 'True'
        """

    cursor.execute(comando)
    carrosel = []
    carrosel = cursor.fetchall()


    return render_template('/index.html', carrosel=carrosel)


@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')


@app.route('/produtos')
def produtos():
    
        comando = f"""
            SELECT id, nome, createDate, imageUrl, unityPrice, createDate descricao FROM cad_produtos
        """
        

        cursor.execute(comando)
        produtos = []
        produtos = cursor.fetchall()



        return render_template('produtos.html', produtos=produtos)



@app.route('/filtro', methods=['POST', 'GET'])
def filtro():
    if request.method == 'POST':
        formFiltro = Filtro(
            request.form["filtro"]
        )

        by = ''
        order = ''

        if formFiltro.filtro == "0":
            by = 'unityPrice'
            order = 'DESC'
        if formFiltro.filtro == "1":
            by = 'unityPrice'
            order = 'ASC'
        if formFiltro.filtro == "2":
            by = 'createDate'
            order = 'DESC'
        if formFiltro.filtro == "3":
            by = 'createDate'
            order = 'ASC'


        comando = f"""SELECT id, imageUrl, nome, createDate, unityPrice FROM cad_produtos
                    ORDER BY {by} {order}"""


        cursor.execute(comando)
        filtroP = []
        filtroP = cursor.fetchall()


        return render_template('produtos.html', filtroP=filtroP)


@app.route('/produto/<id>')
def indProd(id):

    comando = f"""
    SELECT nome, imageUrl, unityPrice, autor, createDate, descricao FROM cad_produtos
    WHERE id = {id}
    """

    cursor.execute(comando)
    resultado = []
    resultado = cursor.fetchall()


    return render_template('indProd.html', id=id, resultado=resultado)


@app.route('/pesquisa', methods=['POST', 'GET'])
def pesquisa():
    if request.method == 'POST':
        formPesquisa = Pesquisa(
            request.form["pesquisa"]
        )


        comando = f"""
            SELECT id, nome, imageUrl, createDate, autor, unityPrice FROM cad_produtos 
            WHERE nome LIKE '{formPesquisa.pesquisa}%' or 
                unityPrice LIKE '{formPesquisa.pesquisa}%' or 
                autor LIKE '{formPesquisa.pesquisa}%' or  
                createDate LIKE '{formPesquisa.pesquisa}%' or
                YEAR(createDate) LIKE '{formPesquisa.pesquisa}%';
        """

        cursor.execute(comando)
        InPesquisa = []
        InPesquisa = cursor.fetchall()


        return render_template('produtos.html', InPesquisa=InPesquisa)




@app.route('/cadastrar', methods=['POST', 'GET'])
def cadastrar():
        if request.method == 'POST':
            formProduto = Produto(
                request.form["nome"],
                request.form["imageUrl"],
                request.form["unityPrice"],
                request.form["autor"],
                request.form["descricao"],
                request.form["showInHomePage"]
        )
        comando = f"""
        INSERT INTO cad_produtos(nome, createDate, imageUrl, unityPrice, autor, descricao, showInHomePage)
        VALUES(
        '{formProduto.nome}',
        GETDATE(),
        '{formProduto.imageUrl}',
        {formProduto.unityPrice},
        '{formProduto.autor}',
        '{formProduto.descricao}',
        '{formProduto.showInHomePage}'
        )
        """

        cursor.execute(comando) 
        cursor.commit()
        


        return redirect('/cadastro')

        

if __name__ == '__main__':
    app.run(debug=True)