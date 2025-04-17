from flask import Flask, request, jsonify, Response
import json
from jsonschema import validate, ValidationError
import dicttoxml
import xmltodict
from jsonpath_ng import parse
import os
import requests  # Para as interações com GraphQL e gRPC

app = Flask(__name__)

# Caminhos dos ficheiros
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'livro_schema.json')
DADOS_PATH = os.path.join(os.path.dirname(__file__), 'livros.json')

# Carregar o schema
with open(SCHEMA_PATH) as f:
    schema = json.load(f)

# Função de validação
def validar_livro(livro):
    try:
        validate(instance=livro, schema=schema)
    except ValidationError as e:
        raise e

# Função para ler e escrever livros
def ler_livros():
    with open(DADOS_PATH) as f:
        return json.load(f)

def escrever_livros(livros):
    with open(DADOS_PATH, 'w') as f:
        json.dump(livros, f, indent=2)

# CRUD
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
    livros_novos = [livro for livro in livros if livro['id'] != id]
    if len(livros_novos) == len(livros):
        return jsonify({"erro": "Livro não encontrado"}), 404
    escrever_livros(livros_novos)
    return jsonify({"msg": "Livro apagado"})

# Exportação/Importação
@app.route('/export/json', methods=['GET'])
def export_json():
    livros = ler_livros()
    return jsonify(livros)

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
    return jsonify({"msg": "Importação concluída"})

@app.route('/import/xml', methods=['POST'])
def import_xml():
    xml_data = request.data
    data_dict = xmltodict.parse(xml_data)
    livros = data_dict.get('livros', {}).get('item', [])
    if isinstance(livros, dict):  # Só um livro
        livros = [livros]
    # Converter campos para os tipos corretos
    for livro in livros:
        livro['id'] = int(livro['id'])
        livro['ano'] = int(livro['ano'])
    for livro in livros:
        try:
            validar_livro(livro)
        except ValidationError as e:
            return jsonify({"erro": "Livro inválido", "detalhe": str(e)}), 400
    escrever_livros(livros)
    return jsonify({"msg": "Importação concluída"})

# Consulta JSONPath
@app.route('/consultar', methods=['POST'])
def consultar_jsonpath():
    req = request.get_json()
    expr = req.get('jsonpath')
    livros = ler_livros()
    jsonpath_expr = parse(expr)
    result = [match.value for match in jsonpath_expr.find(livros)]
    return jsonify(result)

# Interação com GraphQL
@app.route("/graphql/livros", methods=["GET"])
def graphql_livros():
    try:
        response = requests.get("http://localhost:4000/graphql", json={"query": "{ livros { id titulo autor ano estado } }"})
        response.raise_for_status()  # Verifica se houve erro na requisição
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"erro": "Erro ao comunicar com GraphQL", "detalhe": str(e)}), 500

# Interação com gRPC
@app.route("/grpc/livros", methods=["GET"])
def grpc_livros():
    try:
        response = requests.get("http://localhost:50051/livros")
        response.raise_for_status()  # Verifica se houve erro na requisição
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"erro": "Erro ao comunicar com gRPC", "detalhe": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)
