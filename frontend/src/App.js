import React, { useState } from 'react';

function App() {
  const [message, setMessage] = useState('');

  const fetchMessage = async () => {
    const response = await fetch('http://localhost:5000/api/hello');
    const data = await response.json();
    setMessage(data.message);
  };

  return (
    <div style={{ textAlign: 'center', marginTop: '2rem' }}>
      <h1>Frontend React ⚛️</h1>
      <button onClick={fetchMessage}>Obtenir un message du backend</button>
      {message && <p>{message}</p>}
    </div>
  );
}

export default App;