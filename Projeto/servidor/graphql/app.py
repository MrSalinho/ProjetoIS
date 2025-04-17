from ariadne import QueryType, MutationType, make_executable_schema, graphql_sync
from flask import Flask, request, jsonify
import json
import os
from jsonschema import validate, ValidationError
import requests  # Import requests for REST calls

# Caminhos dos ficheiros
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "livro_schema.json")
DADOS_PATH = os.path.join(os.path.dirname(__file__), "livros.json")

# Carregar o schema JSON
with open(SCHEMA_PATH) as f:
    livro_schema = json.load(f)

def validar_livro(livro):
    validate(instance=livro, schema=livro_schema)

def ler_livros():
    try:
        with open(DADOS_PATH) as f:
            return json.load(f)
    except FileNotFoundError:
        livros_iniciais = []
        with open(DADOS_PATH, "w") as f:
            json.dump(livros_iniciais, f, indent=2)
        return livros_iniciais

def escrever_livros(livros):
    with open(DADOS_PATH, "w") as f:
        json.dump(livros, f, indent=2)

# Definir tipos e resolvers
query = QueryType()
mutation = MutationType()

@query.field("livros")
def resolve_livros(*_):
    # Fetch books from REST service
    response = requests.get("http://localhost:5000/livros")
    return response.json()

@query.field("livro")
def resolve_livro(*_, id):
    livros = ler_livros()
    for livro in livros:
        if livro["id"] == id:
            return livro
    return None

@mutation.field("adicionarLivro")
def resolve_adicionar_livro(*_, livro):
    try:
        validar_livro(livro)
    except ValidationError as e:
        raise Exception(f"Livro inválido: {e}")
    
    # Call REST service to add a book
    response = requests.post("http://localhost:5000/livros", json=livro)
    return response.json()

@mutation.field("atualizarLivro")
def resolve_atualizar_livro(*_, id, livro):
    try:
        validar_livro(livro)
    except ValidationError as e:
        raise Exception(f"Livro inválido: {e}")
    
    # Call REST service to update a book
    response = requests.put(f"http://localhost:5000/livros/{id}", json=livro)
    return response.json()

@mutation.field("apagarLivro")
def resolve_apagar_livro(*_, id):
    # Call REST service to delete a book
    response = requests.delete(f"http://localhost:5000/livros/{id}")
    return response.json()

@query.field("exportarLivrosJSON")
def resolve_exportar_livros_json(*_):
    return json.dumps(ler_livros())

@mutation.field("importarLivrosJSON")
def resolve_importar_livros_json(*_, livros_json):
    try:
        livros = json.loads(livros_json)
        for livro in livros:
            validar_livro(livro)
        escrever_livros(livros)
        return True
    except Exception as e:
        raise Exception(f"Erro na importação: {e}")

# Carregar schema GraphQL
type_defs = """
    type Livro {
        id: Int!
        titulo: String!
        autor: String!
        ano: Int!
        estado: String!
    }

    type Query {
        livros: [Livro!]!
        livro(id: Int!): Livro
        exportarLivrosJSON: String!
    }

    type Mutation {
        adicionarLivro(livro: LivroInput!): Livro!
        atualizarLivro(id: Int!, livro: LivroInput!): Livro
        apagarLivro(id: Int!): Boolean!
        importarLivrosJSON(livros_json: String!): Boolean!
    }

    input LivroInput {
        id: Int!
        titulo: String!
        autor: String!
        ano: Int!
        estado: String!
    }
"""

schema = make_executable_schema(type_defs, [query, mutation])

# Flask app
app = Flask(__name__)

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=True
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4000)
