import React, { useState } from "react";
import "./styles.css";
import config from "./config.js";
import { Tab, Tabs, TabList, TabPanel } from "react-tabs";
import "react-tabs/style/react-tabs.css";

function AddFoodPage() {
  const [url, setUrl] = useState("");
  const [category, setCategory] = useState("");
  const [subcategory, setSubcategory] = useState("");
  const [food, setFood] = useState(null);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [name, setName] = useState("");
  const [brand, setBrand] = useState("");
  const [calories, setCalories] = useState(0);
  const [fat, setFat] = useState(0);
  const [carb, setCarb] = useState(0);
  const [protein, setProtein] = useState(0);
  const [servingSize, setServingSize] = useState(0);
  const [insertResult, setInsertResult] = useState(null);
  const [message, setMessage] = useState(null);
  const [isSuccess, setIsSuccess] = useState(false);

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

  const handleInsertFoodManual = () => {
    const req_url = config.getRequestUrl();
    const endpoint = `${req_url}/insert_food_manual`;

    const data = {
      name: name,
      brand: brand,
      category: category,
      subcategory: subcategory,
      item_url: url,
      cals_per_g: calories,
      fat_per_g: fat,
      carb_per_g: carb,
      prot_per_g: protein,
      serving_size: servingSize,
      times_selected: 0,
    };

    fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.result) {
          setMessage("Food inserted correctly");
          setIsSuccess(true);
        } else {
          setMessage(data.error);
          setIsSuccess(false);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        setMessage("An error occurred");
        setIsSuccess(false);
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
      <Tabs>
        <TabList>
          <Tab>Fatsecret Entry</Tab>
          <Tab>Manual Entry</Tab>
        </TabList>

        <TabPanel>
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
            <button
              className="button-4-darkgreen button-4"
              onClick={handleAddFood}
            >
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
        </TabPanel>
        <TabPanel>
          <div style={{ display: "flex", flexDirection: "row" }}>
            <div style={{ minWidth: "200px" }}>
              <label htmlFor="name">Name:</label>
              <br />
              <label htmlFor="brand">Brand:</label>
              <br />
              <label htmlFor="category">Category:</label>
              <br />
              <label htmlFor="subcategory">Subcategory:</label>
              <br />
              <label htmlFor="calories">Kcals/100g:</label>
              <br />
              <label htmlFor="protein">Protein/100g:</label>
              <br />
              <label htmlFor="carb">Carbs/100g:</label>
              <br />
              <label htmlFor="fat">Fat/100g:</label>
              <br />
              <label htmlFor="servingSize">Serving Size:</label>
              <br />
            </div>
            <div style={{ flex: 1 }}>
              <input
                type="text"
                id="name"
                name="name"
                value={name}
                onChange={(event) => setName(event.target.value)}
                className="textbox-4"
                placeholder="Canned tomato"
              />
              <br />
              <input
                type="text"
                id="brand"
                name="brand"
                value={brand}
                onChange={(event) => setBrand(event.target.value)}
                className="textbox-4"
                placeholder="Heinz"
              />
              <br />
              <input
                type="text"
                id="category"
                name="category"
                value={category}
                onChange={(event) => setCategory(event.target.value)}
                className="textbox-4"
                placeholder="Canned Goods"
              />
              <br />
              <input
                type="text"
                id="subcategory"
                name="subcategory"
                value={subcategory}
                onChange={(event) => setSubcategory(event.target.value)}
                className="textbox-4"
                placeholder="Tomatoes"
              />
              <br />
              <input
                type="text"
                id="calories"
                name="calories"
                value={calories}
                onChange={(event) => setCalories(event.target.value)}
                className="textbox-4"
              />
              <br />
              <input
                type="text"
                id="protein"
                name="protein"
                value={protein}
                onChange={(event) => setProtein(event.target.value)}
                className="textbox-4"
              />
              <br />
              <input
                type="text"
                id="carb"
                name="carb"
                value={carb}
                onChange={(event) => setCarb(event.target.value)}
                className="textbox-4"
              />
              <br />
              <input
                type="text"
                id="fat"
                name="fat"
                value={fat}
                onChange={(event) => setFat(event.target.value)}
                className="textbox-4"
              />
              <br />
              <input
                type="text"
                id="servingSize"
                name="servingSize"
                value={servingSize}
                onChange={(event) => setServingSize(event.target.value)}
                className="textbox-4"
              />
              <br />
            </div>
          </div>
          <button
            className="button-4-darkgreen button-4"
            onClick={handleInsertFoodManual}
          >
            Add Food
          </button>
          {message && (
            <div
              style={{
                backgroundColor: isSuccess ? "green" : "red",
                color: "white",
              }}
            >
              {message}
            </div>
          )}
        </TabPanel>
      </Tabs>
    </div>
  );
}

export default AddFoodPage;
