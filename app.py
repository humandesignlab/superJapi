#!flask/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from searchEngine import searchService
import json

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/superJapi/api/v1.0/searchResult', methods=['GET', 'POST'])
def search():
	data1 = json.loads(request.data.decode())
	#print data1
	searchString = data1['userInput']
	returnSearch = searchService(str(searchString))
	#TODO: Maybe with the subprocess pakage, read in real time the pipe output to send an object to angularjs each time a specific string prints.
	return returnSearch

if __name__ == '__main__':
	app.run(debug=True)