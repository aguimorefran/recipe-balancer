from typing import List, Dict
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from db import DB_COLUMNS, execute_query
from balancer import solve_problem as solve
from harvest import harvest_url as harvest
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/search_food")
def search_food(name: str = None):
    """
    Searches for foods in the database that match the given name or brand.
    If name is None, returns all the foods in the database.
    """
    if name == "":
        return {"foods": []}
    if name is None:
        fetched_foods = execute_query("SELECT * FROM food")
    else:
        name_words = name.split()
        where_clause = " AND ".join(
            [
                f"(name LIKE '%{word}%' OR brand LIKE '%{word}%' OR category LIKE '%{word}%' OR subcategory LIKE '%{word}%')"
                for word in name_words
            ]
        )
        fetched_foods = execute_query(f"SELECT * FROM food WHERE {where_clause}")
    foods = []
    for fetched_food in fetched_foods:
        food = {}
        for i, col in enumerate(DB_COLUMNS):
            food[col[0]] = fetched_food[i]
        foods.append(food)
    response = Response()
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Max-Age"] = "86400"
    return {"foods": foods}


@app.get("/food")
def get_food(food_id: int):
    """
    Gets a food from the database given its id.
    """
    fetched_foods = execute_query(f"SELECT * FROM food WHERE id = {food_id}")
    foods = []
    for fetched_food in fetched_foods:
        food = {}
        for i, col in enumerate(DB_COLUMNS):
            food[col[0]] = fetched_food[i]
        foods.append(food)
    response = Response()
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Max-Age"] = "86400"
    return {"results": foods}


@app.get("/harvest_url")
def harvest_url(url: str, category: str, subcategory: str):
    """
    Harvests a food from the given url.
    """
    try:
        result = harvest(url, category, subcategory, True)
        response = Response()
    except Exception as e:
        response = Response(status_code=500)
        return {"error": str(e)}
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Max-Age"] = "86400"
    return {"result": result}


@app.post("/solve_problem")
async def solve_problem(data: dict):
    print(json.dumps(data, indent=4))
    target_kcals = data["target_kcals"]
    max_fat_pct = data["max_fat_pct"]
    min_prot_pct = data["min_prot_pct"]
    penalty_protein = data["penalty_protein"]
    penalty_fat = data["penalty_fat"]
    penalty_kcals = data["penalty_kcals"]
    foods = data["foods"]

    try:
        result = solve(
            {
                "target_kcals": target_kcals,
                "max_fat_pct": max_fat_pct,
                "min_prot_pct": min_prot_pct,
                "foods": foods,
                "penalty_protein": penalty_protein,
                "penalty_fat": penalty_fat,
                "penalty_kcals": penalty_kcals,
            }
        )

    except Exception as e:
        response = Response(status_code=500)
        return {"error": str(e)}

    return {"result": result}
