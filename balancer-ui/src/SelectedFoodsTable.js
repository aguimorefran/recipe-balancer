import React, { useState, useEffect } from "react";

function SelectedFoodsTable({ selectedFoods, onRemoveFood }) {
    const [foodsData, setFoodsData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            const promises = selectedFoods.map((foodId) =>
                fetch(`http://127.0.0.1:8000/food?food_id=${foodId}`, {
                    headers: {
                        accept: "application/json",
                    },
                }).then((response) => response.json())
            );
            const foods = await Promise.all(promises);
            setFoodsData(foods.map((food) => food.results[0]));
        };
        fetchData();
    }, [selectedFoods]);

    return (
        <div>
            <h2>Selected Foods</h2>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Brand</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {foodsData.map((food, index) => (
                        <tr key={selectedFoods[index]}>
                            <td>{selectedFoods[index]}</td>
                            <td>{food.name}</td>
                            <td>{food.brand}</td>
                            <td>
                                <button
                                    style={{
                                        backgroundColor: "red",
                                        color: "white",
                                        fontWeight: "bold",
                                    }}
                                    onClick={() =>
                                        onRemoveFood(selectedFoods[index])
                                    }
                                >
                                    Remove
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default SelectedFoodsTable;