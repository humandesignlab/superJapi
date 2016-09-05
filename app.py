#!flask/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template
from flask_cors import CORS
from searchEngine import searchService

app = Flask(__name__)
CORS(app)
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/superJapi/api/v1.0/searchResult', methods=['GET'])
def search():
	return searchService('papas')

if __name__ == '__main__':
	app.run(debug=True)