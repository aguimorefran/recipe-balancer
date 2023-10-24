import React, { useState, useEffect } from "react";
import Results from "./Results";

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
    const response = await fetch("http://127.0.0.1:8000/solve_problem", {
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
      <button onClick={handleSolveClick}>Calculate</button>
      {solverResult && Object.keys(solverResult).length !== 0 && (
        <Results result_data={solverResult} />
      )}
    </div>
  );
}

export default Solver;
