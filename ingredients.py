#!/usr/bin/env python

# extracts all ingredients from the pearson data dump

import sys, json

input = open(sys.argv[1])
data = json.load(input) #data now a dict
lis = []

for item in data['results']: 
  lis.append(item[u"ingredients"])

with open('ingredients.json', 'w') as outfile:
  json.dump(lis, outfile)
