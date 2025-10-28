import { useState } from 'react'

function App() {
  const [message, setMessage] = useState('')

  const fetchMessage = async () => {
    const res = await fetch('/api/hello')
    const data = await res.json()
    setMessage(data.message)
  }

  return (
    <div>
      <h1>Frontend Vite ⚡</h1>
      <button onClick={fetchMessage}>Parle moi backend !</button>
      {message && <p>{message}</p>}
    </div>
  )
}

export default App