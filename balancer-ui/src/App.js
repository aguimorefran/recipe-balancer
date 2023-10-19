import React, { useState } from "react";
import FoodTable from "./FoodTable";
import SelectedFoodsTable from "./SelectedFoodsTable";

function App() {
  const [searchTerm, setSearchTerm] = useState('');
  const [foods, setFoods] = useState([]);
  const [selectedFoods, setSelectedFoods] = useState([]);

  const handleSelectFood = (foodId) => {
    console.log(foodId)
    if (selectedFoods.includes(foodId)) {
      setSelectedFoods(selectedFoods.filter((id) => id !== foodId));
    } else {
      setSelectedFoods([...selectedFoods, foodId]);
    }


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

  const handleOpenUrl = (url) => {
    window.open(url, "_blank");
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Search for food"
        onChange={(event) => setSearchTerm(event.target.value)}
      />
      <button onClick={handleSearch}>Search</button>
      <FoodTable foods={foods} handleOpenUrl={handleOpenUrl} selectedFoods={selectedFoods} handleSelectFood={handleSelectFood} />
      <SelectedFoodsTable selectedFoods={selectedFoods} onRemoveFood={handleRemoveFood} />
    </div>
  );
};

export default App;