# coding=utf-8
import requests
import json
import spotlight
import goslate
from sparql import getNomFrancais,getTypeRecette,getRecetteSimilaire

"""Liste des ingredients. Chaque ingrédient est défini par une liste composée de son nom,de sa proportion et de l'unité de mesure. Donc c'est une liste de listes. """
list_ingredients = []
"""Liste des Uris (ressources) des ingrédients obtenus à partir de l'api DBPedia Spotlight""" 
list_Uri = []
""" A récuperer / input clavier"""

""" url de l'api pour faire la recherche, on reçoit un objet JSON """
""" fichier de retour JSON """

def getIngredients(recipe):
    gs = goslate.Goslate()
    recipe_tr = gs.translate( recipe, 'en')
    requette="https://api.edamam.com/search?q={0}&app_id=0806efd4&app_key=13a926d1babeb8a3726cc3eead90e57c&from=0&to=3&diet=balanced".format(recipe_tr)
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
                if float(quantite_ingredient) % 1 == 0:
                    quantite_ingredient = int(float(quantite_ingredient))
                else:
                    quantite_ingredient = float(quantite_ingredient)
                unite_ingredient = ingredient['measure']
            annotation = spotlight.annotate('http://spotlight.sztaki.hu:2222/rest/annotate',text=nom_ingredient,confidence=0.1, support=20,spotter='Default')
            uri_ingredient = annotation[0]['URI']
            try:
                nom_ingredient = getNomFrancais(uri_ingredient)
            except:
                nom_ingredient = nom_ingredient + " (anglais)"
        except spotlight.SpotlightException:
            uri_ingredient = None
        list_ingredients.append(dict(name=nom_ingredient, quantity=quantite_ingredient, unit=unite_ingredient, uri=uri_ingredient))

    """ Uri de la recette récupéré grâce à l'api DBPedia Spotlight """
    try:
        annotation = spotlight.annotate('http://spotlight.sztaki.hu:2222/rest/annotate',text=recipe_tr,confidence=0.5, support=20,spotter='Default')
        uri_recette = annotation[0]['URI']
        type_rectte_uri = getTypeRecette(uri_recette)
        recettes_similaires= getRecetteSimilaire(type_rectte_uri)
    except:
        uri_recette = None

    # uri can be None
    recette = dict(list_ingredients=list_ingredients, uri=uri_recette,similar_recipes=recettes_similaires)
    return recette
