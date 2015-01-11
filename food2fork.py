from __future__ import division, print_function
from pprint import pprint
import requests, json
from collections import defaultdict

__author__ = 'Asura'

keys = ["8670184bed1803ea6aaec214ca7063e4",
        "5ac015364e443c1e1e6ea20a1d3dbc19",
        "88bee2635ab15f6a56bfbd0792fcfef4",
        "6250fd4e4353f701061f6d5bcdabb179",
        "56b3dee75b03d8c63b8adbd1a1e5bc29",
        "117c6b90f9fdc0edafd53810d6b578a8",
        "a4b8f017c7b74967468760e626c10f14"]

ranges = [range(0, 400, 26)[0:15],
          range(400, 500, 6)[0:15],
          range(500, 600, 6)[0:15],
          range(600, 700, 6)[0:15],
          range(700, 1000, 20)[0:15],
          range(1000, 1500, 33)[0:15],
          range(1500, 2000, 33)[0:15]]

# base_urls
search_url = "http://food2fork.com/api/search"
get_url = "http://food2fork.com/api/get"

# parameters for recipe search

for key, offsets in zip(keys, ranges):
    print(key, len(offsets))
    for page_count in offsets:
        "\n\nPROCESSING PAGE " + str(page_count) + "\n\n"

        search_params = {"key": key,
                         'q': "",
                         'page': page_count}

        response = requests.get(search_url, params=search_params)
        if response.status_code != 200:
            print('error')
            pprint(response.text)
            break
        page = response.json()

        all_recipes = []

        pprint(page)

        for idx, recipe_obj in enumerate(page['recipes'], 1):
            new_recipe = {'name': recipe_obj['title'],
                          'rating': recipe_obj['social_rank'],
                          'ingredients': None}

            rId = recipe_obj['recipe_id']
            recipe_params = {'key': key,
                             'rId': rId}

            response = requests.get(get_url, params=recipe_params)
            if response.status_code == 200:
                new_recipe['ingredients'] = response.json()['recipe']['ingredients']
                print(idx, "\n")
                pprint(new_recipe)
                all_recipes.append(new_recipe)
            else:
                break

        with open('new_data/recipes_{}.json'.format(page_count), 'w') as f:
            json.dump(all_recipes, f)