# coding=utf-8
from SPARQLWrapper import SPARQLWrapper, JSON

def getNomFrancais(uri):
    """Permet de récupérer le nom des ingrédients en français à partir des uri de la ressource en anglais"""
    spar = SPARQLWrapper("http://dbpedia.org/sparql")
    uri = "<{}>".format(uri)
    spar.setQuery("""
    SELECT ?label WHERE { """ + uri + 
    """    rdfs:label ?label
    FILTER (lang(?label) = "fr")
    } """)
    spar.setReturnFormat(JSON)
    res = spar.query().convert()
    if len(res["results"]["bindings"]) == 0:
        return None
    return res["results"]["bindings"][0]["label"]["value"]

def getDescription(uri, langue="fr"):
    """Permet de récupérer le nom des ingrédients en français à partir des uri de la ressource en anglais"""
    spar = SPARQLWrapper("http://dbpedia.org/sparql")
    uri = "<{}>".format(uri)
    spar.setQuery("""
    SELECT ?comment WHERE { """ + uri + 
    """    rdfs:comment ?comment
    FILTER (lang(?comment) = '""" + langue + """')
    } """)
    spar.setReturnFormat(JSON)
    res = spar.query().convert()
    print(res)
    if len(res["results"]["bindings"]) == 0:
        return None
    # description can be None
    return res["results"]["bindings"][0]["comment"]["value"]

if __name__ == "__main__":
    # do stuff if : python sparql.py
    print(getDescription("http://dbpedia.org/resource/Tajine","en"))
    print(getNomFrancais("http://dbpedia.org/resource/Soup"))