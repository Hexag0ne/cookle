import requests
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
        exec_time = round(time.time()-t, 2)
        # search results
        search_results = [dict(
                        title=l["title"], website=l["href"], nb_results=len(links),
                        type=t, preparation_time=d, summary=s, execution_time=exec_time
                        )
                        for l,t,d,s in zip(links, types, durations, summaries)]
        results = dict(search_results=search_results)
    return results

def getSummaries(links):
    urls = [l["href"] for l in links]
    if ACTIVATE_API:
        summaries = [extractText(url) for url in urls]
    else:
        summaries = [requests.get(url).text[:250] for url in urls]
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
