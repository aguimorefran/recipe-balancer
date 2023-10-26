import React from "react";
import "./styles.css";

function Sliders(props) {
  const {
    minPrtoPctg,
    maxFatPctg,
    protPenalty,
    fatPenalty,
    kcalsPenalty,
    maxKcals,
    setMinPrtoPctg,
    setMaxFatPctg,
    setProtPenalty,
    setFatPenalty,
    setKcalsPenalty,
    setMaxKcals,
  } = props;

  return (
    <div>
      <h1>Balance configuration</h1>
      <div style={{ display: "flex", flexDirection: "row" }}>
        <div style={{ minWidth: "300px" }}>
          <label htmlFor="minPrtoPctg">Minimum protein percentage:</label>
          <br />
          <label htmlFor="maxFatPctg">Maximum fat percentage:</label>
          <br />
          <label htmlFor="protPenalty">Protein penalty:</label>
          <br />
          <label htmlFor="fatPenalty">Fat penalty:</label>
          <br />
          <label htmlFor="kcalsPenalty">Kcals penalty:</label>
          <br />
          <label htmlFor="maxKcals">Maximum kcals:</label>
        </div>
        <div style={{ flex: 1 }}>
          <input
            type="range"
            id="minPrtoPctg"
            name="minPrtoPctg"
            min="0"
            max="1"
            step="0.05"
            value={minPrtoPctg}
            onChange={(event) => {
              const newMinPrtoPctg = event.target.value;
              const newMaxFatPctg = Math.min(
                maxFatPctg,
                1 - newMinPrtoPctg
              ).toFixed(2);
              setMinPrtoPctg(newMinPrtoPctg);
              setMaxFatPctg(newMaxFatPctg);
            }}
          />
          <label htmlFor="minPrtoPctg">{parseInt(minPrtoPctg * 100)}%</label>
          <br />
          <input
            type="range"
            id="maxFatPctg"
            name="maxFatPctg"
            min="0"
            max={1 - minPrtoPctg}
            step="0.05"
            value={maxFatPctg}
            onChange={(event) => {
              const newMaxFatPctg = event.target.value;
              const newMinPrtoPctg = Math.min(
                minPrtoPctg,
                1 - newMaxFatPctg
              ).toFixed(2);
              setMaxFatPctg(newMaxFatPctg);
              setMinPrtoPctg(newMinPrtoPctg);
            }}
          />
          <label htmlFor="maxFatPctg">{parseInt(maxFatPctg * 100)}%</label>
          <br />
          <input
            type="range"
            id="protPenalty"
            name="protPenalty"
            min="0"
            max="10000"
            step="1000"
            value={protPenalty}
            onChange={(event) => setProtPenalty(event.target.value)}
          />
          <label htmlFor="protPenalty">{protPenalty}</label>
          <br />
          <input
            type="range"
            id="fatPenalty"
            name="fatPenalty"
            min="0"
            max="10000"
            step="1000"
            value={fatPenalty}
            onChange={(event) => setFatPenalty(event.target.value)}
          />
          <label htmlFor="fatPenalty">{fatPenalty}</label>
          <br />
          <input
            type="range"
            id="kcalsPenalty"
            name="kcalsPenalty"
            min="0"
            max="2000"
            step="100"
            value={kcalsPenalty}
            onChange={(event) => setKcalsPenalty(event.target.value)}
          />
          <label htmlFor="kcalsPenalty">{kcalsPenalty}</label>
          <br />
          <input
            type="text"
            className="textbox-4"
            id="maxKcals"
            name="maxKcals"
            value={maxKcals}
            onChange={(event) => setMaxKcals(event.target.value)}
          />
          <label htmlFor="maxKcals">kcal</label>
        </div>
      </div>
    </div>
  );
}

export default Sliders;
