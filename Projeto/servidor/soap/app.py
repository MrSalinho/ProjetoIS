from spyne import Application, rpc, ServiceBase, Integer, Unicode, Iterable
from spyne.model.complex import ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import os, json, logging

# Configuração de log para facilitar a depuração
logging.basicConfig(level=logging.DEBUG)

# Definir caminho para o ficheiro JSON
BASE_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(BASE_DIR, 'livros.json')

# Modelo Spyne para o tipo Livro
class Livro(ComplexModel):
    __namespace__ = 'http://example.com/livros'
    id = Integer
    titulo = Unicode
    autor = Unicode
    ano = Integer
    estado = Unicode

# Serviço SOAP
class LivroService(ServiceBase):
    @rpc(_returns=Iterable(Livro))
    def listar_livros(ctx):
        try:
            with open(DATA_FILE) as f:
                livros = json.load(f)
            logging.debug(f"Livros carregados: {livros}")
        except FileNotFoundError:
            livros = []
            logging.error(f"Ficheiro {DATA_FILE} não encontrado.")
        except json.JSONDecodeError:
            livros = []
            logging.error(f"Erro ao decodificar o ficheiro JSON.")
        
        if not livros:
            logging.warning("Nenhum livro encontrado.")
        
        # Garantir que estamos a iterar mesmo que a lista esteja vazia
        for l in livros:
            l.setdefault('estado', 'disponivel')
        
        if livros:
            for l in livros:
                yield Livro(**l)
        else:
            yield Livro(id=-1, titulo="Nenhum livro", autor="Desconhecido", ano=0, estado="indisponível")

    @rpc(Livro, _returns=Livro)
    def adicionar_livro(ctx, novo: Livro):
        try:
            with open(DATA_FILE) as f:
                livros = json.load(f)
        except FileNotFoundError:
            livros = []
        record = {
            'id': novo.id,
            'titulo': novo.titulo,
            'autor': novo.autor,
            'ano': novo.ano,
            'estado': novo.estado or 'disponivel'
        }
        livros.append(record)
        with open(DATA_FILE, 'w') as f:
            json.dump(livros, f, indent=2)
        return Livro(**record)

    @rpc(Integer, Livro, _returns=Livro)
    def atualizar_livro(ctx, id, dados: Livro):
        try:
            with open(DATA_FILE) as f:
                livros = json.load(f)
        except FileNotFoundError:
            raise ValueError('Nenhum livro disponível')
        for i, l in enumerate(livros):
            if l['id'] == id:
                updated = {
                    'id': id,
                    'titulo': dados.titulo,
                    'autor': dados.autor,
                    'ano': dados.ano,
                    'estado': dados.estado or l.get('estado', 'disponivel')
                }
                livros[i] = updated
                with open(DATA_FILE, 'w') as f:
                    json.dump(livros, f, indent=2)
                return Livro(**updated)
        raise ValueError('Livro não encontrado')

    @rpc(Integer, _returns=Unicode)
    def apagar_livro(ctx, id):
        try:
            with open(DATA_FILE) as f:
                livros = json.load(f)
        except FileNotFoundError:
            raise ValueError('Nenhum livro disponível')
        novos = [l for l in livros if l['id'] != id]
        if len(novos) == len(livros):
            raise ValueError('Livro não encontrado')
        with open(DATA_FILE, 'w') as f:
            json.dump(novos, f, indent=2)
        return 'Livro apagado com sucesso'

# Configuração da aplicação SOAP
soap_app = Application(
    [LivroService],
    tns='http://example.com/livros',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

# Arranque do servidor
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    wsgi_app = WsgiApplication(soap_app)
    server = make_server('0.0.0.0', 5001, wsgi_app)
    print('SOAP server disponível em http://0.0.0.0:5001/?wsdl')
    server.serve_forever()
