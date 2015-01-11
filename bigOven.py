from __future__ import division
import requests
import json
import xmltodict

__author__ = ''
onlyHealth = False
page, lastId = map(int,open("_state.tmp","r").read().strip().split())
recipeFile = "oven.json"
#recipeFile = None

def reachLimit(response):
    if "Result" in response and "StatusCode" in response["Result"] and int(response["Result"]["StatusCode"]) == 400:
        return True
    return False

def getValues(d):
    if "Unit" in d:
        unit = d["Unit"]
    else:
        unit = 0
    if "Quantity" in d:
        qnt = d["Quantity"]
    else:
        qnt = 0
    if "Name" in d:
        name = d["Name"]
    else:
        name = 0
    return name, unit, qnt

# load saved json file
if not recipeFile:
    recipes = []
else:
    json_data = open(recipeFile, "r")
    recipes = json.load(json_data)

# base_urls
search_url = "http://api.bigoven.com/recipes"
recipe_url = "http://api.bigoven.com/recipe"

for key in ["dvxSnQcNBSQI77748n31rTuw66IHgElP", "dvxqIL58gls8jQ82A1tFjX492y2sWUE0", "dvx7rjRU1Tz13kktObB36g1Xiz6bTm1o", "dvxBW97ZTXCs09KnczAC292vhiNVYUno", "dvxNlC5EFB1ng6qljl2tvn9d4e9jjpEz", "dvxG69AM67E8cUwXwjU2ZR14ZJJo1e23", "dvxd9sa7fjDopTf5Lt3rIpWPIEnw5G1X", "dvxZh5cdoRli449Xg63yF3VwzI535TZD", "dvxXQdV01863Bu3w573HoXq5LZKWl56D", "dvx310tYY7xiDRirvoMoSD6h7Gr2mRt2", "dvxqhzX75jS80zrtR66d86yxLs5KpQp6","dvxZ7saU0vB8kE5783G58ZK2oiacG61E", "dvx6SVQTzT56H6Cn89tlfFZA0v0owa56", "dvx4j5m504gDS9Exs87416LhdS8bjp1R", "dvxhVcF74Efju5MQYd6HtxwVfP3N31Nn", "dvxsMxao23smCIe8oama2q61aQ5siBHc", "dvxsdvWWsbai8HYQ5xq8e0QwBDoI73eC", "dvxuJDOEI00qQjRHbC9j6e4lx7H1Zg40", "dvxhJ1rHTFoRBM0mW0jD62Gl5SE51pOm", "dvxPdLD6L335HUTg5784qU15wuhdXNp6","dvxB7BYq77f2nZfd1O1qSDcA2W8m4QQ1", "dvx7MFuK6l2v6I2fS48SODjwOV4mxg24", "dvxinu5fXLp1tw1Z73traLyn0fda7ARd", "dvxBNaUx22D446PJE5Mkj2vfU2091s02", "dvxTo4I9V7Ou4KEv0cv0rfESTVOV96hD", "dvx8Rmucu5y0354QWnJBZap0r0e74DhQ"]:
    print "KEY =" , key
    Next = False
    while not Next:

        page = page + 1
        print "NEW PAGE -----> ", page
        # parameters for recipe search
        search_params = {"api_key": key, "sort" : "title", "pg": page, "rpp": 50, }
        if onlyHealth:
            search_params["any_kw"] = "health"

        response = requests.get(search_url, params=search_params)
        data = xmltodict.parse(response.text)
        data = json.loads(json.dumps(data))
        
        # sample GET request
        if reachLimit(data):
            print "Reached Limit Guys"
            Next = True
            # We have to start over for this page
            page = page - 1
            continue

        ids = []
        
        for d in data["RecipeSearchResult"]["Results"]["RecipeInfo"]:
            ids.append( d["RecipeID"] )

        for i, id in enumerate(ids):

            print "Processed: Page:", page, "i: ", i, "out of 50"
            if i < lastId:
                #Already Processed
                continue

            recipe_dict = {}
            recipe_url_tmp = recipe_url + "/" + id
            recipe_params = {"api_key": key}
            response_recipe = requests.get(recipe_url_tmp, params=recipe_params)
            
            recipe = xmltodict.parse(response_recipe.text)
            recipe = json.loads(json.dumps(recipe))
            
            if reachLimit(response_recipe):
                print "Reached Limit Guys"
                Next = True
                # We have to start over for this page
                page = page - 1
                lastId = i
                break
           
            if not "Recipe" in recipe:
                continue

            recipe_dict["Ingredients"] = []
            if "Title" not in recipe["Recipe"]:
                continue

            recipe_dict["Name"] = recipe["Recipe"]["Title"]

            if "Cuisine" in recipe["Recipe"]:
                recipe_dict["Cuisine"] = recipe["Recipe"]["Cuisine"] 
            else:
                recipe_dict["Cuisine"] = None
            
            if "StarRating" in recipe["Recipe"]:
               recipe_dict["Rating"] = recipe["Recipe"]["StarRating"]

            if "Recipe" in recipe:
                if recipe["Recipe"] and "Ingredients" in recipe["Recipe"]:
                    if recipe["Recipe"]["Ingredients"] and "Ingredient" in recipe["Recipe"]["Ingredients"]:
                        if type(recipe["Recipe"]["Ingredients"]["Ingredient"]) == list:
                            for d in recipe["Recipe"]["Ingredients"]["Ingredient"]:
                                #print d["Name"], d["Quantity"], d["Unit"]
                                name, unit, qnt = getValues(d)
                                recipe_dict["Ingredients"].append({"Name": name, "Quantity": qnt, "Unit":unit})
                        
                        if type(recipe["Recipe"]["Ingredients"]["Ingredient"]) == dict:
                            d =  recipe["Recipe"]["Ingredients"]["Ingredient"]
                            name, unit, qnt = getValues(d)
                            recipe_dict["Ingredients"].append({"Name": name, "Quantity": qnt, "Unit":unit})

            recipes.append(recipe_dict)
        #Alright we process everything without errors
        lastId = 0

print "Last processed page:", page, " last id:", lastId
# save json

if not recipeFile:
    recipeFile = "oven_tmp.txt"

with open(recipeFile, 'w') as f:
    json.dump(recipes, f)

with open("_state.tmp","w") as f:
        f.write("%d\t%d" % (page, lastId))

