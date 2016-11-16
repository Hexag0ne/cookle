#local imports
from recipe_api import getIngredients
from sparql import getDescription, getImage

#external imports
import requests
from multiprocessing import Process
from bs4 import BeautifulSoup
import re
import time

ACTIVATE_API = False
if ACTIVATE_API:
    from aylienapiclient import textapi
    client = textapi.Client("18d3d263", "6cb4cddc2c058473fb1984dcc30549ed")

BASE_URL = "http://www.cuistot.org/recherche.php"
DEFAULT_TIMEOUT = 5
DEFAULT_PARAMS = {"type_recettes":0, "vegetarien":0, "alcool":0, "ustensiles":0, "porc": 0, "lait": 0, "type_rech": "mono", "nb_aliments_saisie": 3}

def recipe_search(query=None):
    t = time.time()
    my_params = DEFAULT_PARAMS.copy()
    my_params["texte_rech"] = query # Setting query in parameters
    result = requests.get(url=BASE_URL, params=my_params, timeout=DEFAULT_TIMEOUT)
    if result.status_code != 200:
        print "Error searching query (status_code != 200)"
        results = dict(error="No data found")
    else:
        soup = BeautifulSoup(result.text, "html.parser")
        links, types, durations = getLinks(soup), getTypes(soup), getDurations(soup)
        summaries = getSummaries(links)
        recipe_res = getIngredients(query)
        list_ingredients = recipe_res["list_ingredients"]
        recettes_similaires = recipe_res["similar_recipes"]
        uri = recipe_res["uri"]
        description_fr = getDescription(uri=uri, langue="fr")
        description_en = getDescription(uri=uri, langue="en")
        image_url = getImage(uri=uri)
        exec_time = round(time.time()-t, 2)
        # search results
        search_results = [dict(
                        title=l["title"], website=l["href"],
                        type=t, preparation_time=d, summary=s,
                        )
                        for l,t,d,s in zip(links, types, durations, summaries)]
        results = dict(search_results=search_results, execution_time=exec_time,
                       query=query, nb_results=len(search_results), image_url=image_url,
                       ingredients=list_ingredients, description_en=description_en,
                       description_fr=description_fr,similar_recipes=recettes_similaires)
    return results

def getSummaries(links):
    urls = [l["href"] for l in links]
    if ACTIVATE_API:
        summaries = [extractText(url) for url in urls]
    else:
        summaries = ["//EXTRACTED_TEXT//" for url in urls]
        #summaries = [requests.get(url) for url in urls]
    return summaries

def extractText(url):
    extract = client.Extract({"url": url, "best_image": False, "language":"fr"})
    return extract["article"][:250]

def getDurations(soup):
    # durations
    durations = soup(string=re.compile("paration[ ][:]"))
    durations = [d.split(' : ')[1].split(' et ')[0] for d in durations]
    return durations

def getTypes(soup):
    # type
    types = soup(string=re.compile("Plat.[ ](.*)[.]"))
    types = [t.replace('.', '').split('Plat ')[1] for t in types]
    return types

def getLinks(soup):
    # title + website
    links = soup("a", "gras")
    return links

if __name__ == "__main__":
    # do stuff if : python search.py
    print recipe_search(query="lasagnes")
