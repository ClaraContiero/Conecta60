from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, EmailField, PasswordField
from wtforms.validators import DataRequired 


############################################## COMANDO PARA RODAR O SITE ##############################################
app = Flask(__name__)

#### CHAVE SECRETA
app.config['SECRET_KEY'] = "minhaSenhaHiperUltraMegaBlasterSecreta"

############################################## ROTAS PARA AS PÁGINAS ##############################################

# Página Inicial ##############################################
@app.route("/")
def inicial():
    return render_template('inicio.html')

# Página escolha de prof/aluno ##############################################
@app.route("/cadProfAluno")
def cadProfAluno():
    return render_template('cadastroProfAlun.html')

# Página de cadastro ##############################################
class cadastro(FlaskForm):
    dataNasc = DateField('Data de Nascimento *', validators=[DataRequired()])
    nomeCompleto = StringField('Nome Completo *', validators=[DataRequired()])
    email = EmailField('Email *', validators=[DataRequired()])
    senha = PasswordField('Senha *',validators=[DataRequired()])
    enviar = SubmitField('CADASTRAR')

@app.route("/Cadastre-se", methods=['GET', 'POST'])
def cadastrar():
    name = None
    form = cadastro()
    #validando o formulario
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash('Cadastrado com sucesso!')
    return render_template('cadastro.html',
        name = name,
        form = form)


# Página de login ##############################################
class logar(FlaskForm):
    email = EmailField('Email *', validators=[DataRequired()])
    senha = PasswordField('Senha *',validators=[DataRequired()])
    enviar = SubmitField('ENTRAR')


@app.route("/Entrar")
def login():
    name = None
    form = logar()
    #validando o formulario
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash('Login realizado com sucesso!')
    return render_template('login.html',
        name = name,
        form = form)

# Página de módulos ##############################################
@app.route("/modulos")
def modulos():
    return render_template('modulos.html')

# Página de conteúdos ##############################################
@app.route("/conteudos")
def conteudos():
    return render_template('conteudos.html')

# Página de digitação ##############################################
@app.route("/teste-digitacao")
def digita():
    return render_template('digitacao.html')


# Página inicial do adm ##############################################
@app.route("/adm")
def administrador():
    return render_template('inicio_professor.html')
############################################## FINALIZA A APLICAÇÃO ##############################################


if __name__ == "__main__":
    app.run(debug = True)
