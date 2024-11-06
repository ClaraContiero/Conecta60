# source novo_virtual/Scripts/activate
# deactivate

from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#roda o site
app = Flask(__name__)


#adicionando o banco de dados com o sql lite
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

#adicionando o NOVO banco de dados com o mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:senha987@localhost/our_users'

#chave secreta
app.config['SECRET_KEY'] = "minhaSenhaHiperUltraMegaBlasterSecreta"

#iniciando o banco de dados
db = SQLAlchemy(app)

#criando um modelo
class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(120), nullable = False, unique = True)
    #date_added = db.Column(db.DateTime, default=lambda: datetime.utcnow)

    #criando uma string
    def __repr__(self):
        return '<Name %r>' % self.name

#criando uma classe de formulário, é isso que vou usar no cadastro
class NameForm(FlaskForm):
    name = StringField("Qual é seu nome", validators=[DataRequired()]) #mostra se você preencheu o formulário
    submit = SubmitField('Enviar')


#formulario para cadastrarmos nome e email
class UserForm(FlaskForm):
    name = StringField("Nome", validators=[DataRequired()]) #mostra se você preencheu o formulário
    email = StringField("Email", validators=[DataRequired()]) #mostra se você preencheu o formulário
    submit = SubmitField('Enviar')



#para puxar imagens: https://wtforms.readthedocs.io/en/2.3.x/fields/

#rotas das página do site
@app.route("/")
def name():
    name = None
    form = NameForm()
    #validando o form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash('Enviado com sucesso!')
        
    return render_template('index_teste.html',
        name = name,
        form = form )


@app.route("/user/add", methods=['GET', 'POST']) #FUNCIONOU
def user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email = form.email.data).first()
        if user is None:
            user = Users(name = form.name.data, email = form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash('Usuário adicionado com sucesso')

    our_users = Users.query.order_by(Users.id)
    return render_template('add_user.html',
        form = form, 
        name = name,
        our_users = our_users )

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug = True)
