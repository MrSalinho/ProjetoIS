from lxml import etree

def carregar_livros_xml(ficheiro="livros.xml"):
    with open(ficheiro, "rb") as f:
        return etree.parse(f)

def guardar_livros_xml(tree, ficheiro="livros.xml"):
    with open(ficheiro, "wb") as f:
        tree.write(f, pretty_print=True, xml_declaration=True, encoding="UTF-8")

def validar_xml(xml_path, xsd_path):
    with open(xsd_path, "rb") as f:
        schema_root = etree.XML(f.read())
    schema = etree.XMLSchema(schema_root)
    xml_doc = etree.parse(xml_path)
    return schema.validate(xml_doc)
