import grpc
import livro_pb2
import livro_pb2_grpc

def run():
    # Cria uma conexão com o servidor gRPC na porta 50051
    with grpc.insecure_channel('localhost:50051') as channel:
        # Cria um stub (objeto que representa o serviço)
        stub = livro_pb2_grpc.LivroServiceStub(channel)

        # Exemplo de adicionar um livro
        livro = livro_pb2.Livro(id=3, titulo="Harry Potter", autor="J.K. Rowling", ano=1997, genero="Fantasia")
        resposta = stub.AdicionarLivro(livro)
        print(f"Resposta do servidor: {resposta.mensagem}")

        # Exemplo de listar livros
        for livro in stub.ListarLivros(livro_pb2.Vazio()):
            print(f"Livro ID: {livro.id}, Título: {livro.titulo}, Autor: {livro.autor}, Ano: {livro.ano}, Gênero: {livro.genero}")

if __name__ == '__main__':
    run()
