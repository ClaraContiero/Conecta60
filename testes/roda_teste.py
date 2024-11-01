from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired 

#roda o site
app = Flask(__name__)
app.config['SECRET_KEY'] = "minhaSenhaHiperUltraMegaBlasterSecreta"

#criando uma classe de formulário
class NameForm(FlaskForm):
    name = StringField("Qual é seu nome", validators=[DataRequired()]) #mostra se você preencheu o formulário
    submit = SubmitField('Enviar')





#rotas das página do site
@app.route("/name", methods=['GET', 'POST'])
def name():
    name = None
    form = NameForm()
    #validando o form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        
    return render_template('index_teste.html',
        name = name,
        form = form )



if __name__ == "__main__":
    app.run(debug = True)
