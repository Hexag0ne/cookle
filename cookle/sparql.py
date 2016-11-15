from SPARQLWrapper import SPARQLWrapper, JSON


def test():
	print(getDescription("<http://dbpedia.org/resource/Tajine>","en"))
	print(getDescription("<http://dbpedia.org/resource/Tajine>","fr"))



def getDescription(uri,langue="fr"):
	"""Permet de récupérer la description d'une ressource dbpedia dans la langue souhaitée """
	spar = SPARQLWrapper("http://dbpedia.org/sparql")
	spar.setQuery("""
	SELECT ?comment WHERE { """ + uri + 
	"""	rdfs:comment ?comment
	FILTER (lang(?comment) = '""" + langue + """')
	} """)
	spar.setReturnFormat(JSON)
	resul = spar.query().convert()

	return resul["results"]["bindings"][0]["comment"]["value"]


