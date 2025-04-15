from spyne import Application, rpc, ServiceBase, Unicode, Integer
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from utils import carregar_livros_xml, guardar_livros_xml, validar_xml
from lxml import etree

class LivroService(ServiceBase):
    @rpc(Integer, Unicode, Unicode, Integer, Unicode, _returns=Unicode)
    def adicionar_livro(ctx, id, titulo, autor, ano, genero):
        if not validar_xml("livros.xml", "schema.xsd"):
            return "XML inválido antes da adição."

        tree = carregar_livros_xml()
        root = tree.getroot()

        novo = etree.Element("livro")
        etree.SubElement(novo, "id").text = str(id)
        etree.SubElement(novo, "titulo").text = titulo
        etree.SubElement(novo, "autor").text = autor
        etree.SubElement(novo, "ano").text = str(ano)
        etree.SubElement(novo, "genero").text = genero

        root.append(novo)
        guardar_livros_xml(tree)

        if validar_xml("livros.xml", "schema.xsd"):
            return "Livro adicionado com sucesso."
        else:
            return "Livro adicionado mas XML inválido."

soap_app = Application([LivroService],
                       tns="livros.soap.exemplo",
                       in_protocol=Soap11(validator='lxml'),
                       out_protocol=Soap11())

if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    wsgi_app = WsgiApplication(soap_app)
    server = make_server("0.0.0.0", 8000, wsgi_app)
    print("SOAP server disponível em http://localhost:8000")
    server.serve_forever()
