from flask import Flask
import graphene
from graphene import ObjectType, String, Int, Field, Mutation
from graphene import Schema
from flask_graphql import GraphQLView

# Classe para representar o Livro
class Livro(ObjectType):
    id = Int()
    titulo = String()
    autor = String()
    ano = Int()
    estado = String()

# Lista de livros em memória
livros = [
    Livro(id=1, titulo="Livro 1", autor="Autor 1", ano=2001, estado="disponivel"),
    Livro(id=2, titulo="Livro 2", autor="Autor 2", ano=2002, estado="emprestado"),
]

# Query para listar livros
class Query(ObjectType):
    livros = graphene.List(Livro)

    def resolve_livros(self, info):
        return livros

# Mútua para adicionar um livro
class AdicionarLivro(Mutation):
    class Arguments:
        id = Int()
        titulo = String()
        autor = String()
        ano = Int()
        estado = String()

    livro = Field(Livro)

    def mutate(self, info, id, titulo, autor, ano, estado):
        novo_livro = Livro(id=id, titulo=titulo, autor=autor, ano=ano, estado=estado)
        livros.append(novo_livro)
        return AdicionarLivro(livro=novo_livro)

# Classe para agrupar as mutações
class Mutations(ObjectType):
    adicionar_livro = AdicionarLivro.Field()

# Esquema GraphQL
schema = Schema(query=Query, mutation=Mutations)

# Inicializando o Flask
app = Flask(__name__)

# Configurando o endpoint do GraphQL
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema))

# Rodando o servidor
if __name__ == '__main__':
    app.run(debug=True, port=5003)
