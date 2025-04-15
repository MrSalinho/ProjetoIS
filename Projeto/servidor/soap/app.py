from spyne import Application, rpc, ServiceBase, Integer, Unicode, Iterable, ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import json
import os
from lxml import etree

# Caminho dos ficheiros
DADOS_PATH = os.path.join(os.path.dirname(__file__), '../data/livros.json')
XSD_PATH = os.path.join(os.path.dirname(__file__), 'livro.xsd')

# Modelo de Livro
class Livro(ComplexModel):
    id = Integer
    titulo = Unicode
    autor = Unicode
    ano = Integer
    estado = Unicode

def ler_livros():
    with open(DADOS_PATH) as f:
        return json.load(f)

def escrever_livros(livros):
    with open(DADOS_PATH, 'w') as f:
        json.dump(livros, f, indent=2)

def validar_xml(xml_str):
    xml_doc = etree.fromstring(xml_str)
    with open(XSD_PATH, 'rb') as f:
        schema_doc = etree.XML(f.read())
    schema = etree.XMLSchema(schema_doc)
    return schema.validate(xml_doc)

class LivroService(ServiceBase):
    @rpc(_returns=Iterable(Livro))
    def listar_livros(ctx):
        livros = ler_livros()
        for l in livros:
            yield Livro(**l)

    @rpc(Livro, _returns=Unicode)
    def adicionar_livro(ctx, livro):
        livros = ler_livros()
        livros.append(dict(livro))
        escrever_livros(livros)
        return "Livro adicionado"

    @rpc(Integer, Livro, _returns=Unicode)
    def atualizar_livro(ctx, id, livro):
        livros = ler_livros()
        for i, l in enumerate(livros):
            if l['id'] == id:
                livros[i] = dict(livro)
                escrever_livros(livros)
                return "Livro atualizado"
        return "Livro não encontrado"

    @rpc(Integer, _returns=Unicode)
    def apagar_livro(ctx, id):
        livros = ler_livros()
        livros_novos = [l for l in livros if l['id'] != id]
        if len(livros_novos) == len(livros):
            return "Livro não encontrado"
        escrever_livros(livros_novos)
        return "Livro apagado"

    @rpc(_returns=Unicode)
    def exportar_xml(ctx):
        with open(DADOS_PATH) as f:
            livros = json.load(f)
        # Exportar para XML manualmente (simples)
        livros_xml = "<livros>" + "".join([
            f"<livro><id>{l['id']}</id><titulo>{l['titulo']}</titulo><autor>{l['autor']}</autor><ano>{l['ano']}</ano><estado>{l['estado']}</estado></livro>"
            for l in livros
        ]) + "</livros>"
        return livros_xml

    @rpc(Unicode, _returns=Unicode)
    def importar_xml(ctx, xml_data):
        # Validação XSD
        if not validar_xml(xml_data.encode()):
            return "XML inválido"
        root = etree.fromstring(xml_data.encode())
        livros = []
        for livro_elem in root.findall('livro'):
            livro = {
                'id': int(livro_elem.find('id').text),
                'titulo': livro_elem.find('titulo').text,
                'autor': livro_elem.find('autor').text,
                'ano': int(livro_elem.find('ano').text),
                'estado': livro_elem.find('estado').text
            }
            livros.append(livro)
        escrever_livros(livros)
        return "Importação concluída"

app = Application([LivroService], 'livros.soap',
                  in_protocol=Soap11(validator='lxml'),
                  out_protocol=Soap11())
wsgi_app = WsgiApplication(app)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    print("SOAP server running on http://0.0.0.0:8000")
    make_server('0.0.0.0', 8000, wsgi_app).serve_forever()
