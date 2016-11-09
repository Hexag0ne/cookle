from SPARQLWrapper import SPARQLWrapper, JSON

#sparql = SPARQLWrapper("http://dbpedia.org/sparql")
#sparql.setQuery("""
#    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#    SELECT ?label
#    WHERE { <http://dbpedia.org/resource/Asturias> rdfs:label ?label }
#""")
#sparql.setReturnFormat(JSON)
#results = sparql.query().convert()
#
#for result in results["results"]["bindings"]:
#    print(result["label"]["value"])

def getDescriptionAnglais(uri):
	spar = SPARQLWrapper("http://dbpedia.org/sparql")
	spar.setQuery("""
	SELECT ?comment WHERE { """ + uri + 
	"""	rdfs:comment ?comment
	FILTER (lang(?comment) = 'en')
	} """)
	spar.setReturnFormat(JSON)
	resul = spar.query().convert()

#	for resultat in resul["results"]["bindings"]:
#		print(resultat["comment"]["value"])
	print(resul["results"]["bindings"][0]["comment"]["value"])
	return resul["results"]["bindings"][0]["comment"][value"]


fic["description_en"] = getDescriptionAnglais(uri)
