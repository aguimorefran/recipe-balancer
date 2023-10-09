import requests
import time
from db import init_db, execute_query, insert_food
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

MAX_REQUESTS = 5
REQUEST_DELAY_SECONDS = 60
FOOD_RESULTS = 3

init_db()


def __request_info(url):
    for _ in range(MAX_REQUESTS):
        response = requests.get(url, timeout=60)
        if response.status_code == 429:
            time.sleep(REQUEST_DELAY_SECONDS)
        else:
            break
    if response.status_code != 200:
        print(f"Error requesting {url}: status code {response.status_code}")
        return None
    return response


def __get_food_urls(search_term, page=0, verbose=False):
    search_base_url = "https://www.fatsecret.es/calorías-nutrición/search?q="
    page_url = "&pg=" + str(page)
    url = search_base_url.strip() + search_term.strip().replace(" ", "+") + page_url
    if verbose:
        print(f"Searching on {url}")
    response = __request_info(url)
    if response is None:
        return None
    soup = BeautifulSoup(response.text, "html.parser")
    food_links = soup.find_all("td", {"class": "borderBottom"})
    results = [
        (
            link.find("a", {"class": "prominent"}).text,
            "https://fatsecret.es" + link.find("a", {"class": "prominent"})["href"],
        )
        for link in food_links
    ]
    return tuple(results)


def __check_100g(food_tuple, verbose=False):
    if verbose:
        print(f"Checking if {food_tuple[0]} is 100g -- {food_tuple[1]}")
    soup = BeautifulSoup(__request_info(food_tuple[1]).text, "html.parser")
    serving_size = soup.find("div", {"class": "serving_size black serving_size_value"})
    return serving_size is not None and serving_size.text == "100 g"


def __get_macros(food_tuple, verbose=False):
    if verbose:
        print(f"Gathering macros for {food_tuple[0]} -- {food_tuple[1]}")
    soup = BeautifulSoup(__request_info(food_tuple[1]).text, "html.parser")
    macros = soup.find("div", {"class": "factPanel"})
    if macros is None:
        print(f"No macros found for {food_tuple[0]}")
        return None
    macro_list = [
        macro.text for macro in macros.find_all("div", {"class": "factValue"})
    ]
    if len(macro_list) < 4:
        print(f"Not enough macros found for {food_tuple[0]}")
        return None
    cals, fat, carb, prot = [
        float(macro.replace("g", "").replace(",", ".")) for macro in macro_list[:4]
    ]
    return {"cals": cals, "fat": fat, "carb": carb, "prot": prot}


def __get_metadata(food_tuple, verbose=False):
    if verbose:
        print(f"Gathering metadata for {food_tuple[0]} -- {food_tuple[1]}")
    url = food_tuple[1]
    try:
        response = __request_info(url)
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

    return {"brand": brand, "name": name}


def __get_food_info(search_term, min_results=FOOD_RESULTS, verbose=False):
    data = []
    page = 0
    while len(data) < min_results:
        if verbose:
            print("Searching for", search_term, "on page", page)
        tuples = __get_food_urls(search_term, page, verbose)

        existing_urls = execute_query("SELECT item_url FROM food")
        existing_urls = [url[0] for url in existing_urls]

        tuples_new = [t for t in tuples if t[1] not in existing_urls]
        if verbose:
            print("Found", len(tuples_new), "new results for", search_term)

        for t in tuples_new:
            if __check_100g(t):
                macros = __get_macros(t, verbose)
                if macros is not None:
                    metadata = __get_metadata(t)
                    data.append({**macros, **metadata, "item_url": t[1]})
                if len(data) >= min_results:
                    break
        page += 1
    if verbose:
        print("Found", len(data), "results for", search_term)
    return data


def harvest(food_list, market_name="", verbose=False):
    """
    Harvests food data for a given list of food items and market name.

    Args:
        food_list (list): A list of food items to harvest data for.
        market_name (str, optional): The name of the market to search for the food items. Defaults to "".
        verbose (bool, optional): Whether to print verbose output. Defaults to False.

    Returns:
        list: A list of harvested food items with additional information.
    """
    if verbose:
        print("Harvesting food data. Number of foods:", len(food_list))
    harvested = []
    for food_item in food_list:
        if verbose:
            print("Harvesting", food_item["search_term"])
        search_term = food_item["search_term"] + " " + market_name
        food_info = __get_food_info(search_term, verbose=verbose)
        for info in food_info:
            new_item = food_item.copy()
            for key, value in info.items():
                new_item[key] = value
            harvested.append(new_item)

            # Insert into database
            insert_food(new_item, verbose=verbose)
    return harvested
