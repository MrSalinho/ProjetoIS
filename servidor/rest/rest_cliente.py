import requests
import json

BASE_URL = "http://localhost:5000/livros"

def listar_livros():
    try:
        resposta = requests.get(BASE_URL)
        if resposta.status_code == 200:
            livros = resposta.json()
            print("\n📚 Lista de livros:")
            for livro in livros:
                print(f"- {livro['titulo']} por {livro['autor']} ({livro['ano']}) - {livro['estado']}")
        else:
            print("❌ Erro ao obter livros:", resposta.text)
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Servidor não está rodando na porta 5000")

def criar_livro():
    novo_livro = {
        "id": int(input("ID: ")),
        "titulo": input("Título: "),
        "autor": input("Autor: "),
        "ano": int(input("Ano: ")),
        "estado": "disponivel"
    }
    
    try:
        resposta = requests.post(BASE_URL, json=novo_livro)
        if resposta.status_code == 201:
            print("✅ Livro criado com sucesso!")
        else:
            print("❌ Erro ao criar livro:", resposta.text)
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Servidor não está rodando na porta 5000")

def exportar_json():
    try:
        resposta = requests.get(f"{BASE_URL}/export/json")
        if resposta.status_code == 200:
            with open("livros_exportados.json", "w", encoding="utf-8") as f:
                json.dump(resposta.json(), f, indent=2, ensure_ascii=False)
            print("✅ Livros exportados para livros_exportados.json")
        else:
            print("❌ Erro ao exportar:", resposta.text)
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Servidor não está rodando ou não acessível")

def importar_json():
    try:
        with open("livros_exportados.json", "r", encoding="utf-8") as f:
            livros = json.load(f)
        
        resposta = requests.post(f"{BASE_URL}/import/json", json=livros)
        if resposta.status_code == 200:
            print("✅ Livros importados com sucesso!")
        else:
            print("❌ Erro ao importar:", resposta.text)
    except FileNotFoundError:
        print("❌ Arquivo livros_exportados.json não encontrado")
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Servidor não está rodando ou não acessível")

if __name__ == "__main__":
    while True:
        print("\n=== Sistema de Gestão de Livros (REST) ===")
        print("1. Listar livros")
        print("2. Adicionar livro")
        print("3. Exportar para JSON")
        print("4. Importar de JSON")
        print("0. Sair")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "1":
            listar_livros()
        elif opcao == "2":
            criar_livro()
        elif opcao == "3":
            exportar_json()
        elif opcao == "4":
            importar_json()
        elif opcao == "0":
            print("Até logo! 👋")
            break
        else:
            print("❌ Opção inválida!") 