import sqlite3

from pulp import *

KCALS_GRAM_FAT = 9
KCALS_GRAM_CARBS = 4
KCALS_GRAM_PROTEIN = 4

MIN_GRAMS = 5
MAX_GRAMS = 200


def calculate_results(
    prob,
    food_names,
    food_prots,
    food_fats,
    food_carbs,
    food_cals,
):
    ret = []
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
            ret.append(food)

    # Add the computation of the percentages of each macro by its kcals
    fat_kcals = sum([f["fat"] for f in ret]) * KCALS_GRAM_FAT
    carbs_kcals = sum([f["carbs"] for f in ret]) * KCALS_GRAM_CARBS
    protein_kcals = sum([f["protein"] for f in ret]) * KCALS_GRAM_PROTEIN

    total_kcals_by_macro = fat_kcals + carbs_kcals + protein_kcals
    total_kcals = sum([f["kcals"] for f in ret])

    ret.append(
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

    return ret


def solve_problem(params):
    target_kcals = params.get("target_kcals")
    max_fat_pct = params.get("max_fat_pct", 0.25)
    min_prot_pct = params.get("min_prot_pct", 0.40)
    food = params.get("food")
    penalty_protein = params.get("penalty_protein", 100)
    penalty_fat = params.get("penalty_fat", 100)
    penalty_kcals = params.get("penalty_kcals", 10)

    food_names = [f["name"] for f in food]
    food_names = [f.replace(" ", "_") for f in food_names]
    food_cals = [f["cals_per_g"] for f in food]
    food_fats = [f["fat_per_g"] for f in food]
    food_prots = [f["prot_per_g"] for f in food]
    food_carbs = [f["carb_per_g"] for f in food]

    ####################################################################################################

    target_kcals = 5 * 200
    min_prot_pct = 0.4
    max_fat_pct = 0.20
    serving_size_g, max_servings = [None], [None]
    max_servings = [
        min(MAX_GRAMS // serving_size_g[i], max_servings[i])
        for i in range(len(food_names))
    ]

    # Reset problem
    prob = LpProblem("The food problem", LpMinimize)

    prob_vars = LpVariable.dicts(
        name="food",
        indices=food_names,
        lowBound=MIN_GRAMS,
        upBound=max_servings,
        cat="Integer",
    )

    multipliers = LpVariable.dicts(
        "multiplier",
        food_names,
        lowBound=1,
        upBound=[max_servings[food_names.index(f)] for f in food_names],
        cat="Integer",
    )

    for f in food_names:
        prob += (
            prob_vars[f] == serving_size_g[food_names.index(f)] * multipliers[f],
            f"Min grams of {f}",
        )

    # Slack variables for constraints
    slack_protein = LpVariable("slack_protein", lowBound=0, cat="Continuous")
    slack_fat = LpVariable("slack_fat", lowBound=0, cat="Continuous")
    slack_kcals = LpVariable("slack_kcals", lowBound=0, cat="Continuous")

    # Objective = kcals
    prob += (
        lpSum([prob_vars[f] * food_cals[f] for food in food_names])
        + penalty_protein * slack_protein
        + penalty_fat * slack_fat
        + penalty_kcals * slack_kcals,
        "Total objective",
    )
    # Constraints = kcals, macros, grams
    # KCALS with slack
    prob += (
        lpSum([prob_vars[f] * food_cals[i] for i, f in enumerate(food_names)])
        + slack_kcals
        == target_kcals,
        "Max kcals",
    )

    # MACROS with slack
    # Protein >= target
    protein_constraint = lpSum(
        [prob_vars[f] * food_prots[i] for i, f in enumerate(food_names)]
    )
    prob += (
        protein_constraint + slack_protein
        >= min_prot_pct * target_kcals / KCALS_GRAM_PROTEIN,
        "Min protein",
    )

    # Fat <= target
    fat_constraint = lpSum(
        [prob_vars[f] * food_fats[i] for i, f in enumerate(food_names)]
    )
    prob += (
        fat_constraint - slack_fat <= max_fat_pct * target_kcals / KCALS_GRAM_FAT,
        "Max fat",
    )

    # Solve
    prob.solve()

    result = calculate_results(
        prob=prob,
        food_names=food_names,
        food_prots=food_prots,
        food_fats=food_fats,
        food_carbs=food_carbs,
        food_cals=food_cals,
    )

    return result
