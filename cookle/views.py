# encoding=utf8  
from flask import Flask, render_template, request
from cookle import app
from search import recipe_search
import json

@app.route('/', methods=['GET'])
def index():
	if request.args.get('search'):
		return results()
	else:
		return render_template('index.html')
	

@app.route('/results', methods=['GET'])
def results():
	if request.method == 'GET':
		# search = request.form['search']
		search = request.args.get('search')
		print search
		if search == '': 
			return render_template('index.html')
		else:
			results = recipe_search(query=search)
			'''results = dict(query=search,
							ingredients=[dict(name="Pomme", quantity=u"5 unités", image_url=u"http://lasantedansmonassiette.com/wp-content/uploads/2012/07/pomme-fruit-prefere.jpg"),
										dict(name="Beurre", quantity=u"700 grammes", image_url=u"http://www.didier-beurre.fr/images/beurre.jpg"),
										dict(name="Cannelle", quantity=u"3 pincées", image_url=u"http://ileauxepices.com/60-thickbox/cannelle.jpg"),
										],
							search_results=[dict(
								title="Tarte au chocolat", 
								summary=u"Faire une compote : les mettre dans une casserole avec un peu d'eau (1 verre ou 2). Bien remuer. Quand les pommes commencent a ramollir, ajouter un sachet de levure et remuer jusqu'à ébullition...", 
								website="http://www.marmiton.org", 
								preparation_time=u"20 minutes",
								type=u"Végétarien") for _ in range(15)],
							description_en="",
							description_fr=u"La tarte aux pommes est une variété de tarte sucrée, faite d'une pâte feuilletée ou brisée garnie de pommes émincées. Cette tarte peut être dégustée chaude, tiède ou froide. C'est la tarte officielle de l'état du Vermont, aux États-Unis.",
							image_url="https://www.latableadessert.fr/asset-library/publishingimages/desserts/615x460/7502.jpg",
							similar_recipes=["Tarte aux pommes", "Tarte aux poires", "Tarte au chocolat", "Pommes vertes","Dessert aux fruits"],
							execution_time="0,37",
							nb_results="54,000,000,000")'''
			return render_template('results.html', results=results)
	else:
		return render_template('results.html')


if __name__ == '__main__':
	app.run()
