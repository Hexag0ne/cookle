# coding=utf-8
import requests
import json
import spotlight 

"""Liste des ingredients. Chaque ingrédient est défini par une liste composée de son nom,de sa proportion et de l'unité de mesure. Donc c'est une liste de listes. """
list_ingredients = []
"""Liste des Uris (ressources) des ingrédients obtenus à partir de l'api DBPedia Spotlight""" 
list_Uri = []
""" A récuperer / input clavier"""
motcle ='cake'
""" url de l'api pour faire la recherche, on reçoit un objet JSON """
""" fichier de retour JSON """
recette_json={} 

requette="https://api.edamam.com/search?q={0}&app_id=0806efd4&app_key=13a926d1babeb8a3726cc3eead90e57c&from=0&to=3".format('cake')
resultat = requests.get(requette)
resultat = resultat.json()
ingredients = resultat['hits'][0]['recipe']['ingredients']
for ingredient in ingredients:
	
	try:

		nom_ingredient = ingredient['food']
	
		if ingredient['measure']=='lb' : 
			quantite_ingredient = ingredient['weight'] 
			unite_ingredient = 'g'
		else: 
			quantite_ingredient= ingredient['quantity']
			unite_ingredient = ingredient['measure']
	
		list_ingredients.append([nom_ingredient,quantite_ingredient,unite_ingredient])
	
		annotation = spotlight.annotate('http://spotlight.sztaki.hu:2222/rest/annotate',text=nom_ingredient,confidence=0.1, support=20,spotter='Default')
		uri_ingredient = annotation[0]['URI']
		
	except spotlight.SpotlightException:
		 uri_ingredient=''

	list_Uri.append(uri_ingredient)

""" Uri de la recette récupéré grâce à l'api DBPedia Spotlight """
annotation = spotlight.annotate('http://spotlight.sztaki.hu:2222/rest/annotate',text=motcle,confidence=0.1, support=20,spotter='Default')
uri_recette = annotation[0]['URI']

recette_json["ingredients"]=list_ingredients
recette_json=json.dumps(recette_json, indent=4)

		