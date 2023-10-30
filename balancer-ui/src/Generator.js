import React, { useState, useEffect } from "react";
import config from "./config.js";

function Generator({ solverResult }) {
  const handleGenerateClick = async () => {
    const requestBody = {
      foods: solverResult.result.food_results,
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
    console.log(data);
  };

  return (
    <div>
      <h1>Course generator</h1>
      <button className="button-4" onClick={handleGenerateClick}>
        Generate
      </button>
    </div>
  );
}
export default Generator;
