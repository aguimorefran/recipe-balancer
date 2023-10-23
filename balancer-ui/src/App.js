import React, { useState } from "react";
import FoodTable from "./FoodTable";
import SelectedFoodsTable from "./SelectedFoodsTable";
import AddFoodPage from "./AddFoodPage";
import Solver from "./Solver";
import PieChart from "./Piechart";
import Sliders from "./Sliders";

function App() {
  const [searchTerm, setSearchTerm] = useState("");
  const [foods, setFoods] = useState([]);
  const [selectedFoods, setSelectedFoods] = useState([]);
  const [maxFatPctg, setMaxFatPctg] = useState(0.25);
  const [minPrtoPctg, setMinPrtoPctg] = useState(0.4);
  const [protPenalty, setProtPenalty] = useState(1000);
  const [fatPenalty, setFatPenalty] = useState(1000);
  const [kcalsPenalty, setKcalsPenalty] = useState(100);
  const [maxKcals, setMaxKcals] = useState("500");
  const [showAddFoodPage, setShowAddFoodPage] = useState(false);
  const [addFoodButtonText, setAddFoodButtonText] = useState("Add food");

  const handleSelectFood = (food) => {
    console.log("Inserting food into selectedFoods: ", food);
    if (!selectedFoods.map((food) => food.id).includes(food.id)) {
      setSelectedFoods([
        ...selectedFoods,
        { ...food, max_grams: 0, serving_size: 0 },
      ]);
    }
  };

  const handleRemoveFood = (foodId) => {
    setSelectedFoods(selectedFoods.filter((food) => food.id !== foodId));
  };

  const handleSearch = () => {
    fetch(`http://127.0.0.1:8000/search_food?name=${searchTerm}`)
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        setFoods(data.foods);
      })
      .catch((error) => console.error(error));
  };

  const handleAddFoodClick = () => {
    setShowAddFoodPage(!showAddFoodPage);
    setAddFoodButtonText(showAddFoodPage ? "Add food" : "Hide");
  };

  const handleUpdateSelectedFoods = (updatedSelectedFoods) => {
    setSelectedFoods(updatedSelectedFoods);
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Search for food"
        onChange={(event) => setSearchTerm(event.target.value)}
      />
      <button onClick={handleSearch}>Search</button>
      <button onClick={handleAddFoodClick}>{addFoodButtonText}</button>{" "}
      {showAddFoodPage && <AddFoodPage />}
      <FoodTable
        foods={foods}
        selectedFoods={selectedFoods}
        handleSelectFood={handleSelectFood}
        handleRemoveFood={handleRemoveFood}
      />
      <SelectedFoodsTable
        selectedFoods={selectedFoods}
        onRemoveFood={handleRemoveFood}
        onUpdateSelectedFoods={handleUpdateSelectedFoods}
      />
      <div>
        <div style={{ display: "flex", alignItems: "center" }}>
          <div style={{ flex: 1 }}>
            <Sliders
              minPrtoPctg={minPrtoPctg}
              maxFatPctg={maxFatPctg}
              protPenalty={protPenalty}
              fatPenalty={fatPenalty}
              kcalsPenalty={kcalsPenalty}
              setMinPrtoPctg={setMinPrtoPctg}
              setMaxFatPctg={setMaxFatPctg}
              setProtPenalty={setProtPenalty}
              setFatPenalty={setFatPenalty}
              setKcalsPenalty={setKcalsPenalty}
            />
          </div>
          <div style={{ flex: 1 }}>
            <PieChart
              data={{
                title: "Target macros",
                labels: ["Carbs", "Protein", "Fat"],
                values: [1 - maxFatPctg - minPrtoPctg, minPrtoPctg, maxFatPctg],
                colors: ["#E7ECEF", "#63B3ED", "#F6AD55"],
              }}
            />
          </div>
        </div>
      </div>
      <div>
        <Solver
          selectedFoods={selectedFoods}
          maxKcals={maxKcals}
          maxFatPctg={maxFatPctg}
          minPrtoPctg={minPrtoPctg}
          protPenalty={protPenalty}
          fatPenalty={fatPenalty}
          kcalsPenalty={kcalsPenalty}
          onUpdateSelectedFoods={handleUpdateSelectedFoods}
        />
      </div>
    </div>
  );
}

export default App;
