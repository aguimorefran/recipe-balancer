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

  const handleMaxGramsChange = (foodId, maxServings) => {
    const updatedSelectedFoods = selectedFoods.map((food) => {
      if (food.id === foodId) {
        return { ...food, max_servings: parseInt(maxServings, 10) };
      }
      return food;
    });
    onUpdateSelectedFoods(updatedSelectedFoods);
  };

  const handleServingSizeChange = (foodId, servingSize) => {
    const updatedSelectedFoods = selectedFoods.map((food) => {
      if (food.id === foodId) {
        return { ...food, serving_size: parseInt(servingSize, 10) };
      }
      return food;
    });
    onUpdateSelectedFoods(updatedSelectedFoods);
  };

  return (
    <>
      {selectedFoods.length > 0 && (
        <div>
          <h2>Selected foods: {selectedFoods.length}</h2>
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Serving Size</th>
                <th>Max servings</th>
                <th>Remove</th>
              </tr>
            </thead>
            <tbody>
              {selectedFoods.map((food) => (
                <tr key={food.id}>
                  <td>{food.name}</td>
                  <td>
                    <input
                      className="textbox-4"
                      type="number"
                      value={food.serving_size}
                      onChange={(e) =>
                        handleServingSizeChange(food.id, e.target.value)
                      }
                    />
                  </td>
                  <td>
                    <input
                      className="textbox-4"
                      type="number"
                      value={food.max_servings}
                      onChange={(e) =>
                        handleMaxGramsChange(food.id, e.target.value)
                      }
                    />
                  </td>

                  <td>
                    <button
                      className="button-4 button-4-lightred"
                      onClick={() => onRemoveFood(food.id)}
                    >
                      Remove
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </>
  );
}

export default SelectedFoodsTable;
