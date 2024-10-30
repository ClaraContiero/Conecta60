from flask import Flask, render_template

#roda o site
app = Flask(__name__)


#rotas das página do site
@app.route("/")
def inicial():
    return render_template('inicio.html')

@app.route("/cadProfAluno")
def cadProfAluno():
    return render_template('cadastroProfAlun.html')

@app.route("/cadastro")
def cadastro():
    return render_template('cadastro.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/modulos")
def modulos():
    return render_template('modulos.html')

@app.route("/conteudos")
def conteudos():
    return render_template('conteudos.html')


if __name__ == "__main__":
    app.run(debug = True)