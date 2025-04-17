from flask import Flask, request, jsonify
import graphene
from graphene import ObjectType, String, Int, List, Field, Mutation
import json
import requests
import os

# Caminhos dos ficheiros
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "livro_schema.json")
DADOS_PATH = os.path.join(os.path.dirname(__file__), "livros.json")

# Carregar o schema JSON (para validações, se necessário)
with open(SCHEMA_PATH) as f:
    livro_schema = json.load(f)

def validar_livro(livro):
    # Aqui podes usar jsonschema.validate(livro, livro_schema)
    # para validar conforme o teu schema
    pass

def ler_livros():
    try:
        with open(DADOS_PATH) as f:
            return json.load(f)
    except FileNotFoundError:
        # Cria ficheiro vazio se não existir
        with open(DADOS_PATH, "w") as f:
            json.dump([], f, indent=2)
        return []

def escrever_livros(livros):
    with open(DADOS_PATH, "w") as f:
        json.dump(livros, f, indent=2)

# Definição do tipo Livro
class Livro(ObjectType):
    id = Int()
    titulo = String()
    autor = String()
    ano = Int()
    estado = String()

# Queries
class Query(ObjectType):
    livros = List(Livro)
    livro = Field(Livro, id=Int(required=True))

    def resolve_livros(self, info):
        # Obter lista via REST
        resp = requests.get("http://localhost:5001/livros")
        return resp.json()

    def resolve_livro(self, info, id):
        for l in ler_livros():
            if l["id"] == id:
                return l
        return None

# Mutation de adicionar livro
class AdicionarLivro(Mutation):
    class Arguments:
        id = Int(required=True)
        titulo = String(required=True)
        autor = String(required=True)
        ano = Int(required=True)
        estado = String(required=True)

    livro = Field(Livro)

    def mutate(self, info, id, titulo, autor, ano, estado):
        novo = {"id": id, "titulo": titulo, "autor": autor, "ano": ano, "estado": estado}
        validar_livro(novo)
        resp = requests.post("http://localhost:5001/livros", json=novo)
        if resp.status_code != 201:
            raise Exception(f"Erro REST: {resp.text}")
        return AdicionarLivro(livro=resp.json())

class Mutation(ObjectType):
    adicionar_livro = AdicionarLivro.Field()

# Schema GraphQL
schema = graphene.Schema(query=Query, mutation=Mutation)

# App Flask
app = Flask(__name__)

@app.route("/graphql", methods=["GET", "POST"])
def graphql_server():
    if request.method == "POST":
        data = request.get_json()
        q = data.get("query")
        result = schema.execute(q)
        res = {}
        if result.errors:
            res["errors"] = [str(e) for e in result.errors]
        res["data"] = result.data
        return jsonify(res)
    # GET — só um simples manual
    return """
    <h2>GraphQL endpoint</h2>
    <p>Faz POST com {"query": "..."} para /graphql</p>
    """

if __name__ == "__main__":
    # Corrige a porta se for outra
    app.run(debug=True, port=5003)
