import os
import sqlite3

DB_COLUMNS = [
    ("search_term", "TEXT"),
    ("name", "TEXT"),
    ("category", "TEXT"),
    ("subcategory", "TEXT"),
    ("brand", "TEXT"),
    ("item_url", "TEXT"),
    ("cals", "REAL"),
    ("fat", "REAL"),
    ("carb", "REAL"),
    ("prot", "REAL"),
    ("sugar", "REAL"),
    ("fiber", "REAL"),
    ("cholesterol", "REAL"),
    ("sodium", "REAL"),
    ("potassium", "REAL"),
    ("calcium", "REAL"),
    ("others", "TEXT"),
    ("serving_size", "REAL"),
    ("serving_size_unit", "TEXT"),
    ("serving_size_g", "REAL"),
    ("serving_size_ml", "REAL"),
]


def init_db(delete=False):
    if delete:
        if os.path.isfile("food.db"):
            os.remove("food.db")
    if os.path.isfile("food.db"):
        conn = sqlite3.connect("food.db")
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='food'")
        result = c.fetchone()
        if result is None:
            print("Error: food table does not exist")
            return False
        else:
            c.execute("SELECT * FROM food LIMIT 1")
            result = c.fetchone()
            if result is None:
                print("Error: food table is empty")
                return False
    else:
        conn = sqlite3.connect("food.db")
        c = conn.cursor()
        c.execute(
            "CREATE TABLE food ("
            + ", ".join([f"{col[0]} {col[1]}" for col in DB_COLUMNS])
            + ")"
        )
        conn.commit()
        c.execute("INSERT INTO food VALUES ('test', 100, 10, 20, 30)")
        conn.commit()
    conn.close()
    return True


def execute_query(query):
    try:
        conn = sqlite3.connect("food.db")
        c = conn.cursor()
        c.execute(query)
        conn.commit()
        result = c.fetchall()
        conn.close()
        return result
    except Exception as e:
        print(f"Error executing query: {e}")
        return None


def food_exists(item_url, verbose=False):
    try:
        if verbose:
            print(f"Checking if food exists: {item_url}")
        conn = sqlite3.connect("food.db")
        c = conn.cursor()
        c.execute("SELECT * FROM food WHERE item_url=?", (item_url,))
        result = c.fetchone()
        conn.close()
        if result:
            return dict(zip([col[0] for col in DB_COLUMNS], result))
        return None
    except Exception as e:
        print(f"Error checking if food exists: {e}")
        return None


def insert_food(food_dict, verbose=False):
    try:
        conn = sqlite3.connect("food.db")
        c = conn.cursor()
        values = []
        for col in DB_COLUMNS:
            if col[0] in food_dict:
                values.append(food_dict[col[0]])
            else:
                values.append(None)
        c.execute(
            "INSERT INTO food VALUES (" + ", ".join(["?" for _ in DB_COLUMNS]) + ")",
            values,
        )
        conn.commit()
        conn.close()
        if verbose:
            print(f"Successfully inserted food with name {food_dict['name']}")
        return True
    except Exception as e:
        if verbose:
            print(f"Error inserting food with name {food_dict['name']}: {e}")
        return False
