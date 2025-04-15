import graphene

class Livro(graphene.ObjectType):
    id = graphene.Int()
    titulo = graphene.String()
    autor = graphene.String()
    ano = graphene.Int()
    genero = graphene.String()

class Query(graphene.ObjectType):
    livros = graphene.List(Livro)

    def resolve_livros(root, info):
        import json
        with open("livros.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Livro(**livro) for livro in data]

class CriarLivro(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        titulo = graphene.String()
        autor = graphene.String()
        ano = graphene.Int()
        genero = graphene.String()

    ok = graphene.Boolean()
    livro = graphene.Field(lambda: Livro)

    def mutate(root, info, id, titulo, autor, ano, genero):
        novo = {
            "id": id,
            "titulo": titulo,
            "autor": autor,
            "ano": ano,
            "genero": genero
        }

        import json
        with open("livros.json", "r+", encoding="utf-8") as f:
            data = json.load(f)
            data.append(novo)
            f.seek(0)
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.truncate()

        return CriarLivro(livro=Livro(**novo), ok=True)

class Mutation(graphene.ObjectType):
    criar_livro = CriarLivro.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
