import json
import time
import sqlite3

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from tqdm import tqdm

from db import food_exists, insert_food

MAX_REQUESTS = 5
REQUEST_DELAY_SECONDS = 60
FOOD_RESULTS = 5
FOODS_JSON_PATH = "resources/foods.json"


def __request(url, mode=None):
    for _ in range(MAX_REQUESTS):
        response = requests.get(url, timeout=60)
        if response.status_code == 429:
            if mode == "api":
                raise Exception("Too many requests")
            print(f"Too many requests, waiting {REQUEST_DELAY_SECONDS} seconds")
            time.sleep(REQUEST_DELAY_SECONDS)
        else:
            break
    if response.status_code != 200:
        print(f"Error requesting {url}: status code {response.status_code}")
        return None
    return response


def __add_item_url(food_dict, suf, page, verbose=False, mode=None):
    search_term = food_dict["search_term"] + " " + suf
    search_base_url = "https://www.fatsecret.es/calorías-nutrición/search?q="
    page_url = "&pg=" + str(page)
    url = search_base_url.strip() + search_term.strip().replace(" ", "+") + page_url
    if verbose:
        print(f"Searching on:\n{url}\n")
    response = __request(url, mode=mode)
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


def __check_100g(food_dict, verbose=False, mode=None):
    item_url = food_dict.get("item_url")
    soup = BeautifulSoup(__request(item_url, mode=mode).text, "html.parser")
    serving_size = soup.find("div", {"class": "serving_size black serving_size_value"})

    print(f"Checking if {food_dict['search_term']} is 100g -- {item_url}")
    if serving_size is not None and (
        serving_size.text == "100 g" or serving_size.text == "100 ml"
    ):
        print("This food is 100g.")
        print(serving_size.text)
        return serving_size
    else:
        print("This food is not 100g.")
        print(serving_size.text)
        return False


def __fetch_macros(food_dict, verbose=False, mode=None):
    if verbose:
        print(
            f"Gathering macros for {food_dict['search_term']} -- {food_dict['item_url']}\n"
        )
    soup = BeautifulSoup(
        __request(food_dict["item_url"], mode=mode).text, "html.parser"
    )
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


def __fetch_metadata(food_dict, verbose=False, mode=None):
    if verbose:
        print(
            f"Gathering metadata for {food_dict['search_term']} -- {food_dict['item_url']}\n"
        )
    url = food_dict["item_url"]
    try:
        response = __request(url, mode=mode)
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


def harvest_url(url, cat, subcat, verbose):
    if verbose:
        print(f"Harvesting from {url}")
    if food_exists(url, verbose):
        raise Exception(f"Food {url} already in database.")
    food_dict = {
        "item_url": url,
        "category": cat,
        "subcategory": subcat,
        "search_term": "",
    }
    food_info = __fetch_metadata(food_dict, verbose)
    if food_info is None:
        raise Exception(f"Error fetching metadata for {url}.")
    food_dict.update(food_info)
    food_info = __fetch_macros(food_dict, verbose)
    if food_info is None:
        raise Exception(f"Error fetching macros for {url}.")
    food_dict.update(food_info)
    if not __check_100g(food_dict, verbose):
        raise Exception(f"Food {url} is not 100g.")
    food_dict["serving_size"] = 0
    food_dict["times_selected"] = 0
    insert_food(food_dict, verbose)
    if food_exists(url, verbose) is None:
        raise Exception(f"Error inserting {url} into database.")
    return food_exists(url, verbose)
