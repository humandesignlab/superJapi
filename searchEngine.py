#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os, sys
from bs4 import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
import lxml
import lxml.etree
import urllib2
import json
from cookielib import CookieJar
import pandas as pd
from decimal import *
import re

progCounter = 0

def HTMLEntitiesToUnicode(text):
    text = unicode(BeautifulStoneSoup(text, convertEntities=BeautifulStoneSoup.ALL_ENTITIES))
    return text

def unicodize(seg):
    if re.match(r'\\u[0-9a-f]{4}', seg):
        return seg.decode('unicode-escape')

    return seg.decode('utf-8')

def progressCounter():
	global progCounter
	progCounter += 2.5
	progCounterDict = {'progress' : progCounter}
	jsonProgCounterDict = json.dumps(progCounterDict)
	return jsonProgCounterDict

def chedrauiSearchService(searchString):

	searchTerm = searchString
	searchQuery = searchTerm.replace(" ", "+")
	productNames = []
	allPrices = []
	allImagesUrl = []
	cj = CookieJar()

	preOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	prep = preOpener.open('http://www.chedraui.com.mx/index.php/interlomas/catalogsearch/result/?cat=0&p=1&q=' + searchQuery)
	preSoup = BeautifulSoup(prep, "lxml")
	pagerTotal = preSoup.find('div', class_='pager')
	children = None
	pages = 1
	try: 
		children = pagerTotal.find_all("li")
		if len(children) == 0:
			pages = len(children) +2
		else:
			pages = len(children)
	except Exception, e:
		print "No products found in Chedraui!"

	print "RESULTS CHEDRAUI: "
	for page in range(1,pages):
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		p = opener.open('http://www.chedraui.com.mx/index.php/interlomas/catalogsearch/result/?cat=0&p=' + str(page) + '&q=' + searchQuery)
		mySoup = BeautifulSoup(p, "lxml")

		chedraui_products = mySoup.find_all('div', class_='f-fix')
		for name in chedraui_products:
			names = name.find_all('a', class_='name-product')
			productNames.append(names[0].find(text=True).strip())

		chedraui_prices = mySoup.find_all('div', class_='price-box')
		for price in chedraui_prices:
			prices = price.find_all('span', class_='price')
			allPrices.append(prices[-1].find(text=True).strip())

		chedraui_imgUrl = mySoup.find_all('a', class_='product-image')
		for image in chedraui_imgUrl:
			images = image.find_all('img')
			for img in images:
			    if 'src' in img.attrs:
			        allImagesUrl.append(img.attrs['src'])
			#print allImagesUrl

		print "Retreived data from page: " + str(page)

	print "Number of products: ", len(productNames)
	print "Number of prices: ", len(allPrices)

	dfChedraui = pd.DataFrame(productNames, columns=['Producto'])
	dfChedraui['Precio']=[Decimal('%.2f' % float(element.strip("$").replace(",", ""))) for element in allPrices]
	dfChedraui['imgUrl']= allImagesUrl
	#dfChedraui.to_csv('searches/outchedraui.csv', encoding='utf-8')
	print progressCounter()
	return dfChedraui


def lacomerSearchService (searchString):
	searchQuery = searchString
	productNames = []
	presentation = []
	brandNames = []
	allPrices = []
	allImagesUrl = []
	req = urllib2.Request("http://www.lacomer.com.mx/GSAServices/searchArt?col=lacomer_2&orden=-1&p=1&pasilloId=false&s="+searchQuery+"&succId=14")

	opener = urllib2.build_opener()
	f = opener.open(req)
	json1 = json.loads(f.read())
	numpages = json1['numpages'] + 1

	print "RESULTS LA COMER: "
	print 'Number of pages: ', numpages
	print 'Number of products: ', json1['total']

	for page in range(0,numpages):
		data = opener.open("http://www.lacomer.com.mx/GSAServices/searchArt?col=lacomer_2&orden=-1&p="+str(page)+"&pasilloId=false&s="+searchQuery+"&succId=14")
		completeJson = json.loads(data.read())

		names = [lin['artDes'] for lin in completeJson['res']]
		productNames.append(names)

		pres = [lin['artPres'] for lin in completeJson['res']]
		presentation.append(pres)

		brand = [lin['marDes'] for lin in completeJson['res']]
		brandNames.append(brand)

		prices = [lip['artPrven'] for lip in completeJson['res']]
		allPrices.append(prices)
		#Image URL:
		#https://www.lacomer.com.mx/superc/img_art/7501055901401_1.jpg
		itemCode = [lip['artEan'] for lip in completeJson['res']]
		for code in itemCode:
			imgUrl = 'https://www.lacomer.com.mx/superc/img_art/'+code+'_3.jpg'
			#print imgUrl
			allImagesUrl.append(imgUrl)
	productNamesList  = sum(productNames, [])
	presentationList = sum(presentation, [])
	allPricesList = sum(allPrices, [])
	brandNamesList = sum(brandNames, [])
	#allImagesUrl = sum(allImagesUrl, [])	

	df = pd.DataFrame()
	df['Producto'] = productNamesList
	df['Presentación']=[element.lower() for element in presentationList]
	df['Marca']=[element.lower() for element in brandNamesList]

	dfLacomer = pd.DataFrame()
	dfLacomer['Producto'] = df['Producto'].map(str) + " " + df['Presentación'].map(str) + " " + df['Marca']
	dfLacomer['Precio'] = [Decimal('%.2f' % element) for element in allPricesList]
	dfLacomer['imgUrl'] = allImagesUrl
	#dfLacomer.to_csv('searches/outlacomer.csv', encoding='utf-8')
	print progressCounter()
	return dfLacomer


def superamaSearchService(searchString):
	searchTerm = searchString
	productNames = []
	brandNames = []
	allPrices = []
	allImagesUrl = []
	searchQuery = searchTerm.replace(" ", "+")
	req = urllib2.Request("http://www.superama.com.mx/buscador/resultado?busqueda="+searchQuery)

	opener = urllib2.build_opener()
	f = opener.open(req)
	json1 = json.loads(f.read())

	print "RESULTS SUPERAMA: "
	print 'Number of products: ', len(json1['Products'])

	for item in range(0, len(json1['Products'])):
		names = json1['Products'][item]['Description']
		cleanNames = HTMLEntitiesToUnicode(names).encode('utf-8')
		productNames.append(cleanNames)
		prices = json1['Products'][item]['Precio']
		allPrices.append(prices)
		itemCode = json1['Products'][item]['Upc']
		imagesUrl = 'http://www.superama.com.mx/Content/images/products/img_large/' + itemCode + 'L.jpg'
		allImagesUrl.append(imagesUrl)

	dfSuperama = pd.DataFrame(productNames, columns=['Producto'])
	dfSuperama['Precio']=[Decimal('%.2f' % float(element.strip("$").replace(",", ""))) for element in allPrices]
	dfSuperama['imgUrl'] = allImagesUrl
	#dfSuperama.to_csv('searches/outsuperama.csv', encoding='utf-8')
	print progressCounter()
	return dfSuperama

def walmartSearchService(searchString):
	searchTerm = searchString
	productNames = []
	brandNames = []
	allPrices = []
	allImagesUrl = []
	searchQuery = searchTerm.replace(" ", "%20")
	req = urllib2.Request("https://www.walmart.com.mx/super/WebControls/hlSearch.ashx?Text="+searchQuery)

	opener = urllib2.build_opener()
	f = opener.open(req)
	json1 = json.loads(f.read(), 'ISO-8859-1')

	print "RESULTS WALMART: "
	print 'Number of products: ', len(json1['Products'])

	for item in range(0, len(json1['Products'])):
		names = json1['Products'][item]['Description']
		cleanNames = HTMLEntitiesToUnicode(names).encode('utf-8')
		productNames.append(cleanNames)
		prices = json1['Products'][item]['Precio']
		allPrices.append(prices)
		itemCode = json1['Products'][item]['SEOUrl'][-14:-1]
		imagesUrl = 'https://www.walmart.com.mx/super/images/Products/img_large/' + itemCode + 'L.jpg'
		allImagesUrl.append(imagesUrl)

	dfWalmart = pd.DataFrame(productNames, columns=['Producto'])
	dfWalmart['Precio']=[Decimal('%.2f' % float(element.strip("$").replace(",", ""))) for element in allPrices]
	dfWalmart['imgUrl'] = allImagesUrl
	#dfSuperama.to_csv('searches/outsuperama.csv', encoding='utf-8')
	print progressCounter()
	return dfWalmart

def searchService(searchString):
	dfMasterResult = pd.concat([superamaSearchService(searchString), lacomerSearchService(searchString), chedrauiSearchService(searchString), walmartSearchService(searchString)], keys=['Superama', 'La Comer', 'Chedraui', 'Walmart'])
	dfMasterResult.index.levels[0].name = 'Tienda'
	dfMasterResult.index.levels[1].name = 'ID'
	#print dfMasterResult 
	dfMasterResult.to_csv('outMasterResult.csv', encoding='utf-8')
	jsonResult = dfMasterResult.reset_index().to_json(orient='records')
	replacedJsonResult = (unicodize(seg) for seg in re.split(r'(\\u[0-9a-f]{4})',jsonResult))
	jsonCleanResult = (''.join(replacedJsonResult))
	global progCounter
	progCounter = 0

	return jsonCleanResult


#searchService('jamon serrano')

