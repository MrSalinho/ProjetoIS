import graphene
import json
import dicttoxml
import xmltodict
from jsonpath_ng import parse

# Supondo que as funções ler_livros, validar_livro e escrever_livros já estejam implementadas

class Query(graphene.ObjectType):
    # ... queries existentes ...
    export_json = graphene.String(description="Exportar dados como JSON")
    export_xml = graphene.String(description="Exportar dados como XML")

    def resolve_export_json(self, info):
        livros = ler_livros()
        return json.dumps(livros, indent=2)

    def resolve_export_xml(self, info):
        livros = ler_livros()
        return dicttoxml.dicttoxml(livros, custom_root='livros', attr_type=False).decode()

class ImportData(graphene.Mutation):
    class Arguments:
        format = graphene.String()
        data = graphene.String()

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, format, data):
        try:
            if format == "json":
                livros = json.loads(data)
            elif format == "xml":
                dict_data = xmltodict.parse(data)
                livros = dict_data['livros']['livro']
            else:
                return ImportData(success=False, message="Formato não suportado")

            for livro in livros:
                validar_livro(livro)
            escrever_livros(livros)
            return ImportData(success=True, message="Importação concluída")
        except Exception as e:
            return ImportData(success=False, message=str(e))

class Mutation(graphene.ObjectType):
    import_data = ImportData.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)