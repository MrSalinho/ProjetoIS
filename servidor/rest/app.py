from flask import Flask, request, jsonify, Response
import json
from jsonschema import validate, ValidationError
import dicttoxml
import xmltodict
from jsonpath_ng import parse
import os

app = Flask(__name__)

# Caminhos dos ficheiros
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'livro_schema.json')
DADOS_PATH = os.path.join(os.path.dirname(__file__), 'livros.json')

# Carregar o schema
with open(SCHEMA_PATH) as f:
    schema = json.load(f)

def validar_livro(livro):
    validate(instance=livro, schema=schema)

def ler_livros():
    try:
        with open(DADOS_PATH) as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def escrever_livros(livros):
    with open(DADOS_PATH, 'w') as f:
        json.dump(livros, f, indent=2)

@app.route("/livros", methods=["GET"])
def listar_livros():
    return jsonify(ler_livros())

@app.route("/livros", methods=["POST"])
def adicionar_livro():
    novo_livro = request.get_json()
    try:
        validar_livro(novo_livro)
    except ValidationError as e:
        return jsonify({"erro": "Livro inválido", "detalhe": str(e)}), 400
    livros = ler_livros()
    livros.append(novo_livro)
    escrever_livros(livros)
    return jsonify(novo_livro), 201

@app.route("/livros/<int:id>", methods=["PUT"])
def atualizar_livro(id):
    livro_atualizado = request.get_json()
    try:
        validar_livro(livro_atualizado)
    except ValidationError as e:
        return jsonify({"erro": "Livro inválido", "detalhe": str(e)}), 400
    livros = ler_livros()
    for i, livro in enumerate(livros):
        if livro['id'] == id:
            livros[i] = livro_atualizado
            escrever_livros(livros)
            return jsonify(livro_atualizado)
    return jsonify({"erro": "Livro não encontrado"}), 404

@app.route("/livros/<int:id>", methods=["DELETE"])
def apagar_livro(id):
    livros = ler_livros()
    livros_novos = [l for l in livros if l['id'] != id]
    if len(livros_novos) == len(livros):
        return jsonify({"erro": "Livro não encontrado"}), 404
    escrever_livros(livros_novos)
    return jsonify({"mensagem": "Livro apagado"})

@app.route('/export/json', methods=['GET'])
def export_json():
    return jsonify(ler_livros())

@app.route('/export/xml', methods=['GET'])
def export_xml():
    livros = ler_livros()
    xml = dicttoxml.dicttoxml(livros, custom_root='livros', attr_type=False)
    return Response(xml, mimetype='application/xml')

@app.route('/import/json', methods=['POST'])
def import_json():
    livros = request.get_json()
    if not isinstance(livros, list):
        return jsonify({"erro": "Formato inválido"}), 400
    for livro in livros:
        try:
            validar_livro(livro)
        except ValidationError as e:
            return jsonify({"erro": "Livro inválido", "detalhe": str(e)}), 400
    escrever_livros(livros)
    return jsonify({"mensagem": "Importação concluída"})

if __name__ == "__main__":
    # Criar arquivo de dados se não existir
    if not os.path.exists(DADOS_PATH):
        escrever_livros([])
    app.run(debug=True, host="0.0.0.0", port=5000) 