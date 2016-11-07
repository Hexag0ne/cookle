import requests
from bs4 import BeautifulSoup

BASE_URL = "http://www.cuistot.org/recherche.php"
DEFAULT_TIMEOUT = 5
DEFAULT_PARAMS = {"type_recettes":0, "vegetarien":0, "alcool":0, "ustensiles":0, "porc": 0, "lait": 0, "type_rech": "mono", "nb_aliments_saisie": 3}
DEFAULT_HEADERS = {"X-DevTools-Emulate-Network-Conditions-Client-Id": "bf696541-e4f8-4b30-831b-20ba2760c02a", "Cookie": '__utmt=1; __utma=243895447.1157611143.1478505110.1478505110.1478505110.1; __utmb=243895447.9.10.1478505110; __utmc=243895447; __utmz=243895447.1478505110.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)', "Upgrade-Insecure-Requests": "1", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Encoding": "gzip, deflate, sdch", "Accept-Language": "fr,en-US;q=0.8,en;q=0.6,es;q=0.4", "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36"}

def recipe_search(query=None):
    my_params = DEFAULT_PARAMS.copy()
    my_params["texte_rech"] = query # Setting query in parameters
    result = requests.get(url=BASE_URL, params=my_params, timeout=DEFAULT_TIMEOUT, headers=DEFAULT_HEADERS, allow_redirects=True)
    if result.status_code != 200:
        print "Error searching query (status_code != 200)"
        return None
    else:
        html_doc = result.text
        soup = BeautifulSoup(html_doc, "html.parser")
        results = soup("a", "gras")
        results = [r["title"] for r in results]
        return results

if __name__ == "__main__":
    # do stuff if : python search.py
    print recipe_search(query="lasagnes")