#!/usr/bin/env python

# loads 500 recipes from pearson api
# needs .json file as argument to extract from

import requests, json

url = "http://api.pearson.com:80/kitchen-manager/v1/recipes?"
payload = {'limit': 500}
res = requests.get(url, params=payload)

with open('data.json', 'w') as outfile:
  json.dump(res.json(), outfile)

print("foo")