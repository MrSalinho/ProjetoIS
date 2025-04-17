import grpc
import livro_pb2
import livro_pb2_grpc

def run():
    canal = grpc.insecure_channel('localhost:50051')
    cliente = livro_pb2_grpc.LivroServiceStub(canal)

    # Adicionar um livro
    livro_novo = livro_pb2.Livro(
        id=1,
        titulo="O Senhor dos Anéis",
        autor="J.R.R. Tolkien"
    )
    resposta = cliente.AdicionarLivro(livro_novo)
    print("Resposta ao adicionar livro:", resposta.mensagem)

    # Listar livros
    print("\nLista de livros no servidor:")
    for livro in cliente.ListarLivros(livro_pb2.Vazio()):
        print(f"{livro.id} - {livro.titulo} ({livro.autor})")

if __name__ == '__main__':
    run()
