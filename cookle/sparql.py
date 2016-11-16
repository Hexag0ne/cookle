# coding=utf-8
from SPARQLWrapper import SPARQLWrapper, JSON

def getNomAnglais(uri):
    """Permet de récupérer le nom des ingrédients en français à partir des uri de la ressource en anglais"""
    spar = SPARQLWrapper("http://dbpedia.org/sparql")
    spar.setQuery("""
    SELECT ?label WHERE { """ + uri + 
    """    rdfs:label ?label
    FILTER (lang(?label) = "en")
    } """)
    spar.setReturnFormat(JSON)
    res = spar.query().convert()
    if len(res["results"]["bindings"]) == 0:
        return None
    return res["results"]["bindings"][0]["label"]["value"]

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
        return getNomAnglais(uri)
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
    if len(res["results"]["bindings"]) == 0:
        return None
    # description can be None
    return res["results"]["bindings"][0]["comment"]["value"]

def getImage(uri):
    """Permet de récupérer l'image d'un ingrédient ou une recette """
    spar = SPARQLWrapper("http://dbpedia.org/sparql")
    uri = "<{}>".format(uri)
    spar.setQuery("""
    SELECT * WHERE { """ + uri + 
    """  <http://dbpedia.org/ontology/thumbnail> ?o
    } """)
    spar.setReturnFormat(JSON)
    res = spar.query().convert()
    if len(res["results"]["bindings"]) == 0:
        return None
    return res["results"]["bindings"][0]["o"]["value"]

def getTypeRecette(uri):
    """Permet de récupérer le type de la recette """
    spar = SPARQLWrapper("http://dbpedia.org/sparql")
    uri = "<{}>".format(uri)
    spar.setQuery("""
    SELECT * WHERE { """ + uri + 
    """  <http://dbpedia.org/ontology/type> ?o
    } """)
    spar.setReturnFormat(JSON)
    res = spar.query().convert()
    if len(res["results"]["bindings"]) == 0:
        return None
    return res["results"]["bindings"][0]["o"]["value"]

def getRecetteSimilaire(uri):
    """Permet de récupérer les recettes similaires"""
    if not uri:
        return None
    spar = SPARQLWrapper("http://dbpedia.org/sparql")
    uri = "<{}>".format(uri)
    spar.setQuery("""
    SELECT * WHERE {  ?s <http://dbpedia.org/ontology/type> """ + uri + 
    """ 
    } """)
    spar.setReturnFormat(JSON)
    res = spar.query().convert()
    list_recettes_similaires=[]
    if len(res["results"]["bindings"]) == 0:
        return None
    for i in range(0,5):
        nom_recette = getNomFrancais(res["results"]["bindings"][i]["s"]["value"] )
        image_recette = getImage(res["results"]["bindings"][i]["s"]["value"] )
        list_recettes_similaires.append(dict(nom_recette=nom_recette,image_recette=image_recette))

    recettes_similaire=dict(similar_recipes=list_recettes_similaires)
    return recettes_similaire 

if __name__ == "__main__":
    # do stuff if : python sparql.py
    print(getDescription("http://dbpedia.org/resource/Tajine","en"))
    print(getNomFrancais("http://dbpedia.org/resource/Soup"))


