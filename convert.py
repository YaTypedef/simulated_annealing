#!/usr/bin/env python2.7

import json

f = open('data/libs.txt')
data = f.read()
j = json.loads(data)

for k in j['features']:
	ll = k['geometry']['coordinates']
	name = k['properties']['CompanyMetaData']['name']
	name = name.replace(',', ' ')
	print "{0},{1},{2}".format(name.encode('utf-8'), ll[0], ll[1])