from flask import Flask
import json

app = Flask(__name__)

@app.route('/api/v1/')
def api():
	

if __name__ == '__main__':
	app.run()