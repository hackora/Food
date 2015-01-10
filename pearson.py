#!/usr/bin/env python

import requests, json

url = "http://api.pearson.com:80/kitchen-manager/v1/recipes?"
payload = {'ingredients-any': 'spinach', 'limit': 3000}
payload2 = {'limit': 3000}
res = requests.get(url, params=payload2)

with open('data.json', 'w') as outfile:
  json.dump(res.json(), outfile)

print("foo")