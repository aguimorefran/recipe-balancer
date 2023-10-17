from typing import List
from fastapi import FastAPI
from db import DB_COLUMNS, execute_query
from models import Food
from balancer import solve_problem as solve

app = FastAPI()


def map_row_to_food(row):
    """
    Maps a row from the database to a Food object.
    """
    return Food(**dict(zip([col[0] for col in DB_COLUMNS], row)))


def fetch_all_db():
    """
    Returns a list of all foods in the database, except for the first one (which is a placeholder).
    """
    fetched_foods = execute_query("SELECT * FROM food")
    foods = [map_row_to_food(food) for food in fetched_foods if food[0] != 1]
    return foods


@app.get("/get_all_foods", response_model=List[Food])
def get_all_foods():
    """
    Returns a list of all foods in the database, except for the first one (which is a placeholder).
    """
    return fetch_all_db()


@app.get("/search_food/{name}", response_model=List[Food])
def search_food(name: str):
    """
    Searches for foods in the database that match the given name or brand.
    """
    name_words = name.split()
    where_clause = " AND ".join(
        [f"(name LIKE '%{word}%' OR brand LIKE '%{word}%')" for word in name_words]
    )
    fetched_foods = execute_query(f"SELECT * FROM food WHERE {where_clause}")
    foods = [map_row_to_food(food) for food in fetched_foods]
    return foods


foods_test = [
    {
        "id": 103,
        "search_term": "cacao puro valor",
        "name": "Cacao Puro Natural 100%",
        "category": "chocolate",
        "subcategory": "cacao",
        "brand": "Valor",
        "item_url": "https://fatsecret.es/calor%C3%ADas-nutrici%C3%B3n/valor/cacao-puro-natural-100/100g",
        "cals_per_g": 3.39,
        "fat_per_g": 0.11,
        "carb_per_g": 0.17,
        "prot_per_g": 0.25,
        "serving_size": 10,
        "max_servings": 3,
    },
    {
        "id": 101,
        "search_term": "copos de avena",
        "name": "Copos de Avena",
        "category": "cereales",
        "subcategory": "avena",
        "brand": "Mercadona",
        "item_url": "https://fatsecret.es/calor%C3%ADas-nutrici%C3%B3n/mercadona/copos-de-avena/100g",
        "cals_per_g": 3.75,
        "fat_per_g": 0.07,
        "carb_per_g": 0.59,
        "prot_per_g": 0.14,
        "serving_size": 5,
        "max_servings": 50,
    },
    {
        "id": 39,
        "search_term": "cacahuetes",
        "name": "Cacahuetes Tostados",
        "category": "frutos secos",
        "subcategory": "cacahuetes",
        "brand": "Carrefour",
        "item_url": "https://fatsecret.es/calor%C3%ADas-nutrici%C3%B3n/carrefour/cacahuetes-tostados/100g",
        "cals_per_g": 6.15,
        "fat_per_g": 0.5,
        "carb_per_g": 0.062,
        "prot_per_g": 0.29,
        "serving_size": 5,
        "max_servings": 20,
    },
    {
        "id": 67,
        "search_term": "avellanas laminadas",
        "name": "Avellanas Tostadas",
        "category": "frutos secos",
        "subcategory": "avellanas",
        "brand": "Carrefour",
        "item_url": "https://fatsecret.es/calor%C3%ADas-nutrici%C3%B3n/carrefour/avellanas-tostadas/100g",
        "cals_per_g": 7.12,
        "fat_per_g": 0.68,
        "carb_per_g": 0.038,
        "prot_per_g": 0.17,
        "serving_size": 5,
        "max_servings": 20,
    },
]
target_kcals = 2000
max_fat_pct = 0.25
min_prot_pct = 0.40
penalty_protein = 100
penalty_fat = 100
penalty_kcals = 10


@app.get("/solve_problem")
def solve_problem():
    """
    Calls the solve_problem function to solve a problem.
    """
    result = solve(
        {
            "target_kcals": target_kcals,
            "max_fat_pct": max_fat_pct,
            "min_prot_pct": min_prot_pct,
            "foods": foods_test,
            "penalty_protein": penalty_protein,
            "penalty_fat": penalty_fat,
            "penalty_kcals": penalty_kcals,
        }
    )
    return {"result": result}
