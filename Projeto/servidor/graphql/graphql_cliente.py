import requests

URL = "http://localhost:5003/graphql"

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
    resp = requests.post(URL, json={"query": query})
    if resp.ok:
        data = resp.json()
        if data.get("errors"):
            print("❌ Erros:", data["errors"])
        else:
            print("📚 Livros:")
            for l in data["data"]["livros"]:
                print(f"- {l['titulo']} ({l['ano']}) — {l['estado']}")
    else:
        print("❌ Falha HTTP:", resp.text)

def adicionar_livro():
    # Interacção para obter dados do livro
    try:
        id_ = int(input("ID do livro: "))
    except ValueError:
        print("❌ ID inválido. Usa um número inteiro.")
        return
    titulo = input("Título do livro: ").strip()
    autor   = input("Autor do livro: ").strip()
    try:
        ano = int(input("Ano de publicação: "))
    except ValueError:
        print("❌ Ano inválido. Usa um número inteiro.")
        return

    # Estado — escolha controlada
    print("Estado do livro:")
    print("  1. disponivel")
    print("  2. emprestado")
    est = input("Escolhe (1 ou 2): ").strip()
    if est == "1":
        estado = "disponivel"
    elif est == "2":
        estado = "emprestado"
    else:
        print("❌ Opção inválida, será usado 'disponivel'.")
        estado = "disponivel"

    mutation = f'''
    mutation {{
      adicionarLivro(
        id: {id_},
        titulo: "{titulo}",
        autor: "{autor}",
        ano: {ano},
        estado: "{estado}"
      ) {{ livro {{ id titulo }} }}
    }}
    '''

    resp = requests.post(URL, json={"query": mutation})
    if resp.ok:
        data = resp.json()
        if data.get("errors"):
            print("❌ Erros:", data["errors"])
        else:
            novo = data["data"]["adicionarLivro"]["livro"]
            print(f"✅ Adicionado: {novo['titulo']} (ID {novo['id']})")
    else:
        print("❌ Falha HTTP:", resp.text)

if __name__ == "__main__":
    print("1. Listar livros")
    print("2. Adicionar livro")
    escolha = input("Escolhe opção: ").strip()

    if escolha == "1":
        listar_livros()
    elif escolha == "2":
        adicionar_livro()
    else:
        print("❌ Opção inválida.")
