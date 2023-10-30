import React, { useState, useEffect } from "react";
import Results from "./Results";
import config from "./config.js";
import Generator from "./Generator";

function Solver({
  selectedFoods,
  maxKcals,
  maxFatPctg,
  minPrtoPctg,
  protPenalty,
  fatPenalty,
  kcalsPenalty,
  onUpdateSelectedFoods,
}) {
  const [solverResult, setSolverResult] = useState({});

  const handleSolveClick = async () => {
    const requestBody = {
      target_kcals: parseInt(maxKcals),
      max_fat_pct: parseFloat(maxFatPctg),
      min_prot_pct: parseFloat(minPrtoPctg),
      penalty_protein: parseInt(protPenalty),
      penalty_fat: parseInt(fatPenalty),
      penalty_kcals: parseInt(kcalsPenalty),
      foods: selectedFoods,
    };
    console.log(requestBody);
    const req_url = config.getRequestUrl();
    const response = await fetch(`${req_url}/solve_problem`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestBody),
    });

    const data = await response.json();
    setSolverResult(data);
  };

  return (
    <div>
      <h1>Results</h1>
      <button className="button-4" onClick={handleSolveClick}>
        Calculate
      </button>
      {solverResult && Object.keys(solverResult).length !== 0 && (
        <div>
          <Results result_data={solverResult} />
          <Generator solverResult={solverResult} />
        </div>
      )}
    </div>
  );
}

export default Solver;
