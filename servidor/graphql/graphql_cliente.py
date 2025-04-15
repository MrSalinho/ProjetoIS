import requests

URL = "http://localhost:4000/graphql"

def listar_livros():
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
    try:
        resposta = requests.post(URL, json={'query': query})
        print(f"Status: {resposta.status_code}")
        print(f"Resposta: {resposta.text}")  # Adicionado para debug
        
        if resposta.status_code == 200:
            dados = resposta.json()
            if dados and 'data' in dados and dados['data'] and 'livros' in dados['data']:
                livros = dados['data']['livros']
                print("\n📚 Lista de livros:")
                for livro in livros:
                    print(f"- {livro['titulo']} por {livro['autor']} ({livro['ano']}) - {livro['estado']}")
            else:
                print("❌ Resposta inválida do servidor:", dados)
        else:
            print(f"❌ Erro do servidor: {resposta.status_code}")
    except Exception as e:
        print(f"❌ Erro ao conectar: {str(e)}")

def adicionar_livro():
    mutation = """
    mutation {
        adicionarLivro(livro: {
            id: 2,
            titulo: "Livro GraphQL",
            autor: "Autor GraphQL",
            ano: 2024,
            estado: "disponivel"
        }) {
            id
            titulo
            autor
            ano
            estado
        }
    }
    """
    try:
        resposta = requests.post(URL, json={'query': mutation})
        print(f"Status: {resposta.status_code}")
        print(f"Resposta: {resposta.text}")  # Adicionado para debug
        
        if resposta.status_code == 200:
            dados = resposta.json()
            if dados and 'data' in dados:
                print("✅ Livro adicionado com sucesso!")
            else:
                print("❌ Erro ao adicionar livro:", dados)
        else:
            print(f"❌ Erro do servidor: {resposta.status_code}")
    except Exception as e:
        print(f"❌ Erro ao conectar: {str(e)}")

if __name__ == "__main__":
    while True:
        print("\n=== Sistema de Gestão de Livros (GraphQL) ===")
        print("1. Listar livros")
        print("2. Adicionar livro")
        print("0. Sair")
        
        escolha = input("\nEscolha uma opção: ")
        
        if escolha == "1":
            listar_livros()
        elif escolha == "2":
            adicionar_livro()
        elif escolha == "0":
            print("Até logo! 👋")
            break
        else:
            print("❌ Opção inválida!") 