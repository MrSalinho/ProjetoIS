from spyne import Application, ServiceBase, rpc, Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import json
from wsgiref.simple_server import make_server

class LivroService(ServiceBase):
    @rpc(Integer, Unicode, Unicode, Integer, Unicode, _returns=Unicode)
    def AdicionarLivro(self, id, titulo, autor, ano, genero):
        novo_livro = {
            "id": id,
            "titulo": titulo,
            "autor": autor,
            "ano": ano,
            "genero": genero
        }

        # Atualiza o arquivo JSON
        with open("livros.json", "r+", encoding="utf-8") as f:
            data = json.load(f)
            data.append(novo_livro)
            f.seek(0)
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.truncate()

        return "Livro adicionado com sucesso."

    @rpc(_returns=Unicode)
    def ListarLivros(self):
        with open("livros.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        livros = ""
        for livro in data:
            livros += f"ID: {livro['id']}, Título: {livro['titulo']}, Autor: {livro['autor']}, Ano: {livro['ano']}, Gênero: {livro['genero']}\n"

        return livros

# Criando a aplicação SOAP
application = Application([LivroService], tns='spyne.examples.soap', in_protocol=Soap11(), out_protocol=Soap11())

# Configurando o servidor WSGI
wsgi_application = WsgiApplication(application)

if __name__ == '__main__':
    # Executando o servidor SOAP na porta 8000
    server = make_server('localhost', 8000, wsgi_application)
    print("Servidor SOAP rodando na porta 8000...")
    server.serve_forever()
