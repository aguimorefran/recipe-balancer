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
        colors: colors,
      },
    },
  ];

  return (
    <Plot
      data={pieChartData}
      layout={{
        width: 400,
        height: 400,
        title: title,
      }}
    />
  );
}

export default PieChart;
