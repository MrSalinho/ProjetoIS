import grpc
from concurrent import futures
import json
import dicttoxml
import livro_pb2
import livro_pb2_grpc

class LivroServicer(livro_pb2_grpc.LivroServiceServicer):
    def StreamLivros(self, request, context):
        try:
            with open('livros.json', 'r') as f:
                livros = json.load(f)
            for livro in livros:
                yield livro_pb2.Livro(**livro)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))

    def ImportarLivrosStream(self, request_iterator, context):
        livros = []
        try:
            for livro in request_iterator:
                livros.append({
                    'id': livro.id,
                    'titulo': livro.titulo,
                    'autor': livro.autor,
                    'ano': livro.ano,
                    'estado': livro.estado
                })
            with open('livros.json', 'w') as f:
                json.dump(livros, f, indent=2)
            return livro_pb2.ImportResponse(success=True, message="Importação concluída")
        except Exception as e:
            return livro_pb2.ImportResponse(success=False, message=str(e))

    def ExportarJSON(self, request, context):
        try:
            with open('livros.json', 'r') as f:
                data = f.read()
            return livro_pb2.ExportResponse(data=data, format='json')
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))

    def ExportarXML(self, request, context):
        try:
            with open('livros.json', 'r') as f:
                livros = json.load(f)
            xml = dicttoxml.dicttoxml(livros, custom_root='livros', attr_type=False)
            return livro_pb2.ExportResponse(data=xml.decode(), format='xml')
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e)) 