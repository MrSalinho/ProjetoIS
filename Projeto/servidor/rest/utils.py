import json
from jsonschema import validate, ValidationError

def carregar_livros():
    with open("livros.json", "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_livros(lista):
    with open("livros.json", "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=2, ensure_ascii=False)

def validar_livro(dados):
    with open("schema.json", "r", encoding="utf-8") as f:
        schema = json.load(f)
    validate(instance=dados, schema=schema)
