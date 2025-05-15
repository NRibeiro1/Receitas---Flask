from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Receita(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String, nullable=False)
    tipo = db.Column(db.String, nullable=False)
    origem = db.Column(db.String, nullable=False)
    ingredientes = db.Column(db.String, nullable=False)
    modo_preparo = db.Column(db.String, nullable=False)

    def __init__(self, nome, tipo, origem, ingredientes, modo_preparo):
        self.nome = nome
        self.tipo = tipo
        self.origem = origem
        self.ingredientes = ingredientes
        self.modo_preparo = modo_preparo

# Criar tabelas no banco
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastrar")
def cadastrar():
    return render_template("cadastro.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        tipo = request.form.get("tipo")
        origem = request.form.get("origem")
        ingredientes = request.form.get("ingredientes")
        modo_preparo = request.form.get("modo")

        if nome and tipo and origem and ingredientes and modo_preparo:
            nova_receita = Receita(nome, tipo, origem, ingredientes, modo_preparo)
            db.session.add(nova_receita)
            db.session.commit()
            return redirect(url_for("lista"))

    return render_template("cadastro.html")

@app.route("/lista")
def lista():
    receitas = Receita.query.all()
    return render_template("lista.html", receitas=receitas)

@app.route("/excluir/<int:id>")
def excluir(id):
    receita = Receita.query.get(id)
    if receita:
        db.session.delete(receita)
        db.session.commit()
    return redirect(url_for('lista'))

@app.route("/atualizar/<int:id>", methods=['GET', 'POST'])
def atualizar(id):
    receita = Receita.query.get(id)

    if request.method == "POST":
        nome = request.form.get("nome")
        tipo = request.form.get("tipo")
        origem = request.form.get("origem")
        ingredientes = request.form.get("ingredientes")
        modo_preparo = request.form.get("modo")

        if nome and tipo and origem and ingredientes and modo_preparo:
            receita.nome = nome
            receita.tipo = tipo
            receita.origem = origem
            receita.ingredientes = ingredientes
            receita.modo_preparo = modo_preparo

            db.session.commit()

            return redirect(url_for("lista"))
    return render_template("atualizar.html", receita=receita)

if __name__ == "__main__":
    app.run(debug=True)
