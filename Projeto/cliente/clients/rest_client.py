import requests
import json

class RestClient:
    def __init__(self):
        self.base_url = "http://localhost:5000"

    def listar_livros(self):
        response = requests.get(f"{self.base_url}/livros")
        if response.status_code == 200:
            livros = response.json()
            print("\n=== Livros (REST) ===")
            for livro in livros:
                print(f"ID: {livro['id']} - {livro['titulo']} por {livro['autor']}")
        else:
            print(f"Erro: {response.text}")

    def adicionar_livro(self):
        livro = {
            "id": int(input("ID: ")),
            "titulo": input("Título: "),
            "autor": input("Autor: "),
            "ano": int(input("Ano: ")),
            "estado": input("Estado (disponivel/emprestado): ")
        }
        response = requests.post(f"{self.base_url}/livros", json=livro)
        print("Livro adicionado com sucesso!" if response.status_code == 201 else f"Erro: {response.text}")

    def exportar_json(self):
        response = requests.get(f"{self.base_url}/export/json")
        if response.status_code == 200:
            with open("export_rest.json", "w") as f:
                json.dump(response.json(), f, indent=2)
            print("Dados exportados para export_rest.json")
        else:
            print(f"Erro: {response.text}")

    def exportar_xml(self):
        response = requests.get(f"{self.base_url}/export/xml")
        if response.status_code == 200:
            with open("export_rest.xml", "w") as f:
                f.write(response.text)
            print("Dados exportados para export_rest.xml")
        else:
            print(f"Erro: {response.text}") 