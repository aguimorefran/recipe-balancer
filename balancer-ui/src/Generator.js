import React, { useState } from "react";
import config from "./config.js";

function Generator({ solverResult }) {
  const [selectedOption, setSelectedOption] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [recipe, setRecipe] = useState("");
  const [parsedRecipe, setParsedRecipe] = useState(null);

  const handleOptionChange = (event) => {
    setSelectedOption(event.target.value);
  };

  const handleGenerateClick = async () => {
    setIsLoading(true);
    const requestBody = {
      foods: solverResult.result.food_results,
      course: selectedOption,
    };
    const req_url = config.getRequestUrl();
    const response = await fetch(`${req_url}/generate_recipe`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestBody),
    });

    const data = await response.json();
    if (data.result) {
      setRecipe(data.result);
      setParsedRecipe(JSON.parse(data.result));
    }
    setIsLoading(false);
  };

  const options = ["Breakfast", "Dinner", "Lunch", "Snack", "Entire day"];

  return (
    <div
      style={{
        border: "1px solid #444",
        borderRadius: "10px",
        borderColor: "#7a00a8",
        boxShadow: "0 0 10px #7a00a8",
        padding: "20px",
        margin: "20px",
        backgroundColor: "#f0c9ff",
      }}
    >
      <h1>Course recommendator</h1>
      <p>
        Using GPT-3.5, generate a meal / meal-plan for the selected course or
        the entire day.
      </p>
      <select
        value={selectedOption}
        onChange={handleOptionChange}
        className="button-4"
      >
        <option value="">Select an option</option>
        {options.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
      <button
        className="button-4-purple button-4"
        onClick={handleGenerateClick}
      >
        Generate
      </button>
      {isLoading && <p>Loading...</p>}
      {parsedRecipe && parsedRecipe.meal_plans ? (
        <div style={{ display: "flex" }}>
          {parsedRecipe.meal_plans.map((mealPlan, index) => (
            <div
              key={mealPlan.name}
              style={{
                flex: 1,
                margin: "0 10px",
                borderRight:
                  index !== parsedRecipe.meal_plans.length - 1 &&
                  "1px solid black",
              }}
            >
              <h2>{mealPlan.name}</h2>
              <p>
                <strong>Breakfast:</strong> {mealPlan.breakfast}
              </p>
              <p>
                <strong>Lunch:</strong> {mealPlan.lunch}
              </p>
              <p>
                <strong>Dinner:</strong> {mealPlan.dinner}
              </p>
              <p>
                <strong>Snack:</strong> {mealPlan.snack}
              </p>
            </div>
          ))}
        </div>
      ) : parsedRecipe && parsedRecipe.recipes ? (
        <div style={{ display: "flex" }}>
          {parsedRecipe.recipes.map((recipe, index) => (
            <div
              key={recipe.name}
              style={{
                flex: 1,
                margin: "0 10px",
                borderRight:
                  index !== parsedRecipe.recipes.length - 1 &&
                  "1px solid black",
              }}
            >
              <h2>{recipe.name}</h2>
              <p
                dangerouslySetInnerHTML={{
                  __html: recipe.preparation.replace(/\n/g, "<br>"),
                }}
              ></p>
            </div>
          ))}
        </div>
      ) : null}
    </div>
  );
}

export default Generator;
