import React, { useState, useEffect } from "react";

function SelectedFoodsTable({
  selectedFoods,
  onRemoveFood,
  onUpdateSelectedFoods,
}) {
  const [foodsData, setFoodsData] = useState([]);
  useEffect(() => {
    const fetchData = async () => {
      const foods = selectedFoods.map((food) => food);
      setFoodsData(foods);
    };
    fetchData();
  }, [selectedFoods]);

  const handleMaxGramsChange = (foodId, maxGrams) => {
    const updatedSelectedFoods = selectedFoods.map((food) => {
      if (food.id === foodId) {
        return { ...food, max_grams: maxGrams };
      }
      return food;
    });
    onUpdateSelectedFoods(updatedSelectedFoods);
  };

  const handleServingSizeChange = (foodId, servingSize) => {
    const updatedSelectedFoods = selectedFoods.map((food) => {
      if (food.id === foodId) {
        return { ...food, serving_size: servingSize };
      }
      return food;
    });
    onUpdateSelectedFoods(updatedSelectedFoods);
  };

  return (
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Max Grams</th>
          <th>Serving Size</th>
          <th>Remove</th>
        </tr>
      </thead>
      <tbody>
        {selectedFoods.map((food) => (
          <tr key={food.id}>
            <td>{food.name}</td>
            <td>
              <input
                type="number"
                value={food.max_grams}
                onChange={(e) => handleMaxGramsChange(food.id, e.target.value)}
              />
            </td>
            <td>
              <input
                type="number"
                value={food.serving_size}
                onChange={(e) =>
                  handleServingSizeChange(food.id, e.target.value)
                }
              />
            </td>
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
