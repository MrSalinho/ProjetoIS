import sys
import os
from clients.rest_client import RestClient
from clients.graphql_client import GraphQLClient
from clients.grpc_client import GRPCClient
from clients.soap_client import SOAPClient

def mostrar_menu():
    print("\n=== Sistema de Gerenciamento de Livros ===")
    print("1. REST API")
    print("2. GraphQL")
    print("3. gRPC")
    print("4. SOAP")
    print("5. Sair")
    return input("Escolha uma opção: ")

def menu_operacoes():
    print("\n=== Operações ===")
    print("1. Listar livros")
    print("2. Adicionar livro")
    print("3. Atualizar livro")
    print("4. Apagar livro")
    print("5. Exportar (JSON)")
    print("6. Exportar (XML)")
    print("7. Importar (JSON)")
    print("8. Importar (XML)")
    print("9. Voltar")
    return input("Escolha uma operação: ")

def main():
    rest_client = RestClient()
    graphql_client = GraphQLClient()
    grpc_client = GRPCClient()
    soap_client = SOAPClient()

    while True:
        opcao = mostrar_menu()
        if opcao == "5":
            break

        cliente = None
        if opcao == "1":
            cliente = rest_client
        elif opcao == "2":
            cliente = graphql_client
        elif opcao == "3":
            cliente = grpc_client
        elif opcao == "4":
            cliente = soap_client
        else:
            print("Opção inválida!")
            continue

        while True:
            op = menu_operacoes()
            if op == "9":
                break
            try:
                if op == "1":
                    cliente.listar_livros()
                elif op == "2":
                    cliente.adicionar_livro()
                elif op == "3":
                    cliente.atualizar_livro()
                elif op == "4":
                    cliente.apagar_livro()
                elif op == "5":
                    cliente.exportar_json()
                elif op == "6":
                    cliente.exportar_xml()
                elif op == "7":
                    cliente.importar_json()
                elif op == "8":
                    cliente.importar_xml()
                else:
                    print("Opção inválida!")
            except Exception as e:
                print(f"Erro: {e}")

if __name__ == "__main__":
    main() 