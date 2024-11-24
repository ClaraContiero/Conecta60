from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, EmailField, PasswordField, TextAreaField, FileField, RadioField
from wtforms.validators import DataRequired, regexp
from wtforms import validators
from werkzeug.security import generate_password_hash
from extensions import db
from wtforms.widgets import TextArea


############################################## COMANDO PARA RODAR O SITE ##############################################
def create_app():
    app = Flask(__name__)
    
    # Configuração da chave secreta e do banco de dados
    app.config['SECRET_KEY'] = "minhaSenhaHiperUltraMegaBlasterSecreta"
    #app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://BD070324136:Ulfea9@BD-ACD/BD070324136"
    #app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///meubanco.db"
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/clara_banco"

    
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
# criando um modelo de blog
class tabela_conteudos(db.Model):
    __tablename__ = 'conteudo'
    id_conteudo = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(255))
    subtitulo = db.Column(db.String(255))
    texto = db.Column(db.Text)
    slug = db.Column(db.String(255))
    # ver vídeo do migration

class postConteudo(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired()])
    subtitulo = StringField('Subtítulo', validators=[DataRequired()])
    texto = StringField('Texto', validators=[DataRequired()], widget=TextArea())
    slug = StringField('Slug', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route("/AddConteudo", methods=['GET', 'POST'])
def conteudos():
    form = postConteudo()

    if form.validate_on_submit():
        # Criar uma nova instância de conteúdo com os dados do formulário
        post = tabela_conteudos(
            titulo=form.titulo.data, 
            subtitulo=form.subtitulo.data,
            texto=form.texto.data, 
            slug=form.slug.data)
        
        # Adicionar o novo conteúdo ao banco de dados
        db.session.add(post)
        db.session.commit()

        # Limpar os campos do formulário após o envio
        form.titulo.data = ''
        form.subtitulo.data = ''
        form.texto.data = ''
        form.slug.data = ''

        # Adicionar uma mensagem de sucesso
        flash('Conteúdo postado com sucesso!')

        # Redirecionar ou renderizar novamente o template com os dados
        return redirect(url_for('conteudo'))

    # Recuperar todos os conteúdos do banco de dados
    all_conteudos = tabela_conteudos.query.all()

    # Renderizar o template, passando o formulário e os conteúdos
    return render_template('aluno/conteudos.html', form=form, conteudos=all_conteudos)


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
