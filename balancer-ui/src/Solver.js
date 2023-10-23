import React, { useState, useEffect } from "react";

function Solver({
  selectedFoods,
  maxKcals,
  maxFatPctg,
  minPrtoPctg,
  protPenalty,
  fatPenalty,
  onUpdateSelectedFoods,
}) {
  return (
    <div>
      <h1>Solver</h1>
      <p>Max Kcals: {maxKcals}</p>
      <p>Max Fat Percentage: {maxFatPctg}</p>
      <p>Min Protein Percentage: {minPrtoPctg}</p>
      <p>Protein Penalty: {protPenalty}</p>
      <p>Fat Penalty: {fatPenalty}</p>

      {selectedFoods.length === 0 ? (
        <div style={{ backgroundColor: "orange", padding: "10px" }}>
          At least one food is needed
        </div>
      ) : (
        <div>
          <p>Selected Foods:</p>
          <ul>
            {selectedFoods.map((food) => (
              <li key={food.id}>{food.name}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default Solver;
