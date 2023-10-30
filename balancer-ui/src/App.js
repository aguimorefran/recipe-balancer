import React, { useState } from "react";
import FoodTable from "./FoodTable";
import SelectedFoodsTable from "./SelectedFoodsTable";
import AddFoodPage from "./AddFoodPage";
import Solver from "./Solver";
import PieChart from "./Piechart";
import Sliders from "./Sliders";
import "./styles.css";
import config from "./config.js";

function App() {
  const [searchTerm, setSearchTerm] = useState("");
  const [foods, setFoods] = useState([]);
  const [selectedFoods, setSelectedFoods] = useState([]);
  const [maxFatPctg, setMaxFatPctg] = useState(0.25);
  const [minPrtoPctg, setMinPrtoPctg] = useState(0.4);
  const [protPenalty, setProtPenalty] = useState(2500);
  const [fatPenalty, setFatPenalty] = useState(2500);
  const [kcalsPenalty, setKcalsPenalty] = useState(2500);
  const [maxKcals, setMaxKcals] = useState(500);
  const [showAddFoodPage, setShowAddFoodPage] = useState(false);
  const [addFoodButtonText, setAddFoodButtonText] = useState("Add food");

  const handleSelectFood = (food) => {
    const req_url = config.getRequestUrl();
    console.log("Inserting food into selectedFoods: ", food);
    if (!selectedFoods.map((food) => food.id).includes(food.id)) {
      setSelectedFoods([
        ...selectedFoods,
        { ...food, max_servings: 0, serving_size: 0 },
      ]);
      fetch(`${req_url}/inc_selection?food_id=${food.id}`, {
        method: "GET",
        headers: {
          Accept: "application/json",
        },
      })
        .then((response) => response.json())
        .then((data) => console.log(data))
        .catch((error) => console.error(error));
    }
  };

  const handleRemoveFood = (foodId) => {
    setSelectedFoods(selectedFoods.filter((food) => food.id !== foodId));
  };

  const handleSearch = () => {
    const req_url = config.getRequestUrl();
    fetch(`${req_url}/search_food?name=${searchTerm}`)
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
      <div style={{ display: "flex", alignItems: "center" }}>
        <img src={require("./logo.png")} width="100" height="100" />
        <div style={{ marginLeft: "10px", fontSize: "30px" }}>
          Recipe Balancer
        </div>
      </div>
      <input
        type="text"
        className="textbox-4 textbox-4-main"
        placeholder="Search for food"
        onChange={(event) => setSearchTerm(event.target.value)}
        onKeyPress={(event) => {
          if (event.key === "Enter") {
            handleSearch();
          }
        }}
      />
      <button className="button-4" onClick={handleSearch}>
        Search
      </button>
      <button className="button-4" onClick={handleAddFoodClick}>
        {addFoodButtonText}
      </button>{" "}
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
      <div
        style={{
          border: "1px solid #444",
          borderRadius: "10px",
          padding: "20px",
          margin: "20px",
          backgroundColor: "#eee",
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "left",
          }}
        >
          <h1 style={{ margin: "0" }}>Target macros</h1>
        </div>
        <div style={{ display: "flex" }}>
          <div style={{ flex: 1, display: "flex", alignItems: "center" }}>
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
              maxKcals={maxKcals}
              setMaxKcals={setMaxKcals}
            />
          </div>
          <div style={{ flex: 1 }}>
            <PieChart
              data={{
                title: "Target macros",
                labels: ["Carbs", "Protein", "Fat"],
                values: [1 - maxFatPctg - minPrtoPctg, minPrtoPctg, maxFatPctg],
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
