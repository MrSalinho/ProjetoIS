import requests

class GraphQLClient:
    def __init__(self):
        self.url = "http://localhost:4000/graphql"

    def execute_query(self, query):
        response = requests.post(self.url, json={'query': query})
        if response.status_code == 200:
            return response.json()
        raise Exception(f"GraphQL Error: {response.text}")

    def listar_livros(self):
        query = """
        query {
            livros {
                id
                titulo
                autor
                ano
                estado
            }
        }
        """
        result = self.execute_query(query)
        print("\n=== Livros (GraphQL) ===")
        for livro in result['data']['livros']:
            print(f"ID: {livro['id']} - {livro['titulo']} por {livro['autor']}")

    def adicionar_livro(self):
        id = input("ID: ")
        titulo = input("Título: ")
        autor = input("Autor: ")
        ano = input("Ano: ")
        estado = input("Estado (disponivel/emprestado): ")

        mutation = f"""
        mutation {{
            adicionarLivro(livro: {{
                id: {id},
                titulo: "{titulo}",
                autor: "{autor}",
                ano: {ano},
                estado: "{estado}"
            }}) {{
                id
                titulo
            }}
        }}
        """
        result = self.execute_query(mutation)
        print("Livro adicionado com sucesso!") 