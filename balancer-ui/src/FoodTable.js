import React from "react";

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
    <div>
      <h1>Search results</h1>
      <table>
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
            <th>Select</th>
          </tr>
        </thead>
        <tbody>
          {foods.slice(0, 20).map((food) => (
            <tr key={food.id}>
              <td>{food.id}</td>
              <td>{food.name}</td>
              <td>{food.category}</td>
              <td>{food.subcategory}</td>
              <td>{food.brand}</td>
              <td>
                <button onClick={() => handleOpenUrl(food.item_url)}>
                  {"Open URL"}
                </button>
              </td>
              <td>{food.cals_per_g.toFixed(2)}</td>
              <td>{food.fat_per_g.toFixed(2)}</td>
              <td>{food.carb_per_g.toFixed(2)}</td>
              <td>{food.prot_per_g.toFixed(2)}</td>
              <td>
                <button
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
