import React, { useState, useEffect } from "react";

function SelectedFoodsTable({ selectedFoods, onRemoveFood }) {
  const [foodsData, setFoodsData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const foods = selectedFoods.map((food) => food);
      setFoodsData(foods);
    };
    fetchData();
  }, [selectedFoods]);

  return (
    <table>
      <thead>
        <tr>
          <th>Brand</th>
          <th>Name</th>
          <th>Cat</th>
          <th>Subcat</th>
          <th>Kcals/g</th>
          <th>Carbs/g</th>
          <th>Fat/g</th>
          <th>Prot/g</th>
          <th>Remove</th>
        </tr>
      </thead>
      <tbody>
        {foodsData.map((food) => (
          <tr key={food.id}>
            <td>{food.brand}</td>
            <td>{food.name}</td>
            <td>{food.category}</td>
            <td>{food.subcategory}</td>
            <td>{food.cals_per_g}</td>
            <td>{food.carb_per_g}</td>
            <td>{food.fat_per_g}</td>
            <td>{food.prot_per_g}</td>
            <td>
              <button onClick={() => onRemoveFood(food.id)}>Remove</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default SelectedFoodsTable;
