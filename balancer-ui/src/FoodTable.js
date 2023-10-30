import React from "react";
import "./styles.css";

const FoodTable = ({
  foods,
  selectedFoods,
  handleSelectFood,
  handleRemoveFood,
}) => {
  const handleOpenUrl = (url) => {
    window.open(url, "_blank");
  };

  return (
    <div
      style={{
        border: "1px solid #444",
        borderRadius: "10px",
        padding: "20px",
        margin: "20px",
        backgroundColor: "#eee",
      }}
    >
      <table className="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Category</th>
            <th>Subcategory</th>
            <th>Brand</th>
            <th>Item URL</th>
            <th>Kcals/g</th>
            <th>Fat/g</th>
            <th>Carbs/g</th>
            <th>Protein/g</th>
            <th>Times selected</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {foods.slice(0, 20).map((food) => (
            <tr key={food.id}>
              <td>{food.id}</td>
              <td>{food.name}</td>
              <td>{food.category}</td>
              <td>{food.subcategory}</td>
              <td>{food.brand === "Ver Más" ? "No brand" : food.brand}</td>
              <td>
                <button
                  className="button-4"
                  onClick={() => handleOpenUrl(food.item_url)}
                >
                  {"Open URL"}
                </button>
              </td>
              <td>{food.cals_per_g.toFixed(2)}</td>
              <td>{food.fat_per_g.toFixed(2)}</td>
              <td>{food.carb_per_g.toFixed(2)}</td>
              <td>{food.prot_per_g.toFixed(2)}</td>
              <td>{food.times_selected}</td>
              <td>
                <button
                  className={
                    selectedFoods.some(
                      (selectedFood) => selectedFood.id === food.id
                    )
                      ? "button-4 button-4-lightred" // use light red color if food is selected
                      : "button-4 button-4-lightgreen" // use light green color if food is not selected
                  }
                  onClick={() =>
                    selectedFoods.some(
                      (selectedFood) => selectedFood.id === food.id
                    )
                      ? handleRemoveFood(food.id)
                      : handleSelectFood(food)
                  }
                >
                  {selectedFoods.some(
                    (selectedFood) => selectedFood.id === food.id
                  )
                    ? "Remove"
                    : "Select"}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default FoodTable;
