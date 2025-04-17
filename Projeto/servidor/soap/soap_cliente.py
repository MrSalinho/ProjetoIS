from zeep import Client
from zeep.exceptions import Fault
import os

# URL do WSDL do serviço SOAP
WSDL_URL = 'http://localhost:5004/?wsdl' 

client = Client(WSDL_URL)

def listar_livros():
    try:
        livros = client.service.listar_livros()
        print('📚 Lista de livros SOAP:')
        for livro in livros:
            print(f"- {livro.titulo} (ID: {livro.id}, Estado: {livro.estado})")
    except Fault as e:
        print('❌ Erro ao listar livros:', e)

def adicionar_livro():
    try:
        id_ = int(input('ID do livro: '))
        titulo = input('Título do livro: ')
        autor = input('Autor do livro: ')
        ano = int(input('Ano de publicação: '))
        estado = input('Estado (disponivel/emprestado): ')

        novo = client.service.adicionar_livro(
            id_, titulo, autor, ano, estado
        )
        print(f"✅ Adicionado: {novo.titulo} (ID {novo.id})")
    except Fault as e:
        print('❌ Erro ao adicionar livro:', e)
    except ValueError:
        print('❌ Valor inválido para ID ou Ano.')

if __name__ == '__main__':
    print('1. Listar livros')
    print('2. Adicionar livro')
    opcao = input('Escolhe opção: ')
    if opcao == '1':
        listar_livros()
    elif opcao == '2':
        adicionar_livro()
    else:
        print('❌ Opção inválida.')
