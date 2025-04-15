import grpc
from concurrent import futures
import time
import json
import livro_pb2
import livro_pb2_grpc

class LivroService(livro_pb2_grpc.LivroServiceServicer):
    def AdicionarLivro(self, request, context):
        novo = {
            "id": request.id,
            "titulo": request.titulo,
            "autor": request.autor,
            "ano": request.ano,
            "genero": request.genero
        }

        try:
            with open("livros.json", "r+", encoding="utf-8") as f:
                try:
                    # Tenta carregar os dados do ficheiro
                    data = json.load(f)
                except json.JSONDecodeError:
                    # Se o JSON estiver vazio ou mal formado, inicializa uma lista vazia
                    data = []

                # Adiciona o novo livro à lista
                data.append(novo)
                f.seek(0)  # Vai para o início do ficheiro
                # Grava os dados de volta no ficheiro
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.truncate()  # Elimina o conteúdo restante no ficheiro

        except FileNotFoundError:
            # Se o ficheiro não existir, cria um novo e adiciona o livro
            with open("livros.json", "w", encoding="utf-8") as f:
                json.dump([novo], f, indent=2, ensure_ascii=False)

        return livro_pb2.Resposta(mensagem="Livro adicionado com sucesso.")

    def ListarLivros(self, request, context):
        try:
            with open("livros.json", "r", encoding="utf-8") as f:
                # Carrega os livros do ficheiro
                data = json.load(f)
                # Para cada livro, cria uma resposta gRPC
                for l in data:
                    yield livro_pb2.Livro(**l)
        except FileNotFoundError:
            context.set_details("Ficheiro não encontrado.")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return []
        except json.JSONDecodeError:
            context.set_details("Erro ao ler o ficheiro JSON.")
            context.set_code(grpc.StatusCode.INTERNAL)
            return []

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
