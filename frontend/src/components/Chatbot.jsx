import { useState } from "react";

export default function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { sender: "user", text: input }];
    setMessages(newMessages);
    setInput("");

    // POUR PASSER EN LOCAL -> modifier VITE_API_URL dans .env
    const API_URL = import.meta.env.VITE_API_URL; // à modifier dans .env
    
    const response = await fetch(`${API_URL}/api/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: input, session_id: "user123" })
    });

    const data = await response.json();
    setMessages([...newMessages, { sender: "bot", text: data.answer }]);
  };

  return (
    <div style={{ padding: 20, background: "#f5f5f5", borderRadius: 10, width: 400 }}>
      <div style={{ height: 300, overflowY: "auto", marginBottom: 10 }}>
        {messages.map((m, i) => (
          <div key={i} style={{ textAlign: m.sender === "user" ? "right" : "left" }}>
            <p style={{ 
              display: "inline-block",
              padding: "8px 12px",
              borderRadius: 8,
              background: m.sender === "user" ? "#007bff" : "#e5e5ea",
              color: m.sender === "user" ? "white" : "black"
            }}>
              {m.text}
            </p>
          </div>
        ))}
      </div>

      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        style={{ width: "80%", padding: 8 }}
        placeholder="Écris ta question..."
      />
      <button onClick={sendMessage} style={{ width: "18%", marginLeft: "2%" }}>Envoyer</button>
    </div>
  );
}
