import React, { useState } from "react";

function AddFoodPage() {
    const [url, setUrl] = useState("");
    const [category, setCategory] = useState("");
    const [subcategory, setSubcategory] = useState("");
    const [food, setFood] = useState(null);
    const [error, setError] = useState(null);

    const handleAddFood = () => {
        const encodedUrl = encodeURIComponent(url);
        const endpoint = `http://127.0.0.1:8000/harvest_url?url=${encodedUrl}&category=${category}&subcategory=${subcategory}`;

        fetch(endpoint)
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then((data) => {
                console.log(data);
                setFood(data.food);
                setError(null);
            })
            .catch((error) => {
                console.error(error);
                setFood(null);
                setError(error.response.data.error);
                console.log(error.response.data.error);
            });
    };

    return (
        <div>
            <h1>Add Food</h1>
            <div>
                <label htmlFor="url">URL:</label>
                <input
                    type="text"
                    id="url"
                    name="url"
                    value={url}
                    onChange={(event) => setUrl(event.target.value)}
                />
            </div>
            <div>
                <label htmlFor="category">Category:</label>
                <input
                    type="text"
                    id="category"
                    name="category"
                    value={category}
                    onChange={(event) => setCategory(event.target.value)}
                />
            </div>
            <div>
                <label htmlFor="subcategory">Subcategory:</label>
                <input
                    type="text"
                    id="subcategory"
                    name="subcategory"
                    value={subcategory}
                    onChange={(event) => setSubcategory(event.target.value)}
                />
            </div>
            <button onClick={handleAddFood}>Add food</button>
            {error && (
                <p style={{ color: "red" }}>
                    Error: {error}
                </p>
            )}
            {food && (
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Brand</th>
                            <th>Category</th>
                            <th>Subcategory</th>
                            <th>Calories</th>
                            <th>Protein</th>
                            <th>Fat</th>
                            <th>Carbs</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>{food.name}</td>
                            <td>{food.brand}</td>
                            <td>{food.category}</td>
                            <td>{food.subcategory}</td>
                            <td>{food.calories}</td>
                            <td>{food.protein}</td>
                            <td>{food.fat}</td>
                            <td>{food.carbs}</td>
                        </tr>
                    </tbody>
                </table>
            )}
        </div>
    );
}

export default AddFoodPage;