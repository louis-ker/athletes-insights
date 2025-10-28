import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
// (optionnel) importe un global CSS si tu en as un :
// import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)