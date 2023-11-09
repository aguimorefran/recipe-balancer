import os

# import psycopg2
import sqlite3
# from config import DB_HOST, DB_PASSWORD, DB_PORT, DB_RESET, DB_USER
from unidecode import unidecode

FOOD_COLS = [
    # ("id", "SERIAL PRIMARY KEY"),
    ("id", "INTEGER PRIMARY KEY"),
    ("search_term", "TEXT"),
    ("name", "TEXT"),
    ("category", "TEXT"),
    ("subcategory", "TEXT"),
    ("brand", "TEXT"),
    ("item_url", "TEXT"),
    ("cals_per_g", "REAL"),
    ("fat_per_g", "REAL"),
    ("carb_per_g", "REAL"),
    ("prot_per_g", "REAL"),
    ("serving_size", "REAL"),
    ("times_selected", "INTEGER"),
]

FOOD_MEAL_COLS = [
    ("id", "SERIAL PRIMARY KEY"),
    ("food_id", "INTEGER"),
    ("grams", "REAL"),
    ("meal_id", "INTEGER"),
]

MEAL_COLS = [
    ("id", "SERIAL PRIMARY KEY"),
    ("name", "TEXT"),
    ("description", "TEXT"),
    ("cals", "REAL"),
    ("fat_pct", "REAL"),
    ("carb_pct", "REAL"),
    ("prot_pct", "REAL"),
    ("fat_grams", "REAL"),
    ("carb_grams", "REAL"),
    ("prot_grams", "REAL"),
    ("date_created", "TIMESTAMP"),
]


def init_tables(conn):
    cur = conn.cursor()
    print("DB_RESET:", os.getenv('DB_RESET'))
    tables = ["foods", "meals", "food_meals"]
    columns = [FOOD_COLS, MEAL_COLS, FOOD_MEAL_COLS]

    db_reset = os.getenv('DB_RESET', 'false').lower() == 'true'
    if db_reset:
        print("Resetting database...")
        for table in tables:
            cur.execute(f"DROP TABLE IF EXISTS {table}")

    for table, cols in zip(tables, columns):
        cur.execute(
            f"CREATE TABLE IF NOT EXISTS {table} ("
            + ",".join([f"{col} {dtype}" for col, dtype in cols])
            + ")"
        )

    conn.commit()
    cur.close()


def create_conn():
    conn = sqlite3.connect("foods.db")
    init_tables(conn)


def fetch_food(name):
    # cur = conn.cursor()
    conn = sqlite3.connect("foods.db")
    cur = conn.cursor()
    name = unidecode(name).lower().strip()
    query = "SELECT * FROM foods WHERE "
    query += " OR ".join(
        [
            f"LOWER({col}) LIKE ?"
            for col in ["name", "brand", "category", "subcategory"]
        ]
    )
    params = [f'%{name}%'] * 4
    query += " ORDER BY times_selected DESC, name ASC"
    cur.execute(query, params)
    result = cur.fetchall()
    print(result)
    cur.close()
    result = (
        [{FOOD_COLS[i][0]: row[i] for i in range(len(FOOD_COLS))} for row in result]
        if len(result) > 0
        else []
    )
    return result

def inc_selection(food_id):
    # cur = conn.cursor()
    conn = sqlite3.connect("foods.db")
    cur = conn.cursor()
    cur.execute(
        "UPDATE foods SET times_selected = times_selected + 1 WHERE id = ?", (food_id,)
    )
    conn.commit()
    cur.close()


def food_exists(url, verbose=False):
    conn = sqlite3.connect("foods.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM foods WHERE item_url = ?", (url,))
    result = cur.fetchall()
    cur.close()
    return {FOOD_COLS[i][0]: result[0][i] for i in range(len(FOOD_COLS))} if result else None


def insert_food(food_dict, verbose=False, manual=False):
    try:
        conn = sqlite3.connect("foods.db")
        cur = conn.cursor()
        values = []
        for col in FOOD_COLS:
            if col[0] in food_dict:
                if isinstance(food_dict[col[0]], str):
                    food_dict[col[0]] = unidecode(food_dict[col[0]])
                values.append(food_dict[col[0]])
            else:
                values.append(None)
        name = unidecode(food_dict["name"]).strip()
        brand = unidecode(food_dict["brand"]).strip()
        category = unidecode(food_dict["category"]).lower().strip()
        subcategory = unidecode(food_dict["subcategory"]).lower().strip()
        item_url = food_dict["item_url"]
        cals_per_g = food_dict["cals_per_g"]
        fat_per_g = food_dict["fat_per_g"]
        carb_per_g = food_dict["carb_per_g"]
        prot_per_g = food_dict["prot_per_g"]
        serving_size = food_dict["serving_size"]
        times_selected = food_dict["times_selected"]

        cur.execute(
            "INSERT INTO foods (search_term, name, category, subcategory, brand, item_url, cals_per_g, fat_per_g, carb_per_g, prot_per_g, serving_size, times_selected) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                name,
                name,
                category,
                subcategory,
                brand,
                item_url,
                cals_per_g,
                fat_per_g,
                carb_per_g,
                prot_per_g,
                serving_size,
                times_selected,
            ),
        )

        conn.commit()
        cur.close()
        return True
    except Exception as e:
        return e
