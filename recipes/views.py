from flask import Flask, render_template, request
from recipes import app
import json

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		search = request.form['search']
		return render_template('results.html', search = search)
	else:
		return render_template('index.html')
	

@app.route('/results', methods=['GET', 'POST'])
def results():
	if request.method == 'POST':
		search = request.form['search']
		return render_template('results.html', search = search)
	else:
		return render_template('results.html')


if __name__ == '__main__':
	app.run()
