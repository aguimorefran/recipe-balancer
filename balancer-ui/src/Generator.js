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

  const options = ["breakfast", "dinner", "lunch", "snack", "entire day"];

  return (
    <div>
      <h1>Course recommendator</h1>
      <select value={selectedOption} onChange={handleOptionChange}>
        <option value="">Select an option</option>
        {options.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
      <button className="button-4" onClick={handleGenerateClick}>
        Generate
      </button>
      {isLoading && <p>Loading...</p>}
      {parsedRecipe && (
        <div style={{ display: "flex" }}>
          <div style={{ flex: 1 }}>
            <h2>{parsedRecipe.recipes[0].name}</h2>
            <p>{parsedRecipe.recipes[0].preparation}</p>
          </div>
          <div style={{ flex: 1 }}>
            <h2>{parsedRecipe.recipes[1].name}</h2>
            <p>{parsedRecipe.recipes[1].preparation}</p>
          </div>
          <div style={{ flex: 1 }}>
            <h2>{parsedRecipe.recipes[2].name}</h2>
            <p>{parsedRecipe.recipes[2].preparation}</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default Generator;
