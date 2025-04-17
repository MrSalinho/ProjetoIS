from flask import Flask
from graphene import ObjectType, String, Int, List, Field, Mutation, Schema
from graphene import JSON
import json

app = Flask(__name__)

# Modelo Livro (Graphene ObjectType)
class Livro(ObjectType):
    id = Int()
    titulo = String()
    autor = String()
    ano = Int()
    genero = String()

# Mutation para Adicionar Livro
class AdicionarLivro(Mutation):
    class Arguments:
        id = Int()
        titulo = String()
        autor = String()
        ano = Int()
        genero = String()

    mensagem = String()

    def mutate(self, info, id, titulo, autor, ano, genero):
        novo_livro = {
            "id": id,
            "titulo": titulo,
            "autor": autor,
            "ano": ano,
            "genero": genero
        }

        # Atualiza o arquivo JSON
        with open("livros.json", "r+", encoding="utf-8") as f:
            data = json.load(f)
            data.append(novo_livro)
            f.seek(0)
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.truncate()

        return AdicionarLivro(mensagem="Livro adicionado com sucesso.")

# Query para listar livros
class Query(ObjectType):
    livros = List(Livro)

    def resolve_livros(self, info):
        with open("livros.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Livro(**livro) for livro in data]

# Definindo o Schema
class Mutation(ObjectType):
    adicionar_livro = AdicionarLivro.Field()

# Definindo o Schema do GraphQL
schema = Schema(query=Query, mutation=Mutation)

# Rota para GraphQL
from flask_graphql import GraphQLView
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == '__main__':
    app.run(debug=True, port=5002)
