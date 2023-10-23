import React from "react";

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
      <div>
        <label htmlFor="minPrtoPctg">Minimum protein percentage:</label>
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
        <span>{minPrtoPctg}%</span>
      </div>
      <div>
        <label htmlFor="maxFatPctg">Maximum fat percentage:</label>
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
        <span>{maxFatPctg}%</span>
      </div>
      <div>
        <label htmlFor="protPenalty">Protein penalty:</label>
        <input
          type="range"
          id="protPenalty"
          name="protPenalty"
          min="0"
          max="1000"
          step="100"
          value={protPenalty}
          onChange={(event) => setProtPenalty(event.target.value)}
        />
        <span>{protPenalty}</span>
      </div>
      <div>
        <label htmlFor="fatPenalty">Fat penalty:</label>
        <input
          type="range"
          id="fatPenalty"
          name="fatPenalty"
          min="0"
          max="10000"
          step="100"
          value={fatPenalty}
          onChange={(event) => setFatPenalty(event.target.value)}
        />
        <span>{fatPenalty}</span>
      </div>
      <div>
        <label htmlFor="kcalsPenalty">Calories penalty:</label>
        <input
          type="range"
          id="kcalsPenalty"
          name="kcalsPenalty"
          min="0"
          max="200"
          step="10"
          value={kcalsPenalty}
          onChange={(event) => setKcalsPenalty(event.target.value)}
        />
        <span>{kcalsPenalty}</span>
      </div>

      <div>
        <label htmlFor="maxKcals">Maximum calories:</label>
        <input
          type="number"
          id="maxKcals"
          name="maxKcals"
          min="0"
          max="10000"
          step="10"
          value={maxKcals}
          onChange={(event) => setMaxKcals(parseInt(event.target.value))}
        />
      </div>
    </div>
  );
}

export default Sliders;
