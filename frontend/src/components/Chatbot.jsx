import { useState, useEffect, useRef } from "react";
import BounceLoader from "react-spinners/BounceLoader";

export default function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const chatContainerRef = useRef(null); // 🔹 référence à la boîte de dialogue

  // 🔹 Fait défiler automatiquement vers le bas quand un nouveau message arrive
  useEffect(() => {
    const container = chatContainerRef.current;
    if (container) {
      container.scrollTop = container.scrollHeight;
    }
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { sender: "user", text: input }];
    setMessages(newMessages);
    setInput("");
    setIsLoading(true);

    // POUR PASSER EN LOCAL -> modifier VITE_API_URL dans .env
    // remplacer    https://athletes-insights-backend.onrender.com/api/ask
    // par          http://127.0.0.1:4000//api/ask

    try {
      const response = await fetch("http://127.0.0.1:4000//api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: input, session_id: "user123" }),
      });

      const data = await response.json();
      setMessages([...newMessages, { sender: "bot", text: data.answer }]);
    } catch (error) {
      setMessages([
        ...newMessages,
        { sender: "bot", text: "Erreur de connexion au serveur." },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div
      style={{
        padding: 20,
        background: "#f5f5f5",
        borderRadius: 10,
        width: 400,
        display: "flex",
        flexDirection: "column",
      }}
    >
      {/* 🔹 Zone de chat scrollable */}
      <div
        ref={chatContainerRef}
        style={{
          height: 300,
          overflowY: "auto",
          marginBottom: 10,
          paddingRight: 5,
          scrollBehavior: "smooth", // 👈 rend le défilement fluide
        }}
      >
        {messages.map((m, i) => (
          <div key={i} style={{ textAlign: m.sender === "user" ? "right" : "left" }}>
            <p
              style={{
                display: "inline-block",
                padding: "8px 12px",
                borderRadius: 8,
                background: m.sender === "user" ? "#007bff" : "#e5e5ea",
                color: m.sender === "user" ? "white" : "black",
                maxWidth: "80%",
                wordWrap: "break-word",
                marginBottom: 6,
              }}
            >
              {m.text}
            </p>
          </div>
        ))}

        {isLoading && (
          <div style={{ textAlign: "center", marginTop: 10 }}>
            <BounceLoader color="#c299ff" size={20} />
          </div>
        )}
      </div>

      {/* 🔹 Zone d'entrée */}
      <div style={{ display: "flex" }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          style={{ flexGrow: 1, padding: 8 }}
          placeholder="Ask something about Speed Skating"
          disabled={isLoading}
        />
        <button
          onClick={sendMessage}
          style={{ width: "18%", marginLeft: "2%" }}
          disabled={isLoading}
        >
          Envoyer
        </button>
      </div>
    </div>
  );
}
