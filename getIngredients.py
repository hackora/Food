import json
import re
from collections import Counter

def norm(s):
    if not s:
        return ""
    s = re.sub('[\W_]+', ' ', s)
    s = re.sub("\d+", '', s)
    s = re.sub(' +',' ', s)
    return s.lower()

ingrdsOutFile = "ingrds2.txt"
#infile = "oven_health.json"
infile = "oven.json"

json_data = open(infile, "r")
recipes = json.load(json_data)

tokens = []
for recipe in recipes:
    for ing in recipe["Ingredients"]:
        if not ing["Name"]:
            continue
        
        names = norm(ing["Name"].strip()).split()
        names = [n for n in names if n and len(n) > 1]
        tokens.extend(names)

c = Counter(tokens)
with open(ingrdsOutFile, "w") as f:
    for k, v in c.most_common(500):
        f.write(k + "\n")

