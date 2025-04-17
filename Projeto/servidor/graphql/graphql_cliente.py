from flask import Flask
from graphene import Schema, ObjectType, String, Int, Field, Mutation
from graphene import Boolean
from graphene import List
from graphene import View
from graphene import GraphQLView

class Livro(ObjectType):
    id = Int()
    titulo = String()
    autor = String()
    ano = Int()
    estado = String()

livros = [
    Livro(id=1, titulo="Livro 1", autor="Autor 1", ano=2001, estado="disponivel"),
    Livro(id=2, titulo="Livro 2", autor="Autor 2", ano=2002, estado="emprestado"),
]

class Query(ObjectType):
    livros = List(Livro)

    def resolve_livros(self, info):
        return livros

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

class Mutation(ObjectType):
    adicionar_livro = AdicionarLivro.Field()

schema = Schema(query=Query, mutation=Mutation)

app = Flask(__name__)

# Use GraphQLView from graphene directly
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema))

if __name__ == '__main__':
    app.run(debug=True, port=5003)
