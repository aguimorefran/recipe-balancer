import sqlite3

from pulp import *


def print_rest(prob, kcals_objetive):
    print("=========================================")
    print("Status: {:>10}".format(LpStatus[prob.status]))
    if LpStatus[prob.status] == "Optimal":
        print("Objective kcals: {:>10.2f}".format(kcals_objetive) + " kcals")
        print("Target kcals: {:>13.2f}".format(value(prob.objective)) + " kcals")

        fat_kcals = 0
        prot_kcals = 0
        carb_kcals = 0

        food_vars = [(f, value(prob_vars[f])) for f in food_names]
        food_vars_sorted = sorted(food_vars, key=lambda x: x[1])

        for f, var_value in food_vars_sorted:
            fat_kcals += var_value * food_fats[food_names.index(f)] * KCALS_GRAM_FAT
            prot_kcals += (
                var_value * food_prots[food_names.index(f)] * KCALS_GRAM_PROTEIN
            )
            carb_kcals += var_value * food_carbs[food_names.index(f)] * KCALS_GRAM_CARBS

        total_kcals = fat_kcals + prot_kcals + carb_kcals
        print("Result kcals: {:>13.2f}".format(total_kcals) + " kcals")
        print("=========================================")
        print("Macros:")
        print("=========================================")
        print(
            "Result protein: {:>10.2f}".format(prot_kcals / KCALS_GRAM_PROTEIN) + " %"
        )
        print("Result fat: {:>14.2f}".format(fat_kcals / KCALS_GRAM_FAT) + " %")
        print("Result carbs: {:>12.2f}".format(carb_kcals / KCALS_GRAM_CARBS) + " %")
        print("=========================================")
        print("Foods:")
        print("=========================================")
        for f, var_value in food_vars_sorted:
            print("- {:>10.2f}".format(var_value) + " grams of " + f.replace("_", " "))
        print("=========================================")
        print("Slack variables:")
        print("=========================================")
        print("Protein: {:>10.2f}".format(value(slack_protein)))
        print("Fat: {:>14.2f}".format(value(slack_fat)))
        print("Kcals: {:>12.2f}".format(value(slack_kcals)))


def ask_calories():
    while True:
        try:
            calories = int(input("How many calories do you want to eat? "))
            break
        except ValueError:
            print("Please enter a number")
    return calories


def ask_prot_pct():
    while True:
        try:
            prot_pct = float(
                input("What percentage of protein do you want as minimum? ")
            )
            break
        except ValueError:
            print("Please enter a number")
    return prot_pct


def ask_fat_pct():
    while True:
        try:
            fat_pct = float(input("What percentage of fat do you want as maximum? "))
            break
        except ValueError:
            print("Please enter a number")
    return fat_pct


def ask_params(food_names):
    gram_multiplier = []
    max_grams = []
    for f in food_names:
        multiplier = input(f"How many grams of {f} do you want to eat? ")
        gram_multiplier.append(int(multiplier))
        max_gram = input(f"What is the maximum grams of {f} you can eat? ")
        max_grams.append(int(max_gram))
    return gram_multiplier, max_grams


####################################################################################################

KCALS_GRAM_FAT = 9
KCALS_GRAM_CARBS = 4
KCALS_GRAM_PROTEIN = 4

MIN_GRAMS = 5
MAX_GRAMS = 200


PENALTY_PROT = 100
PENALTY_FAT = 100
PENALTY_KCALS = 10


food_ids = [60, 62, 68, 77, 92]

conn = sqlite3.connect("food.db")
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
kcals_objetive = ask_calories()
prot_pct = ask_prot_pct()
fat_pct = ask_fat_pct()
gram_multiplier, max_grams = ask_params(food_names)

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

print_rest(prob, kcals_objetive)