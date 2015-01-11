import json
import re
import pandas as pd
from collections import defaultdict

def norm(s):
    if not s:
        return ""
    s = re.sub('[\W_]+', ' ', s)
    s = re.sub("\d+", '', s)
    s = re.sub(' +',' ', s)
    return s.lower()

ingrdsFile = "ingrds.txt"
#ingrdsFile = "ingrds2.txt"
#infile = "oven_health.json"
infile = "oven.json"

ingrds_ = open(ingrdsFile, "r")
ingrds = []
for l in ingrds_:
    ingrds.append(l.strip())
ingrds_dict = defaultdict(int)
for i in ingrds:
    ingrds_dict[i] = 1

json_data = open(infile, "r")
recipes = json.load(json_data)

new_recipes = []

for recipe in recipes:
    new_recipe = {}
    new_recipe["Name"] = recipe["Name"]
    new_recipe["Rating"] = recipe["Rating"]
    new_recipe["Ingredients"] = []

    for ing in recipe["Ingredients"]:
        if not ing["Name"]:
            continue
        
        names = norm(ing["Name"].strip()).split()
        names = [name for name in names if name and len(name) > 1]

        if not names:
            continue
        
        for name in names:
            if ingrds_dict[name] == 1:
                new_recipe["Ingredients"].append(name)
        
        #ing["NameList"].append(name)
    
    new_recipes.append(new_recipe)

columns = [u'Name', u'Rating']
columns.extend(ingrds)

df = pd.DataFrame(columns = columns)

for idx, recipe in enumerate(new_recipes):
    print idx,
    #ing["NameList"].append(name)
        
    #ings = [1 if ingredient['Name'] == list_element else 0 for list_element in ingrds]
    ing_map = defaultdict(int)
    for ing in recipe['Ingredients']:
        ing_map[ing] = 1
    
    ings = [1 if ing_map[list_element] == 1 else 0 for list_element in ingrds]
    print sum(ings)
    row = [recipe['Name'], recipe['Rating']]
    row.extend(ings)
    df.loc[idx] = row

df.drop_duplicates(inplace=True)

# Tokens
tokens = []
for sentence in ingrds:
    tokens.extend( w for w in sentence.strip().split())

from collections import Counter
c = Counter(tokens)
#for k, v in c.most_common(500):
#   print k, v

# df.to_pickle("oven.nothealth")


