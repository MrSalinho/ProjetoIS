# cliente/graphql_cliente.py

import requests

URL = "http://localhost:5003/graphql"  # ajusta se for diferente

def listar_livros():
    query = """
    query {
        livros {
            id
            titulo
            autor
            ano
        }
    }
    """
    resposta = requests.post(URL, json={'query': query})
    if resposta.status_code == 200:
        dados = resposta.json()
        livros = dados["data"]["livros"]
        print("📚 Lista de livros GraphQL:")
        for livro in livros:
            print(f"- {livro['titulo']} ({livro['ano']})")
    else:
        print("❌ Erro ao obter livros:", resposta.text)

def adicionar_livro():
    mutation = """
    mutation {
        adicionarLivro(id: 4, titulo: "Livro GraphQL", autor: "Autor QL", ano: 2025) {
            id
            titulo
        }
    }
    """
    resposta = requests.post(URL, json={'query': mutation})
    if resposta.status_code == 200:
        print("✅ Livro adicionado com sucesso.")
    else:
        print("❌ Erro ao adicionar livro:", resposta.text)

if __name__ == "__main__":
    print("1. Listar livros")
    print("2. Adicionar livro")
    escolha = input("Escolhe uma opção: ")

    if escolha == "1":
        listar_livros()
    elif escolha == "2":
        adicionar_livro()
    else:
        print("❌ Opção inválida.")
