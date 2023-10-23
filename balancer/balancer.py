import sqlite3

from pulp import *

KCALS_GRAM_FAT = 9
KCALS_GRAM_CARBS = 4
KCALS_GRAM_PROTEIN = 4

MIN_GRAMS = 5
MAX_GRAMS = 2000


def parse_result(prob, foods):
    result = {}

    result["target_kcals"] = round(prob.objective.value(), 2)
    result["problem_status"] = LpStatus[prob.status]

    food_names = [f["name"] for f in foods]
    food_cals = [f["cals_per_g"] for f in foods]
    food_fats = [f["fat_per_g"] for f in foods]
    food_carbs = [f["carb_per_g"] for f in foods]
    food_prots = [f["prot_per_g"] for f in foods]

    fat_kcals = 0
    carb_kcals = 0
    protein_kcals = 0

    food_results = []

    for v in prob.variables():
        if "slack" in v.name:
            result[v.name] = round(v.varValue, 2)
        if "food" in v.name:
            food_name = v.name[5:].replace("_", " ")
            food_idx = food_names.index(food_name)
            food_results.append(
                {
                    "name": food_name,
                    "grams": round(v.varValue, 2),
                    "cals": round(v.varValue * food_cals[food_idx], 2),
                    "fat_grams": round(v.varValue * food_fats[food_idx], 2),
                    "carb_grams": round(v.varValue * food_carbs[food_idx], 2),
                    "protein_grams": round(v.varValue * food_prots[food_idx], 2),
                    "fat_kcals": round(
                        v.varValue * food_fats[food_idx] * KCALS_GRAM_FAT, 2
                    ),
                    "carb_kcals": round(
                        v.varValue * food_carbs[food_idx] * KCALS_GRAM_CARBS, 2
                    ),
                    "protein_kcals": round(
                        v.varValue * food_prots[food_idx] * KCALS_GRAM_PROTEIN, 2
                    ),
                }
            )
            fat_kcals += v.varValue * food_fats[food_idx] * KCALS_GRAM_FAT
            carb_kcals += v.varValue * food_carbs[food_idx] * KCALS_GRAM_CARBS
            protein_kcals += v.varValue * food_prots[food_idx] * KCALS_GRAM_PROTEIN
    total_kcals = fat_kcals + carb_kcals + protein_kcals
    result["fat_kcal_pctg"] = fat_kcals / total_kcals
    result["carb_kcal_pctg"] = carb_kcals / total_kcals
    result["protein_kcal_pctg"] = protein_kcals / total_kcals

    result["food_results"] = food_results

    return result


def solve_problem(params):
    target_kcals = params["target_kcals"]
    max_fat_pct = params["max_fat_pct"]
    min_prot_pct = params["min_prot_pct"]
    foods = params["foods"]
    penalty_protein = params["penalty_protein"]
    penalty_fat = params["penalty_fat"]
    penalty_kcals = params["penalty_kcals"]

    food_names = [f["name"] for f in foods]
    food_cals = [f["cals_per_g"] for f in foods]
    food_fats = [f["fat_per_g"] for f in foods]
    food_carbs = [f["carb_per_g"] for f in foods]
    food_prots = [f["prot_per_g"] for f in foods]
    gram_multiplier = [f["serving_size"] for f in foods]
    max_servings = [f["max_servings"] for f in foods]
    max_grams = [f["max_servings"] * f["serving_size"] for f in foods]

    ####################################################################################################
    # Problem definition
    ####################################################################################################

    # Create the 'prob' variable to contain the problem data
    prob = LpProblem("The food problem", LpMinimize)

    # A dictionary called 'prob_vars' is created to contain the referenced Variables
    prob_vars = LpVariable.dicts(
        name="food",
        indices=food_names,
        lowBound=MIN_GRAMS,
        upBound=max_grams,
        cat="Integer",
    )

    multipliers = LpVariable.dicts(
        "multiplier",
        indices=food_names,
        lowBound=0,
        upBound=None,
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

    for f in food_names:
        prob += (
            prob_vars[f] <= multipliers[f] * max_grams[food_names.index(f)],
            f"Maximum {f} grams",
        )

    # Solve
    prob.solve()

    result = parse_result(prob, foods)

    return result
