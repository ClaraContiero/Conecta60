from flask import Flask, render_template

#roda o site
app = Flask(__name__)


#rotas das página do site
@app.route("/")

def inicial():
    return render_template('inicio.html')





if __name__ == "__main__":
    app.run(debug = True)