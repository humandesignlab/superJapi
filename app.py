#!flask/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template
from searchEngine import searchService

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/superJapi/api/v1.0/searchResult', methods=['GET'])
def search():
	return searchService('leche lala deslactosada 1 l')

if __name__ == '__main__':
	app.run(debug=True)