import React from "react";
import Plot from "react-plotly.js";

function PieChart({ data }) {
  const { title, labels, values, colors } = data;

  const pieChartData = [
    {
      values: values,
      labels: labels,
      type: "pie",
      marker: {
        colors: ["#E7ECEF", "#63B3ED", "#F6AD55"],
      },
    },
  ];

  return (
    <Plot
      data={pieChartData}
      layout={{
        width: 300,
        height: 300,
        title: title,
        paper_bgcolor: "rgba(0,0,0,0)",
      }}
    />
  );
}

export default PieChart;
