from flask import Flask, render_template, request
from cookle import app
from search import recipe_search
import json

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		return results()
	else:
		return render_template('index.html')
	

@app.route('/results', methods=['GET', 'POST'])
def results():
	if request.method == 'POST' :
		search = request.form['search']
		if search == '': 
			return render_template('index.html')
		else:
			results = recipe_search(query=search)
			return render_template('results.html', results=results)
	else:
		return render_template('results.html')


if __name__ == '__main__':
	app.run()
