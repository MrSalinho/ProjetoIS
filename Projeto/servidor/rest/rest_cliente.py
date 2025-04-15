# cliente/rest_cliente.py

import requests
import json

BASE_URL = "http://localhost:5001/livros"  # ajusta conforme o teu serviço REST

def listar_livros():
    resposta = requests.get(BASE_URL)
    if resposta.status_code == 200:
        livros = resposta.json()
        print("📚 Lista de livros:")
        for livro in livros:
            print(f"- {livro['titulo']} (ID: {livro['id']})")
    else:
        print("❌ Erro ao obter livros:", resposta.text)

def criar_livro():
    novo_livro = {
        "id": 3,
        "titulo": "Novo Livro REST",
        "autor": "Autor X",
        "ano": 2024
    }
    resposta = requests.post(BASE_URL, json=novo_livro)
    if resposta.status_code == 201:
        print("✅ Livro criado com sucesso.")
    else:
        print("❌ Erro ao criar livro:", resposta.text)

def exportar_json(ficheiro_saida="exportado_rest.json"):
    resposta = requests.get(BASE_URL)
    if resposta.status_code == 200:
        with open(ficheiro_saida, "w", encoding="utf-8") as f:
            json.dump(resposta.json(), f, indent=4, ensure_ascii=False)
        print(f"✅ Dados exportados para {ficheiro_saida}")
    else:
        print("❌ Erro ao exportar:", resposta.text)

def importar_json(ficheiro_entrada="importar_rest.json"):
    try:
        with open(ficheiro_entrada, "r", encoding="utf-8") as f:
            livros = json.load(f)
        for livro in livros:
            resposta = requests.post(BASE_URL, json=livro)
            if resposta.status_code != 201:
                print(f"❌ Erro ao importar livro {livro['id']}: {resposta.text}")
        print("✅ Importação concluída.")
    except Exception as e:
        print("❌ Erro ao importar ficheiro:", str(e))

if __name__ == "__main__":
    print("1. Listar livros")
    print("2. Criar livro")
    print("3. Exportar para JSON")
    print("4. Importar de JSON")
    escolha = input("Escolhe uma opção: ")

    if escolha == "1":
        listar_livros()
    elif escolha == "2":
        criar_livro()
    elif escolha == "3":
        exportar_json()
    elif escolha == "4":
        importar_json()
    else:
        print("❌ Opção inválida.")
