import { useEffect, useState, useRef, setBoxWidth } from "react";
import "./MessageBox.css";


export default function MessageBox({ pinAtPx = 1000, setResponseData, setIsLoading}) {
  const [message, setMessage] = useState("");
  const [file, setFile] = useState(null);
  const boxRef = useRef(null);
  const [pinned, setPinned] = useState(false);
  const [boxWidth, setBoxWidth] = useState(null);

  // Pin quand on dépasse pinAtPx pixels de scroll
  useEffect(() => {
    const onScroll = () => {
      const y = window.pageYOffset || document.documentElement.scrollTop;
      setPinned(y >= pinAtPx);
    };
    onScroll(); // état correct au chargement
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, [pinAtPx]);

  // Mesure la largeur quand pas pinned
  useEffect(() => {
    if (!pinned && boxRef.current) {
      setBoxWidth(boxRef.current.getBoundingClientRect().width);
    }
  }, [pinned]);

  async function handleSend() {
    const q = message.trim();
    if (!q) return;

    setIsLoading?.(true);
    // Render :
    // https://athletes-insights-backend.onrender.com/api/ask
    // Local :
    // http://localhost:4000/api/run
    try {
      const response = await fetch("https://athletes-insights-backend.onrender.com/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: q })
      });

      const data = await response.json();
      console.log("Réponse backend :", data);

      // 🔧 remonter aussi la question initiale (fallback)
      setResponseData({ ...data, _originalQuestion: q });

    } catch (err) {
      console.error("Erreur d'envoi :", err);
    } finally {
      setIsLoading?.(false);
    }

    setMessage("");
  }

  return (
    <>
      {pinned && <div className="messageBoxSpacer"></div>} 
      <div
        ref={boxRef}
        className={`messageBox ${pinned ? "pinned" : ""}`}
        style={pinned ? { width: boxWidth } : {}}
      >
        <div class="fileUploadWrapper">
          <label for="file">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 337 337">
              <circle
                stroke-width="20"
                stroke="#6c6c6c"
                fill="none"
                r="158.5"
                cy="168.5"
                cx="168.5"
              ></circle>
              <path
                stroke-linecap="round"
                stroke-width="25"
                stroke="#6c6c6c"
                d="M167.759 79V259"
              ></path>
              <path
                stroke-linecap="round"
                stroke-width="25"
                stroke="#6c6c6c"
                d="M79 167.138H259"
              ></path>
            </svg>
            <span class="tooltip">Add an image</span>
          </label>
          <input type="file" id="file" name="file" />
        </div>
        <input value={message}
          onChange={(e) => setMessage(e.target.value)}
          required
          placeholder="Ask something about Speed Skating..."
          type="text"
          id="messageInput" />
        <button id="sendButton" onClick={handleSend}>
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 664 663">
            <path
              fill="none"
              d="M646.293 331.888L17.7538 17.6187L155.245 331.888M646.293 331.888L17.753 646.157L155.245 331.888M646.293 331.888L318.735 330.228L155.245 331.888"
            ></path>
            <path
              stroke-linejoin="round"
              stroke-linecap="round"
              stroke-width="33.67"
              stroke="#6c6c6c"
              d="M646.293 331.888L17.7538 17.6187L155.245 331.888M646.293 331.888L17.753 646.157L155.245 331.888M646.293 331.888L318.735 330.228L155.245 331.888"
            ></path>
          </svg>
        </button>
      </div>
    </>

  );
}
