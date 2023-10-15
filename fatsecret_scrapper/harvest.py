import json
import time

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from tqdm import tqdm

from db import food_exists, init_db, insert_food

MAX_REQUESTS = 5
REQUEST_DELAY_SECONDS = 60
FOOD_RESULTS = 5
FOODS_JSON_PATH = "resources/foods.json"


init_db()


def __request(url):
    for _ in range(MAX_REQUESTS):
        response = requests.get(url, timeout=60)
        if response.status_code == 429:
            print(f"Too many requests, waiting {REQUEST_DELAY_SECONDS} seconds")
            time.sleep(REQUEST_DELAY_SECONDS)
        else:
            break
    if response.status_code != 200:
        print(f"Error requesting {url}: status code {response.status_code}")
        return None
    return response


def __add_item_url(food_dict, suf, page, verbose=False):
    search_term = food_dict["search_term"] + " " + suf
    search_base_url = "https://www.fatsecret.es/calorías-nutrición/search?q="
    page_url = "&pg=" + str(page)
    url = search_base_url.strip() + search_term.strip().replace(" ", "+") + page_url
    if verbose:
        print(f"Searching on:\n{url}\n")
    response = __request(url)
    if response is None:
        return None
    soup = BeautifulSoup(response.text, "html.parser")
    food_links = soup.find_all("td", {"class": "borderBottom"})
    results = []
    for link in food_links:
        item_dict = food_dict.copy()
        item_dict["item_url"] = (
            "https://fatsecret.es" + link.find("a", {"class": "prominent"})["href"]
        )
        results.append(item_dict)
    return results


def __check_100g(food_dict, verbose=False):
    item_url = food_dict.get("item_url")
    soup = BeautifulSoup(__request(item_url).text, "html.parser")
    serving_size = soup.find("div", {"class": "serving_size black serving_size_value"})
    if verbose:
        print(f"Checking if {food_dict['search_term']} is 100g -- {item_url}")
        if serving_size is not None and serving_size.text == "100 g":
            print("This food is 100g.")
        else:
            print("This food is not 100g.")
        print("--------------------------------------------------")
    return serving_size is not None and serving_size.text == "100 g"


def __fetch_macros(food_dict, verbose=False):
    if verbose:
        print(
            f"Gathering macros for {food_dict['search_term']} -- {food_dict['item_url']}\n"
        )
    soup = BeautifulSoup(__request(food_dict["item_url"]).text, "html.parser")
    macros = soup.find("div", {"class": "factPanel"})
    if macros is None:
        if verbose:
            print(f"No macros found for {food_dict['search_term']}\n")
        return None
    macro_list = [
        macro.text for macro in macros.find_all("div", {"class": "factValue"})
    ]
    if len(macro_list) < 4:
        if verbose:
            print(f"Not enough macros found for {food_dict['search_term']}\n")
        return None
    cals, fat, carb, prot = [
        float(macro.replace("g", "").replace(",", ".")) for macro in macro_list[:4]
    ]
    result = {
        "cals_per_g": cals / 100,
        "fat_per_g": fat / 100,
        "carb_per_g": carb / 100,
        "prot_per_g": prot / 100,
    }
    if verbose:
        print(f"Macros found for {food_dict['search_term']}:\n{result}\n")
        print("--------------------------------------------------")
    return result


def __fetch_metadata(food_dict, verbose=False):
    if verbose:
        print(
            f"Gathering metadata for {food_dict['search_term']} -- {food_dict['item_url']}\n"
        )
    url = food_dict["item_url"]
    try:
        response = __request(url)
    except RequestException as e:
        print(f"Error requesting {url}: {e}")
        return None

    if response.status_code != 200:
        print(f"Error requesting {url}: status code {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # BRAND
    brand = None
    brand_tag = soup.find("a", {"style": "color: #028CC4;"})
    if brand_tag is not None:
        brand = brand_tag.text

    # NAME
    name = None
    name_tag = soup.find("h1", {"style": "text-transform:none"})
    if name_tag is not None:
        name = name_tag.text

    result = {"brand": brand, "name": name}

    if verbose:
        print("Metadata found:")
        for k, v in result.items():
            print(f"{k}: {v}")
        print("--------------------------------------------------")
    return result


def __get_food_info(food_dict, suffix, min_results=FOOD_RESULTS, verbose=False):
    data = []
    page = 0
    if suffix != "":
        search_term = food_dict["search_term"] + " " + suffix
    else:
        search_term = food_dict["search_term"]
    while len(data) < min_results:
        food_dicts = __add_item_url(food_dict, suffix, page, verbose)
        for food_dict in tqdm(food_dicts, leave=False):
            saved_food = food_exists(food_dict["item_url"], verbose)
            if saved_food is not None:
                if verbose:
                    print(f"Found {saved_food['name']} in database.")
                data.append(saved_food)
                if len(data) >= min_results:
                    break
            else:
                if __check_100g(food_dict, verbose):
                    food_dict.update(__fetch_macros(food_dict, verbose))
                    food_dict.update(__fetch_metadata(food_dict, verbose))
                    insert_food(food_dict, verbose)
                    data.append(food_dict)
                    if verbose:
                        print(f"Harvested {len(data)} / {min_results} results.")
                        print("--------------------------------------------------")
                    if len(data) >= min_results:
                        break
        page += 1
    if verbose:
        print(f"Found {len(data)} results for {search_term}.")
        print("==================================================")
    return data


def harvest(search_list, suffixes, verbose):
    harvested = []
    total_items = len(search_list) * len(suffixes) if suffixes else len(search_list)
    with tqdm(total=total_items) as pbar:
        for i, food in enumerate(search_list):
            for suf in suffixes or [""]:
                pbar.set_description(f"Harvesting {food} {suf}")
                food_info = __get_food_info(food, suf, verbose=verbose)
                harvested.append(food_info)
                pbar.update(1)
                if verbose:
                    print("-------------------------------------------------------")
                    print(f"Done: {i+1}/{total_items} ({(i+1)/total_items*100:.2f}%)")
                    print("-------------------------------------------------------\n")
    return harvested


with open(FOODS_JSON_PATH, "r", encoding="utf-8") as f:
    foods = json.load(f)
food_list = foods.get("data", [])

f = harvest(food_list, None, verbose=False)
