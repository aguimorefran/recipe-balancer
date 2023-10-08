import requests
import time
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from tqdm import tqdm

MAX_REQUESTS = 5
REQUEST_DELAY_SECONDS = 60
MIN_RESULTS = 3


def request_info(url):
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


def get_food_urls(food_name, page=0, verbose=False):
    search_base_url = "https://www.fatsecret.es/calorías-nutrición/search?q="
    page_url = "&pg=" + str(page)
    url = search_base_url.strip() + food_name.strip().replace(" ", "+") + page_url
    if verbose:
        print(f"Searching on {url}")
    response = request_info(url)
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


def check_100g(food_tuple, verbose=False):
    if verbose:
        print(f"Checking if {food_tuple[0]} is 100g -- {food_tuple[1]}")
    soup = BeautifulSoup(request_info(food_tuple[1]).text, "html.parser")
    serving_size = soup.find("div", {"class": "serving_size black serving_size_value"})
    return serving_size is not None and serving_size.text == "100 g"


def get_macros(food_tuple, verbose=False):
    if verbose:
        print(f"Gathering macros for {food_tuple[0]} -- {food_tuple[1]}")
    soup = BeautifulSoup(request_info(food_tuple[1]).text, "html.parser")
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


def get_metadata(food_tuple, verbose=False):
    if verbose:
        print(f"Gathering metadata for {food_tuple[0]} -- {food_tuple[1]}")
    url = food_tuple[1]
    try:
        response = request_info(url)
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

    return {"brand": brand}


def get_food_info(food_name, min_results=MIN_RESULTS, verbose=False):
    data = []
    tuples = []
    page = 0
    while len(tuples) < min_results:
        if verbose:
            print(f"Searching for {food_name} on page {page}")
        new_tuples = get_food_urls(food_name, page, verbose)
        tuples += [t for t in new_tuples if check_100g(t, verbose)]
        if verbose:
            print(f"Tuples for {food_name} found: {len(tuples)}")
        page += 1
    for t in tuples:
        macros = get_macros(t, verbose)
        if macros is not None:
            metadata = get_metadata(t, verbose)
            data.append({**macros, **metadata})
    return data


def harvest_info(food_dict_list, min_results=MIN_RESULTS, verbose=False):
    pbar = tqdm(total=len(food_dict_list))
    pbar.set_description("Getting food info")
    pbar.refresh()

    data = []
    for food_dict in food_dict_list:
        name = food_dict["name"]
        cat = food_dict["category"]
        subcat = food_dict["subcategory"]
        pbar.set_description(f"Getting info for {name} ({cat} - {subcat})")

        new_elem = {
            "name": name,
            "category": cat,
            "subcategory": subcat,
        }
        harvested_data = get_food_info(name, min_results, verbose)
        for d in harvested_data:
            new_elem.update(d)

        data.append(new_elem)
        pbar.update(1)
        pbar.refresh()

    return data
