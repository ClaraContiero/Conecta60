from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, EmailField, PasswordField, TextAreaField, FileField, RadioField
from wtforms.validators import DataRequired, regexp
from wtforms import validators
from werkzeug.security import generate_password_hash
from extensions import db
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditor
from flask_ckeditor import CKEditorField
from flask_migrate import Migrate



# COMANDO PARA RODAR O SITE ----------------------------------------------------------------------------------------------------
def create_app():
    app = Flask(__name__)
    ckeditor = CKEditor(app)
    
    # Configuração da chave secreta e do banco de dados
    app.config['SECRET_KEY'] = "minhaSenhaHiperUltraMegaBlasterSecreta"
    #app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://BD070324136:Ulfea9@BD-ACD/BD070324136"
    #app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///meubanco.db"
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/clara_banco"
    #app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123@localhost/projetoi"

    
    # Inicializar o SQLAlchemy com o app
    db.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()
    
    return app

app = create_app()

# ROTAS PARA AS PÁGINAS ----------------------------------------------------------------------------------------------------

# Página Inicial ----------------------------------------------------------------------------------------------------
@app.route("/")
def inicial():
    return render_template('geral/inicio.html')


@app.route('/Administrador')
def adm():
    return render_template('adm/inicio_professor.html')

# Página escolha de prof/aluno ----------------------------------------------------------------------------------------------------
@app.route("/Cadastro_Categoria")
def cadProfAluno():
    return render_template('geral/cadastroProfAlun.html')


# Página de cadastro ----------------------------------------------------------------------------------------------------
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


@app.route('/Administrador/Editar/<int:id_cadastro>', methods=['GET', 'POST'])
def editar_cadastro(id_cadastro):
    cad = tabela_cadastro.query.get_or_404(id_cadastro)
    form = cadastro()
    if form.validate_on_submit():
        cad.nome_completo = form.nome_completo.data
        cad.email = form.email.data
        cad.senha = form.senha.data

        # Atualizando o banco de dados
        db.session.add(cad)
        db.session.commit()
        flash('Cadastro Atualizado.')
        return redirect(url_for('administrador', id_cadastro = cad.id_cadastro))
    form.nome_completo.data = cad.nome_completo
    form.email.data = cad.email
    form.senha.data = cad.senha
    return render_template('adm/adm_editar_perfil.html', form=form)
    

# Página de login ----------------------------------------------------------------------------------------------------
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

# Página de conteúdos ----------------------------------------------------------------------------------------------------
class tabela_conteudos(db.Model):
    __tablename__ = 'conteudo'
    id_conteudo = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(255))
    subtitulo = db.Column(db.String(255))
    texto = db.Column(db.Text)
    slug = db.Column(db.String(255))
    id_modulo = db.Column(db.Integer, db.ForeignKey('modulo.id_modulo'))


class postConteudo(FlaskForm):
    titulo = StringField('Título:', validators=[DataRequired()], render_kw={"placeholder": "Digite o título aqui..."})
    subtitulo = StringField('Subtítulo:', validators=[DataRequired()], render_kw={"placeholder": "Digite o subtítulo aqui..."})
    #texto = StringField('Texto:', validators=[DataRequired()], widget=TextArea(), render_kw={"placeholder": "Digite o texto aqui..."})
    texto = CKEditorField('Texto', validators=[DataRequired()], render_kw={"placeholder": "Digite o texto aqui..."})  
    slug = StringField('Slug:', validators=[DataRequired()], render_kw={"placeholder": "Digite o slug da página aqui..."})
    submit = SubmitField('Salvar e Publicar')

@app.route("/AddConteudo/<int:id_modulo>", methods=['GET', 'POST'])
def conteudos(id_modulo):
    form = postConteudo()

    if form.validate_on_submit():
        # Cria uma nova instância de conteúdo com os dados do formulário
        post = tabela_conteudos(
            titulo=form.titulo.data, 
            subtitulo=form.subtitulo.data,
            texto=form.texto.data, 
            slug=form.slug.data,
            id_modulo = id_modulo)
        
        # Adicionar o novo conteúdo ao banco de dados
        db.session.add(post)
        db.session.commit()

        # Limpar os campos do formulário após o envio
        form.titulo.data = ''
        form.subtitulo.data = ''
        form.texto.data = ''
        form.slug.data = ''

        # Adiciona uma mensagem de sucesso
        flash('Conteúdo postado com sucesso!')

        # Redirecionar ou renderizar novamente o template com os dados
        return redirect(url_for('posts'))

    # Recuperar todos os conteúdos do banco de dados
    all_conteudos = tabela_conteudos.query.all()
    # Renderizar o template, passando o formulário e os conteúdos
    return render_template('adm/conteudos.html', form=form, conteudos=all_conteudos)

# Página dos posts ----------------------------------------------------------------------------------------------------
@app.route('/Posts') # posts gerais
def posts():
    posts = tabela_conteudos.query.order_by(tabela_conteudos.titulo)
    modulos = tabela_modulos.query.order_by(tabela_modulos.titulo)
    return render_template('adm/conteudo_alunos.html', posts = posts, modulos = modulos )

@app.route('/Posts/<int:id_conteudo>') # individuais
def post(id_conteudo):
    post = tabela_conteudos.query.get_or_404(id_conteudo)
    return render_template('adm/post.html', post = post)



@app.route('/Posts/Editar/<int:id_conteudo>', methods=['GET', 'POST'])
def editar_post(id_conteudo):
    post = tabela_conteudos.query.get_or_404(id_conteudo)
    form = postConteudo()
    if form.validate_on_submit():
        post.titulo = form.titulo.data
        post.subtitulo = form.subtitulo.data
        post.texto = form.texto.data
        post.slug = form.slug.data

        # Atualizando o banco de dados
        db.session.add(post)
        db.session.commit()
        flash('Post atualizado.')
        return redirect(url_for('posts', id_conteudo = post.id_conteudo))
    form.titulo.data = post.titulo
    form.subtitulo.data = post.subtitulo
    form.texto.data = post.texto
    form.slug.data = post.slug
    return render_template('adm/editar_post.html', form=form)
    
@app.route('/Posts/Deletar/<int:id_conteudo>')
def deletar_post(id_conteudo):
    post_to_delete = tabela_conteudos.query.get_or_404(id_conteudo)

    try:
        db.session.delete(post_to_delete)
        db.session.commit()

        flash('Post deletado.')
        posts = tabela_conteudos.query.order_by(tabela_conteudos.titulo)
        return render_template('aluno/conteudo_alunos.html', posts = posts )

    except:
        flash('Houve um problema. Tente novamente.')
        posts = tabela_conteudos.query.order_by(tabela_conteudos.titulo)
        return render_template('adm/conteudo_alunos.html', posts = posts )


# Página de módulos
class tabela_modulos(db.Model):
    __tablename__ = 'modulo'
    id_modulo = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(255))
    descricao = db.Column(db.String(255))
    conteudo = db.relationship('tabela_conteudos', backref='modulo', lazy=True)

    # ver vídeo do migration

class postModulo(FlaskForm):
    titulo = StringField('Título:', validators=[DataRequired()], render_kw={"placeholder": "Digite o título aqui..."})
    descricao = StringField('Descrição:', validators=[DataRequired()], render_kw={"placeholder": "Digite a descrição aqui..."})
    submit = SubmitField('Salvar e Publicar')

@app.route("/AddModulo", methods=['GET', 'POST'])
def modulos():
    form = postModulo()
    conteudo_modulo = {}


    if form.validate_on_submit():
        # Cria uma nova instância de conteúdo com os dados do formulário
        postMod = tabela_modulos(
            titulo=form.titulo.data, 
            descricao=form.descricao.data)
        
        # Adicionar o novo conteúdo ao banco de dados
        db.session.add(postMod)
        db.session.commit()

        # Limpar os campos do formulário após o envio
        form.titulo.data = ''
        form.descricao.data = ''

        # Adiciona uma mensagem de sucesso
        flash('Modulo postado com sucesso!')

        # Redirecionar ou renderizar novamente o template com os dados
        return redirect(url_for('posts'))

    # Recuperar todos os conteúdos do banco de dados
    all_modulos = tabela_modulos.query.all()
    # Renderizar o template, passando o formulário e os conteúdos
    return render_template('adm/modulos.html', form=form, conteudos=all_modulos)


@app.route('/Posts/Editar_Modulo/<int:id_modulo>', methods=['GET', 'POST'])
def editar_modulo(id_modulo):
    modulo = tabela_modulos.query.get_or_404(id_modulo)
    form = postModulo()
    if form.validate_on_submit():
        modulo.titulo = form.titulo.data
        modulo.descricao = form.descricao.data

        # Atualizando o banco de dados
        db.session.add(modulo)
        db.session.commit()
        flash('Modulo atualizado.')
        return redirect(url_for('posts', id_modulo = modulo.id_modulo))
    form.titulo.data = modulo.titulo
    form.descricao.data = modulo.descricao

    return render_template('adm/editar_modulo.html', form=form)
    
@app.route('/Posts/Deletar_Modulos/<int:id_modulo>')
def deletar_modulo(id_modulo):
    modulo_to_delete = tabela_modulos.query.get_or_404(id_modulo)

    try:
        db.session.delete(modulo_to_delete)
        db.session.commit()

        flash('Modulo deletado.')
        modulos = tabela_modulos.query.order_by(tabela_modulos.titulo)
        return render_template('adm/conteudo_alunos.html', modulos = modulos )

    except:
        flash('Houve um problema. Tente novamente.')
        modulos = modulos.query.order_by(tabela_modulos.titulo)
        return render_template('adm/conteudo_alunos.html', modulos = modulos )


# Página de digitação ----------------------------------------------------------------------------------------------------
@app.route("/Digitacao")
def digita():
    return render_template('aluno/digitacao.html')


# Página inicial do adm ----------------------------------------------------------------------------------------------------
@app.route("/Administrador")
def administrador():
    return render_template('adm/inicio_professor.html')



# Página inicial do aluno ----------------------------------------------------------------------------------------------------

@app.route("/Modulos")
def modulosAlunos():
    posts = tabela_conteudos.query.order_by(tabela_conteudos.titulo)
    modulos = tabela_modulos.query.order_by(tabela_modulos.titulo)
    return render_template('aluno/postsAlunos.html', posts = posts, modulos = modulos )

@app.route('/Modulos/<int:id_conteudo>') # individuais
def lerPost(id_conteudo):
    post = tabela_conteudos.query.get_or_404(id_conteudo)
    return render_template('aluno/lerPost.html', post = post)


# FINALIZA A APLICAÇÃO ----------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug = True)


