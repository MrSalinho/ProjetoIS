import grpc
from concurrent import futures
import time
import json
import livro_pb2
import livro_pb2_grpc
import requests  # Import requests for REST calls

class LivroService(livro_pb2_grpc.LivroServiceServicer):
    def AdicionarLivro(self, request, context):
        novo = {
            "id": request.id,
            "titulo": request.titulo,
            "autor": request.autor,
            "ano": request.ano,
            "genero": request.genero
        }

        # Call REST service to add a book
        response = requests.post("http://localhost:5000/livros", json=novo)
        return livro_pb2.Resposta(mensagem=response.json().get("msg", "Livro adicionado com sucesso."))

    def ListarLivros(self, request, context):
        try:
            response = requests.get("http://localhost:5000/livros")
            data = response.json()
            for l in data:
                yield livro_pb2.Livro(**l)
        except requests.exceptions.RequestException as e:
            context.set_details(f"Erro ao chamar o serviço REST: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    livro_pb2_grpc.add_LivroServiceServicer_to_server(LivroService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Servidor gRPC em execução na porta 50051...")
    try:
        while True:
            time.sleep(86400)  # O servidor vai ficar a correr indefinidamente
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()
