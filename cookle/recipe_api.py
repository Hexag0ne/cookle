# coding=utf-8
import requests
import json
import spotlight
import goslate
from sparql import getNomFrancais,getTypeRecette,getRecetteSimilaire,getImage

def getIngredients(recipe):
    list_ingredients = []
    gs = goslate.Goslate(service_urls=['http://translate.google.de'])
    recipe_tr = translate(recipe)
    requette = "https://api.edamam.com/search?q={0}&app_id=0806efd4&app_key=13a926d1babeb8a3726cc3eead90e57c&from=0&to=3&diet=balanced".format(recipe_tr)
    resultat = requests.get(requette)
    resultat = resultat.json()
    if len(resultat['hits'])==0:
        return dict(list_ingredients=[], uri=None)
    ingredients = resultat['hits'][0]['recipe']['ingredients']
    i = 1
    for ingredient in ingredients:
        nom_ingredient = ingredient['food']
        if ingredient['measure']=='lb' : 
            quantite_ingredient = ingredient['weight'] 
            unite_ingredient = 'g'
        else: 
            quantite_ingredient= ingredient['quantity']
            if float(quantite_ingredient) % 1 == 0:
                quantite_ingredient = int(float(quantite_ingredient))
            else:
                quantite_ingredient = round(float(quantite_ingredient), 2)
            unite_ingredient = ingredient['measure']
        image_url, uri_ingredient = None, None
        try:
            annotation = spotlight.annotate('http://spotlight.sztaki.hu:2222/rest/annotate',text=nom_ingredient,confidence=0.1, support=20,spotter='Default')
            uri_ingredient = annotation[0]['URI']
            image_url = getImage(uri_ingredient)
            try:
                nom_ingredient = getNomFrancais(uri_ingredient)
            except:
                nom_ingredient = "{} (anglais)".format(nom_ingredient)
        except:
            pass
        if nom_ingredient:
            i += 1
            list_ingredients.append(dict(name=nom_ingredient, quantity=quantite_ingredient, unit=unite_ingredient, uri=uri_ingredient, image_url=image_url))
        if i > 5:
            break

    """ Uri de la recette récupéré grâce à l'api DBPedia Spotlight """
    try:
        annotation = spotlight.annotate('http://spotlight.sztaki.hu:2222/rest/annotate',text=recipe_tr,confidence=0.5, support=20,spotter='Default')
        uri_recette = annotation[0]['URI']
        type_rectte_uri = getTypeRecette(uri_recette)
        recettes_similaires= getRecetteSimilaire(type_rectte_uri)
    except:
        recettes_similaires= {}
        uri_recette = None

    # uri can be None
    recette = dict(list_ingredients=list_ingredients, uri=uri_recette, similar_recipes=recettes_similaires)
    return recette

def translate(word):
    req = "https://translate.yandex.net/api/v1.5/tr.json/translate?key=trnsl.1.1.20161116T102126Z.efd63f26cc4533d2.7e0ab34d8ae9647e547a4b450788b5de86a9e6a6&text={}&lang=fr-en".format(word)
    return requests.get(req).json()['text'][0]
