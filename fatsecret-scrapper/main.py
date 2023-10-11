from harvest import harvest
import json

""" 
TODO:
- Skip already existing foods
- When searching for the market name, search also without it
 """


FOODS_JSON_PATH = "resources/foods_small.json"

with open(FOODS_JSON_PATH, "r", encoding="utf-8") as f:
    foods = json.load(f)

food_list = foods.get("food_list")
harvested = harvest(items_to_search=food_list, market_name="", verbose=True)

# save to json
with open("resources/harvested.json", "w", encoding="utf-8") as f:
    json.dump(harvested, f, ensure_ascii=False, indent=4)
