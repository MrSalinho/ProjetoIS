from zeep import Client

class SOAPClient:
    def __init__(self):
        self.client = Client('http://localhost:8000/?wsdl')

    def listar_livros(self):
        try:
            livros = self.client.service.listar_livros()
            print("\n=== Livros (SOAP) ===")
            for livro in livros:
                print(f"ID: {livro.id} - {livro.titulo} por {livro.autor}")
        except Exception as e:
            print(f"Erro SOAP: {e}")

    def adicionar_livro(self):
        try:
            id = int(input("ID: "))
            titulo = input("Título: ")
            autor = input("Autor: ")
            ano = int(input("Ano: "))
            estado = input("Estado (disponivel/emprestado): ")
            
            result = self.client.service.adicionar_livro(id=id, titulo=titulo, 
                                                       autor=autor, ano=ano, 
                                                       estado=estado)
            print("Livro adicionado com sucesso!")
        except Exception as e:
            print(f"Erro SOAP: {e}") 