from typing import List
from fastapi import FastAPI
from db import DB_COLUMNS, execute_query
from models import Food

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
