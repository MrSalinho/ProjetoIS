from flask import Flask, request, jsonify
from utils import carregar_livros, guardar_livros, validar_livro
from jsonschema.exceptions import ValidationError

app = Flask(__name__)

@app.route("/livros", methods=["GET"])
def listar_livros():
    return jsonify(carregar_livros())

@app.route("/livros", methods=["POST"])
def adicionar_livro():
    novo_livro = request.get_json()
    try:
        validar_livro(novo_livro)
    except ValidationError as e:
        return jsonify({"erro": "Livro inválido", "detalhe": str(e)}), 400
    livros = carregar_livros()
    livros.append(novo_livro)
    guardar_livros(livros)
    return jsonify(novo_livro), 201

if __name__ == "__main__":
    app.run(debug=True)
