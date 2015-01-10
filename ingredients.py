#!/usr/bin/env python

# extracts all ingredients from the pearson data dump

import sys, json

input = open(sys.argv[1])
data = json.load(input) #data now a dict
list = []

for item in data['results']: 
  list.append(item[u"ingredients"])

with open('ingredients.json', 'w') as outfile:
  json.dump(list, outfile)
