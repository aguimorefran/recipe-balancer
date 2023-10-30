import json
from typing import Dict, List
import openai

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from harvest import harvest_url as harvest

from balancer import solve_problem as solve
from db import create_conn, fetch_food, inc_selection

from keys import OPENAI_KEY

conn = create_conn()

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
    fetched_foods = fetch_food(conn, name)
    response = Response()
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Max-Age"] = "86400"
    return {"foods": fetched_foods}


@app.get("/inc_selection")
def increment_selections(food_id: int):
    """
    Increments the number of times the food has been selected.
    """
    try:
        result = inc_selection(conn, food_id)
        response = Response()
    except Exception as e:
        response = Response(status_code=500)
        return {"error": str(e)}
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Max-Age"] = "86400"
    return {"result": result}


@app.get("/harvest_url")
def harvest_url(url: str, category: str, subcategory: str):
    """
    Harvests a food from the given url.
    """
    try:
        result = harvest(conn, url, category, subcategory, True)
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


@app.post("/generate_recipe")
async def generate_recipe(data: dict):
    foods = data["foods"]
    course = data["course"].lower()
    names = [food["name"] for food in foods]
    foods_string = ""
    for i in range(len(names)):
        foods_string += f"{names[i]}"

    openai.api_key = OPENAI_KEY

    if course != "entire day":
        system_prompt = f"""
        You are a cook in a restaurant. You are skilled at creating recipes with the existing ingredients."""
        user_prompt = f"""
        Create three possible recipes for {course} using JUST the following ingredients, and dont add others: {foods_string}.
        Give an overall description of how to prepare it. You MUST return a JSON format response like:
        {{
            "recipes": [
                {{
                    "name": "Recipe Name",
                    "preparation": "Recipe preparation"
                }},
                {{
                    "name": "Recipe Name",
                    "preparation": "Recipe preparation"
                }},
                {{
                    "name": "Recipe Name",
                    "preparation": "Recipe preparation"
                }}
            ]
        }}
        Add HTML tags to the response to format it.
        """
    elif course == "entire day":
        system_prompt = f"""
        You are a cook in a restaurant. You are skilled at creating recipes with the existing ingredients."""
        user_prompt = f"""
        Create a full meal plan for an entire day using JUST the following ingredients, and dont add others: {foods_string}.

        You MUST return a JSON format response like:
        {{
            "meal_plans": [
                {{
                    "name": "Meal plan 1",
                    "breakfast": "Meal description",
                    "lunch": "Meal description",
                    "dinner": "Meal description",
                    "snack": "Meal description"
                }},
                {{
                    "name": "Meal plan 2",
                    "breakfast": "Meal description",
                    "lunch": "Meal description",
                    "dinner": "Meal description",
                    "snack": "Meal description"
                }},
                {{
                    "name": "Meal plan 3",
                    "breakfast": "Meal description",
                    "lunch": "Meal description",
                    "dinner": "Meal description",
                    "snack": "Meal description"
                }}
            ]
        }}

        I repeat, dont add other ingredients. Add HTML tags to the response to format it. Use the exact names of the ingredients.
        """

    completion = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=f"{system_prompt}\n{user_prompt}",
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.5,
    )

    response = completion.choices[0].text

    print(response)

    return {"result": response}
