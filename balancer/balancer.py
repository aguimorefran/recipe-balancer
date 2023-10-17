import sqlite3

from pulp import *

KCALS_GRAM_FAT = 9
KCALS_GRAM_CARBS = 4
KCALS_GRAM_PROTEIN = 4

MIN_GRAMS = 5
MAX_GRAMS = 200


def parse_result(prob):
    result = {}
    for v in prob.variables():
        if v.varValue > 0:
            result[v.name] = v.varValue
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
        cat="Continuous",
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

    # Solve
    prob.solve()

    result = parse_result(prob)

    return result
