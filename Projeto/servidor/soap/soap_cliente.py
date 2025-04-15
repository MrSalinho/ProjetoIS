# cliente/soap_cliente.py

from zeep import Client
from zeep.exceptions import Fault

WSDL_URL = "http://localhost:5002/?wsdl"  # ajusta este URL conforme o teu servidor

client = Client(WSDL_URL)

def listar_livros():
    try:
        livros = client.service.listar_livros()
        print("📚 Lista de livros SOAP:")
        for livro in livros:
            print(f"- {livro['titulo']} (ID: {livro['id']})")
    except Fault as e:
        print("❌ Erro ao listar livros:", e)

def adicionar_livro():
    novo_livro = {
        "id": 3,
        "titulo": "Livro SOAP",
        "autor": "Autor SOAP",
        "ano": 2025
    }
    try:
        resultado = client.service.adicionar_livro(novo_livro)
        if resultado:
            print("✅ Livro adicionado com sucesso.")
        else:
            print("⚠️ Livro já existe ou erro no servidor.")
    except Fault as e:
        print("❌ Erro ao adicionar livro:", e)

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
