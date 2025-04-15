import grpc
import client_pb2
import client_pb2_grpc

# Função principal para chamar o servidor gRPC
def run():
    # Cria uma conexão com o servidor gRPC na porta 50051
    with grpc.insecure_channel('localhost:50051') as channel:
        # Cria um stub (objeto que representa o serviço)
        stub = client_pb2_grpc.ClientServiceStub(channel)

        # Cria uma mensagem de requisição
        request = client_pb2.HelloRequest(name='Mundo')

        # Chama o método SayHello do serviço
        response = stub.SayHello(request)

        # Imprime a resposta do servidor
        print(f'Resposta do servidor: {response.message}')

if __name__ == '__main__':
    run()
