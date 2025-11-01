import { useEffect, useState } from "react";

function HelloAPI() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetch("https://athletes-insights-backend.onrender.com/api/hello")
      .then((response) => response.json())
      .then((data) => setMessage(data.message))
      .catch((error) => console.error("Erreur:", error));
  }, []);

  return <h1>{message}</h1>;
}

export default HelloAPI;
