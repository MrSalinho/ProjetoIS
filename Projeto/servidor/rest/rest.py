from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/livros', methods=['GET'])
def listar_livros():
    with open("livros.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/livros', methods=['POST'])
def adicionar_livro():
    novo_livro = request.get_json()

    with open("livros.json", "r+", encoding="utf-8") as f:
        data = json.load(f)
        data.append(novo_livro)
        f.seek(0)
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.truncate()

    return jsonify({"mensagem": "Livro adicionado com sucesso."}), 201

if __name__ == "__main__":
    app.run(debug=True, port=5000)
