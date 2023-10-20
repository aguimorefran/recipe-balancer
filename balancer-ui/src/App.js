import React, { useState } from "react";
import FoodTable from "./FoodTable";
import SelectedFoodsTable from "./SelectedFoodsTable";

function App() {
  const [searchTerm, setSearchTerm] = useState('');
  const [foods, setFoods] = useState([]);
  const [selectedFoods, setSelectedFoods] = useState([]);
  const [maxFatPctg, setMaxFatPctg] = useState(0.25);
  const [minPrtoPctg, setMinPrtoPctg] = useState(0.4);
  const [protPenalty, setProtPenalty] = useState(1000);
  const [fatPenalty, setFatPenalty] = useState(1000);
  const [kcalsPenalty, setKcalsPenalty] = useState(100);
  const [maxKcals, setMaxKcals] = useState("");

  const handleSelectFood = (foodId) => {
    setSelectedFoods([...selectedFoods, foodId]);
  };

  const handleRemoveFood = (foodId) => {
    setSelectedFoods(selectedFoods.filter((id) => id !== foodId));
  };

  const handleSearch = () => {
    fetch(`http://127.0.0.1:8000/search_food?name=${searchTerm}`)
      .then(response => response.json())
      .then(data => {
        console.log(data);
        setFoods(data.foods);
      })
      .catch(error => console.error(error));
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Search for food"
        onChange={(event) => setSearchTerm(event.target.value)}
      />
      <button onClick={handleSearch}>Search</button>
      <FoodTable
        foods={foods}
        selectedFoods={selectedFoods}
        handleSelectFood={handleSelectFood}
        handleRemoveFood={handleRemoveFood}
      />      <SelectedFoodsTable selectedFoods={selectedFoods} onRemoveFood={handleRemoveFood} />
      <div>
        <label htmlFor="maxFatPctg">Max Fat Percentage:</label>
        <input
          type="range"
          id="maxFatPctg"
          name="maxFatPctg"
          min="0"
          max="1"
          step="0.05"
          value={maxFatPctg}
          onChange={(event) => setMaxFatPctg(event.target.value)}
        />
        <span>{parseInt(maxFatPctg * 100)}%</span>
        <br />
        <label htmlFor="minPrtoPctg">Min Protein Percentage:</label>
        <input
          type="range"
          id="minPrtoPctg"
          name="minPrtoPctg"
          min="0"
          max="1"
          step="0.05"
          value={minPrtoPctg}
          onChange={(event) => setMinPrtoPctg(event.target.value)}
        />
        <span>{parseInt(minPrtoPctg * 100)}%</span>
        <br />
        <label htmlFor="protPenalty">Protein Penalty:</label>
        <input
          type="range"
          id="protPenalty"
          name="protPenalty"
          min="0"
          max="2000"
          step="100"
          value={protPenalty}
          onChange={(event) => setProtPenalty(event.target.value)}
        />
        <span>{protPenalty}</span>
        <br />
        <label htmlFor="fatPenalty">Fat Penalty:</label>
        <input
          type="range"
          id="fatPenalty"
          name="fatPenalty"
          min="0"
          max="2000"
          step="100"
          value={fatPenalty}
          onChange={(event) => setFatPenalty(event.target.value)}
        />
        <span>{fatPenalty}</span>
        <br />
        <label htmlFor="kcalsPenalty">Kcals Penalty:</label>
        <input
          type="range"
          id="kcalsPenalty"
          name="kcalsPenalty"
          min="0"
          max="200"
          step="10"
          value={kcalsPenalty}
          onChange={(event) => setKcalsPenalty(event.target.value)}
        />
        <span>{kcalsPenalty}</span>
        <br />
        <label htmlFor="maxKcals">Max Kcals:</label>
        <input
          type="text"
          id="maxKcals"
          name="maxKcals"
          value={maxKcals}
          onChange={(event) => setMaxKcals(event.target.value)}
        />
        <br />

      </div>
    </div>
  );
};

export default App;