import json

from harvest import harvest

""" 
TODO:
- Skip already existing foods
- When searching for the market name, search also without it
 """


FOODS_JSON_PATH = "resources/foods_small.json"

with open(FOODS_JSON_PATH, "r", encoding="utf-8") as f:
    foods = json.load(f)
food_list = foods.get("food_list", [])

harvest(food_list, verbose=True)
