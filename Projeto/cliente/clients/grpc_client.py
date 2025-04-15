import grpc
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from servidor.grpc import livro_pb2
from servidor.grpc import livro_pb2_grpc

class GRPCClient:
    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = livro_pb2_grpc.LivroServiceStub(self.channel)

    def listar_livros(self):
        try:
            response = self.stub.ListarLivros(livro_pb2.Empty())
            print("\n=== Livros (gRPC) ===")
            for livro in response.livros:
                print(f"ID: {livro.id} - {livro.titulo} por {livro.autor}")
        except grpc.RpcError as e:
            print(f"Erro gRPC: {e}")

    def adicionar_livro(self):
        try:
            livro = livro_pb2.Livro(
                id=int(input("ID: ")),
                titulo=input("Título: "),
                autor=input("Autor: "),
                ano=int(input("Ano: ")),
                estado=input("Estado (disponivel/emprestado): ")
            )
            response = self.stub.AdicionarLivro(livro)
            print("Livro adicionado com sucesso!")
        except grpc.RpcError as e:
            print(f"Erro gRPC: {e}") 