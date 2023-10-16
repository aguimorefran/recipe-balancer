import sqlite3

from pulp import *

KCALS_GRAM_FAT = 9
KCALS_GRAM_CARBS = 4
KCALS_GRAM_PROTEIN = 4

MIN_GRAMS = 5
MAX_GRAMS = 200


PENALTY_PROT = 100
PENALTY_FAT = 100
PENALTY_KCALS = 10


food_ids = [60, 62, 68, 77, 92]

conn = sqlite3.connect("fatsecret_scrapper/food.db")
c = conn.cursor()

foods = c.execute(
    "SELECT * FROM food WHERE id IN ({})".format(",".join("?" * len(food_ids))),
    food_ids,
).fetchall()

food_names = [f[1] for f in foods]
food_names = [f.replace(" ", "_") for f in food_names]
food_cals = [f[7] for f in foods]
food_fats = [f[8] for f in foods]
food_carbs = [f[9] for f in foods]
food_prots = [f[10] for f in foods]

# Update food_names after replacing spaces with underscores
food_names = [f.replace(" ", "_") for f in food_names]


####################################################################################################

# Ask for params
# kcals_objetive = ask_calories()
# prot_pct = ask_prot_pct()
# fat_pct = ask_fat_pct()
# gram_multiplier, max_grams = ask_params(food_names)
kcals_objetive = 2000
prot_pct = 0.3
fat_pct = 0.3
gram_multiplier = [1] * len(food_names)
max_grams = [MAX_GRAMS] * len(food_names)

# Reset problem
prob = LpProblem("The food problem", LpMinimize)

prob_vars = LpVariable.dicts(
    name="food",
    indices=food_names,
    lowBound=MIN_GRAMS,
    upBound=max_grams,
    cat="Integer",
)

multipliers = LpVariable.dicts(
    "multiplier",
    food_names,
    lowBound=1,
    upBound=[max_grams[food_names.index(f)] for f in food_names],
    cat="Integer",
)

for f in food_names:
    var = prob_vars[f]
    var.upBound = max_grams[food_names.index(f)]


# Slack variables for constraints
slack_protein = LpVariable("slack_protein", lowBound=0, cat="Continuous")
slack_fat = LpVariable("slack_fat", lowBound=0, cat="Continuous")
slack_kcals = LpVariable("slack_kcals", lowBound=0, cat="Continuous")

# Objective = kcals
prob += (
    lpSum([prob_vars[f] * food_cals[i] for i, f in enumerate(food_names)])
    + PENALTY_PROT * slack_protein
    + PENALTY_FAT * slack_fat
    + PENALTY_KCALS * slack_kcals,
    "Total objective",
)
# Constraints = kcals, macros, grams
# KCALS with slack
prob += (
    lpSum([prob_vars[f] * food_cals[i] for i, f in enumerate(food_names)]) + slack_kcals
    == kcals_objetive,
    "Max kcals",
)

# MACROS with slack
# Protein >= target
protein_constraint = lpSum(
    [prob_vars[f] * food_prots[i] for i, f in enumerate(food_names)]
)
prob += (
    protein_constraint + slack_protein
    >= prot_pct * kcals_objetive / KCALS_GRAM_PROTEIN,
    "Min protein",
)

# Fat <= target
fat_constraint = lpSum([prob_vars[f] * food_fats[i] for i, f in enumerate(food_names)])
prob += (
    fat_constraint - slack_fat <= fat_pct * kcals_objetive / KCALS_GRAM_FAT,
    "Max fat",
)


# Solve
prob.solve()


def calculate_results(
    prob,
    food_names,
    food_prots,
    food_fats,
    food_carbs,
    food_cals,
    KCALS_GRAM_FAT,
    KCALS_GRAM_CARBS,
    KCALS_GRAM_PROTEIN,
):
    result = []
    # Print the name of the vars and the value
    for v in prob.variables():
        if v.varValue > 0:
            food = {}
            print(v.name, "=", v.varValue)
            name_no_prefix = v.name.replace("food_", "")
            if "multiplier" in v.name or "slack" in v.name:
                continue
            food["name"] = v.name
            food["grams"] = v.varValue
            food["protein_per_100g"] = round(
                food_prots[food_names.index(name_no_prefix)] * 100, 3
            )
            food["fat_per_100g"] = round(
                food_fats[food_names.index(name_no_prefix)] * 100, 3
            )
            food["carbs_per_100g"] = round(
                food_carbs[food_names.index(name_no_prefix)] * 100, 3
            )
            food["kcals_per_100g"] = round(
                food_cals[food_names.index(name_no_prefix)] * 100, 3
            )

            food["protein"] = round(food["protein_per_100g"] * food["grams"] / 100, 3)
            food["fat"] = round(food["fat_per_100g"] * food["grams"] / 100, 3)
            food["carbs"] = round(food["carbs_per_100g"] * food["grams"] / 100, 3)
            food["kcals"] = round(food["kcals_per_100g"] * food["grams"] / 100, 3)
            result.append(food)

    # Add the computation of the percentages of each macro by its kcals
    fat_kcals = sum([f["fat"] for f in result]) * KCALS_GRAM_FAT
    carbs_kcals = sum([f["carbs"] for f in result]) * KCALS_GRAM_CARBS
    protein_kcals = sum([f["protein"] for f in result]) * KCALS_GRAM_PROTEIN

    total_kcals_by_macro = fat_kcals + carbs_kcals + protein_kcals
    total_kcals = sum([f["kcals"] for f in result])

    result.append(
        {
            "results": {
                "fat_kcals": round(fat_kcals, 2),
                "carbs_kcals": round(carbs_kcals, 2),
                "protein_kcals": round(protein_kcals, 2),
                "total_kcals": round(total_kcals, 2),
                "total_kcals_by_macro": round(total_kcals_by_macro, 2),
                "fat_pct": round(fat_kcals / total_kcals_by_macro, 2),
                "carbs_pct": round(carbs_kcals / total_kcals_by_macro, 2),
                "protein_pct": round(protein_kcals / total_kcals_by_macro, 2),
            },
        }
    )

    return result


result = calculate_results()

for f in result:
    print(json.dumps(f, indent=4, ensure_ascii=False))
