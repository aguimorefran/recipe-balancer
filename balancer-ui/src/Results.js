import React, { useState, useEffect } from "react";
import PieChart from "./Piechart";
import html2canvas from "html2canvas";
import Recommendator from "./Recommendator";

function Results({ result_data }) {
  const [foodResults, setFoodResults] = useState([]);

  useEffect(() => {
    console.log("Showing data");
    console.log(result_data);
    if (result_data.result) {
      setFoodResults(result_data.result.food_results);
    }
  }, [result_data]);

  const total = foodResults.reduce(
    (acc, curr) => {
      acc.cals += curr.cals;
      acc.fat_grams += curr.fat_grams;
      acc.carb_grams += curr.carb_grams;
      acc.protein_grams += curr.protein_grams;
      acc.fat_kcals += curr.fat_kcals;
      acc.carb_kcals += curr.carb_kcals;
      acc.protein_kcals += curr.protein_kcals;
      acc.grams += curr.grams;
      return acc;
    },
    {
      cals: 0,
      fat_grams: 0,
      carb_grams: 0,
      protein_grams: 0,
      fat_kcals: 0,
      carb_kcals: 0,
      protein_kcals: 0,
      grams: 0,
    }
  );

  if (foodResults.length === 0) {
    return (
      <div style={{ backgroundColor: "orange", padding: "10px" }}>
        No result
      </div>
    );
  }

  const { fat_kcal_pctg, carb_kcal_pctg, protein_kcal_pctg } =
    result_data.result;

  const handleSaveImage = () => {
    const tableContainer = document.querySelector(".table-container");
    html2canvas(tableContainer).then((canvas) => {
      const link = document.createElement("a");
      link.download = "table.png";
      link.href = canvas.toDataURL();
      link.click();
    });
  };

  return (
    <div>
      <div style={{ display: "flex", alignItems: "center" }}>
        <div style={{ flex: 1 }} className="table-container">
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Grams</th>
                <th>Cals</th>
                <th>Fat (g)</th>
                <th>Carbs (g)</th>
                <th>Protein (g)</th>
                <th>Fat (kcals)</th>
                <th>Carbs (kcals)</th>
                <th>Protein (kcals)</th>
              </tr>
            </thead>
            <tbody>
              {foodResults.map((food) => (
                <tr key={food.name}>
                  <td>{food.name}</td>
                  <td>{food.grams.toFixed(2)}</td>
                  <td>{food.cals.toFixed(2)}</td>
                  <td>{food.fat_grams.toFixed(2)}</td>
                  <td>{food.carb_grams.toFixed(2)}</td>
                  <td>{food.protein_grams.toFixed(2)}</td>
                  <td>{food.fat_kcals.toFixed(2)}</td>
                  <td>{food.carb_kcals.toFixed(2)}</td>
                  <td>{food.protein_kcals.toFixed(2)}</td>
                </tr>
              ))}
              <tr className="total-row">
                <td>Total</td>
                <td>{total.grams.toFixed(2)}</td>
                <td>{total.cals.toFixed(2)}</td>
                <td>{total.fat_grams.toFixed(2)}</td>
                <td>{total.carb_grams.toFixed(2)}</td>
                <td>{total.protein_grams.toFixed(2)}</td>
                <td>{total.fat_kcals.toFixed(2)}</td>
                <td>{total.carb_kcals.toFixed(2)}</td>
                <td>{total.protein_kcals.toFixed(2)}</td>
              </tr>
              <tr>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td>{(fat_kcal_pctg * 100).toFixed(2)}%</td>
                <td>{(carb_kcal_pctg * 100).toFixed(2)}%</td>
                <td>{(protein_kcal_pctg * 100).toFixed(2)}%</td>
              </tr>
            </tbody>
          </table>
          <button className="button-4" onClick={handleSaveImage}>
            Save as image
          </button>
        </div>
        <div style={{ flex: 1 }}>
          <PieChart
            data={{
              title: "Result macros",
              labels: ["Carbs", "Protein", "Fat"],
              values: [carb_kcal_pctg, protein_kcal_pctg, fat_kcal_pctg],
            }}
          />
        </div>
      </div>
      <Recommendator foodResults={foodResults} />
    </div>
  );
}

export default Results;
