// GlobeWithControls.jsx
import React, { useState } from "react";
import Globe from "./Globe";
import "./GlobeWithControls.css";

// Attention : les noms doivent correspondre à `properties.name` du topojson
const COUNTRY_BUTTONS = [
  { id: "Norway", label: "ISU Speed Skating World Cup #4" },
  { id: "Poland", label: "ISU Speed Skating European Championships" },
  { id: "Netherlands", label: "ISU Short Track European Championships" },
  { id: "Germany", label: "ISU Speed Skating World Cup #5" },
  { id: "United States of America", label: "ISU Short Track Junior World Championships" },
  { id: "Italy", label: "Olympic Winter Games 2026 Figure Skating" },
];

const GlobeWithControls = () => {
  const [selectedCountry, setSelectedCountry] = useState("");

  return (
    <div style={{ textAlign: "center" }}>

      <div className="globeAndButtons">
        <Globe width={400} selectedCountryName={selectedCountry} />

        <div className="countriesTable">
          {COUNTRY_BUTTONS.map((c) => (
            <button
              className="countryButton"
              key={c.id}
              onClick={() => setSelectedCountry(c.id)}
            >
              {c.label}
            </button>
          ))}
        </div>
      </div>

    </div>

  );
};

export default GlobeWithControls;
