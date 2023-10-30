import React, { useState } from "react";
import "./styles.css";
import config from "./config.js";

function AddFoodPage() {
  const [url, setUrl] = useState("");
  const [category, setCategory] = useState("");
  const [subcategory, setSubcategory] = useState("");
  const [food, setFood] = useState(null);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleAddFood = () => {
    const encodedUrl = encodeURIComponent(url);
    const req_url = config.getRequestUrl();
    const endpoint = `${req_url}/harvest_url?url=${encodedUrl}&category=${category}&subcategory=${subcategory}`;

    fetch(endpoint)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        console.log(data);
        if (data.error) {
          setFood(null);
          setError(data.error);
          setSuccess(false);
        } else {
          setFood(data.result);
          setError(null);
          setSuccess(true);
        }
      })
      .catch((error) => {
        console.error(error);
        setFood(null);
        setError(error.message || "An unknown error occurred");
        setSuccess(false);
      });
  };

  return (
    <div
      style={{
        border: "1px solid #444",
        borderRadius: "10px",
        padding: "20px",
        margin: "20px",
        backgroundColor: "#d3ffbf",
        boxShadow: "0 0 10px #1a5200",
      }}
    >
      <h2>Add Food</h2>

      <div>
        <div style={{ display: "flex", flexDirection: "row" }}>
          <div style={{ minWidth: "200px" }}>
            <label htmlFor="url">URL:</label>
            <br />
            <label htmlFor="category">Category:</label>
            <br />
            <label htmlFor="subcategory">Subcategory:</label>
          </div>
          <div style={{ flex: 1 }}>
            {" "}
            <input
              type="text"
              id="url"
              name="url"
              value={url}
              onChange={(event) => setUrl(event.target.value)}
              className="textbox-4"
            />
            <br />
            <input
              type="text"
              id="category"
              name="category"
              className="textbox-4"
              value={category}
              onChange={(event) => setCategory(event.target.value)}
            />
            <br />
            <input
              type="text"
              id="subcategory"
              name="subcategory"
              value={subcategory}
              className="textbox-4"
              onChange={(event) => setSubcategory(event.target.value)}
            />
          </div>
        </div>
        <button className="button-4-darkgreen button-4" onClick={handleAddFood}>
          Add Food
        </button>
        {error !== null && (
          <div
            style={{
              backgroundColor: "red",
              color: "white",
              padding: "10px",
              marginTop: "10px",
            }}
          >
            {error}
          </div>
        )}
        {success && (
          <div
            style={{
              backgroundColor: "green",
              color: "white",
              padding: "10px",
              marginTop: "10px",
            }}
          >
            OK
          </div>
        )}
        {food !== null && (
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Category</th>
                <th>Subcategory</th>
                <th>Brand</th>
                <th>Kcals/g</th>
                <th>Fat/g</th>
                <th>Carbs/g</th>
                <th>Prot/g</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>{food.name}</td>
                <td>{food.category}</td>
                <td>{food.subcategory}</td>
                <td>{food.brand}</td>
                <td>{food.cals_per_g.toFixed(2)}</td>
                <td>{food.fat_per_g.toFixed(2)}</td>
                <td>{food.carb_per_g.toFixed(2)}</td>
                <td>{food.prot_per_g.toFixed(2)}</td>
              </tr>
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default AddFoodPage;
