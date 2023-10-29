import React, { useState } from "react";
import "./styles.css";
import config from "./config.js";

const Recommendator = ({ foodResults }) => {
  const [response, setResponse] = useState("");
  const [mode, setMode] = useState("snack"); // default mode is "snack"

  const handleClick = async () => {
    const foods = JSON.stringify(foodResults);
    console.log(foods);
    const req_url = config.getRequestUrl();
    const url = `${req_url}/generate_recipe?mode=${mode}`;
    const requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        accept: "application/json",
      },
      body: JSON.stringify({ foods }),
    };
    const response = await fetch(url, requestOptions);
    const data = await response.json();
    setResponse(JSON.stringify(data, null, 2));
  };

  const handleModeChange = (event) => {
    setMode(event.target.value);
  };

  return (
    <div>
      <h1>Recommendator</h1>
      {/* dropdown for "snack", "breakfast", "lunch", "dinner", "dessert", "entire day" */}
      <h2>Mode</h2>
      <select value={mode} onChange={handleModeChange}>
        <option value="snack">Snack</option>
        <option value="breakfast">Breakfast</option>
        <option value="lunch">Lunch</option>
        <option value="dinner">Dinner</option>
        <option value="dessert">Dessert</option>
        <option value="entire day">Entire day</option>
      </select>

      <button onClick={handleClick}>Generate Recipe</button>
      <pre>{response}</pre>
    </div>
  );
};

export default Recommendator;
