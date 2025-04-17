import grpc
from concurrent import futures
import time

import client_pb2
import client_pb2_grpc

# Implementação do serviço ClientService
class ClientServiceServicer(client_pb2_grpc.ClientServiceServicer):
    def SayHello(self, request, context):
        # Implementação do método SayHello
        response = client_pb2.HelloResponse()
        response.message = f"Olá, {request.name}!"
        return response

# Função para iniciar o servidor
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    client_pb2_grpc.add_ClientServiceServicer_to_server(ClientServiceServicer(), server)

    # Escuta na porta 50051
    print("Servidor gRPC a ouvir na porta 50051...")
    server.add_insecure_port('[::]:50051')
    server.start()

    try:
        while True:
            time.sleep(60 * 60 * 24)  # O servidor vai correr durante 24h (ou até ser parado)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
