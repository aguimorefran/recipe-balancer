import os

import psycopg2
from config import DB_HOST, DB_PASSWORD, DB_PORT, DB_USER
from unidecode import unidecode

FOOD_COLS = [
    ("id", "SERIAL PRIMARY KEY"),
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
]


def init_tables(conn):
    # foods
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS foods ("
        + ",".join([f"{col} {dtype}" for col, dtype in FOOD_COLS])
        + ")"
    )
    # Check if table exists
    cur.execute(
        "SELECT EXISTS ("
        "SELECT FROM information_schema.tables "
        "WHERE table_schema = 'public' "
        "AND table_name = 'foods'"
        ")"
    )
    conn.commit()
    cur.close()


def create_conn():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname="postgres",
    )
    init_tables(conn)
    return conn


def fetch_food(conn, name):
    cur = conn.cursor()
    if name is None:
        cur.execute("SELECT * FROM foods")
    else:
        name = unidecode(name).lower().strip()
        query = "SELECT * FROM foods WHERE "
        query += " OR ".join(
            [
                f"LOWER({col}) LIKE '%{name}%'"
                for col in ["name", "brand", "category", "subcategory"]
            ]
        )
        cur.execute(query)
    result = cur.fetchall()
    cur.close()
    result = [{FOOD_COLS[i][0]: result[0][i] for i in range(len(FOOD_COLS))}]

    return result


def food_exists(conn, url, verbose=False):
    cur = conn.cursor()
    cur.execute("SELECT * FROM foods WHERE item_url = %s", (url,))
    result = cur.fetchall()
    if len(result) > 0:
        return {FOOD_COLS[i][0]: result[0][i] for i in range(len(FOOD_COLS))}
    return None


def insert_food(conn, food_dict, verbose=False):
    try:
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

        cur.execute(
            "INSERT INTO foods (search_term, name, category, subcategory, brand, item_url, cals_per_g, fat_per_g, carb_per_g, prot_per_g, serving_size) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
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
            ),
        )

        conn.commit()
        cur.close()
        return True
    except Exception as e:
        return False
