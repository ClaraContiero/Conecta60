from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, EmailField, PasswordField, TextAreaField, FileField, RadioField
from wtforms.validators import DataRequired, regexp
from wtforms import validators
from werkzeug.security import generate_password_hash
from extensions import db


############################################## COMANDO PARA RODAR O SITE ##############################################
def create_app():
    app = Flask(__name__)
    
    # Configuração da chave secreta e do banco de dados
    app.config['SECRET_KEY'] = "minhaSenhaHiperUltraMegaBlasterSecreta"
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://BD070324136:Ulfea9@BD-ACD/BD070324136"
    #app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///meubanco.db"
    
    # Inicializar o SQLAlchemy com o app
    db.init_app(app)

    with app.app_context():
        db.create_all()
    
    return app

app = create_app()

############################################## ROTAS PARA AS PÁGINAS ##############################################

# Página Inicial ##############################################
@app.route("/")
def inicial():
    return render_template('geral/inicio.html')

# Página escolha de prof/aluno ##############################################
@app.route("/Cadastro_Categoria")
def cadProfAluno():
    return render_template('geral/cadastroProfAlun.html')


# Página login de prof/aluno ##############################################
@app.route("/Login_Categoria")
def loginProfAluno():
    return render_template('geral/loginProfAlun.html')


# Página de cadastro ##############################################

class tabela_cadastro(db.Model): 
    __tablename__ = 'cadastro'
    id_cadastro = db.Column(db.Integer, primary_key = True)
    nome_completo = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique = True)
    data_nasc = db.Column(db.Date, nullable = False)
    senha = db.Column(db.String(256), nullable = False)

class cadastro(FlaskForm):
    data_nasc = DateField('Data de Nascimento *', validators=[DataRequired()])
    nome_completo = StringField('Nome Completo *', validators=[DataRequired()])
    email = EmailField('Email *', validators=[DataRequired()])
    senha = PasswordField('Senha *',validators=[DataRequired()])
    enviar = SubmitField('CADASTRAR')

@app.route("/Cadastre-se", methods=['GET', 'POST'])
def cadastrar():
    form = cadastro()
    name = None
    #validando o formulario
    if form.validate_on_submit():
        usuario = tabela_cadastro.query.filter_by(email=form.email.data).first()
        if usuario is None:
            try:

                senha_hash = generate_password_hash(form.senha.data)

                usuario = tabela_cadastro(
                    data_nasc = form.data_nasc.data,
                    nome_completo = form.nome_completo.data,
                    email = form.email.data,
                    senha = senha_hash
                )
                name = form.nome_completo.data
                db.session.add(usuario)
                db.session.commit()

                form.data_nasc.data = ''
                form.nome_completo.data = ''
                form.email.data = ''
                form.senha.data = ''

                flash('Cadastrado com sucesso!')
                return redirect(url_for('login'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao registrar o usuário: {e}')
        else:
                flash('Email já existente.')
    return render_template('geral/cadastro.html', form = form, name = name)


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
    return render_template('geral/login.html',
        name = name,
        form = form)

# Página de módulos ##############################################
@app.route("/Modulos")
def modulos():
    return render_template('aluno/modulos.html')

# Página de conteúdos ##############################################
class elementos(FlaskForm):
    h1 = TextAreaField(u'Digite um título...', [validators.optional(), validators.length(max=200)], render_kw={"placeholder": "Digite o título aqui..."})
    h2 = TextAreaField(u'Digite um subtítulo...', [validators.optional(), validators.length(max=250)], render_kw={"placeholder": "Digite o subtítulo aqui..."})
    paragrafo = TextAreaField(u'Digite um texto...', [validators.optional(), validators.length(max=1000)], render_kw={"placeholder": "Digite o texto aqui..."})
    imagem = FileField(u'Imagem', [regexp(r'^[a-zA-Z0-9_-]+\.jpg$', message="Apenas arquivos .jpg são permitidos.")])


@app.route("/Conteudo")
def conteudos():
    name = None
    form = elementos()
    return render_template('aluno/conteudos.html',
        name = name,
        form = form)

# Página de digitação ##############################################
@app.route("/Digitacao")
def digita():
    return render_template('aluno/digitacao.html')


# Página inicial do adm ##############################################
@app.route("/Administrador")
def administrador():
    return render_template('adm/inicio_professor.html')
############################################## FINALIZA A APLICAÇÃO ##############################################


if __name__ == "__main__":
    app.run(debug = True)
