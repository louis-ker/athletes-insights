// import { useState } from 'react'
// import Dock from './components/Dock'
// import { VscHome, VscArchive, VscAccount, VscSettingsGear } from 'react-icons/vsc'

// import { useEffect } from 'react';
// import ScrollReveal from 'scrollreveal';

// import imagePrincipale from './assets/image.jpg'

// export default function App() {
//   const [message, setMessage] = useState('')

//   const fetchMessage = async () => {
//     try {
//       const res = await fetch('/api/hello')
//       const data = await res.json()
//       setMessage(data.message)
//     } catch (e) {
//       setMessage(`Erreur: ${e.message}`)
//     }
//   }

//   // Items du Dock
//   const dockItems = [
//     { icon: <VscHome size={24} />,    label: 'Home',     onClick: () => alert('Home!') },
//     { icon: <VscArchive size={24} />, label: 'Archive',  onClick: () => alert('Archive!') },
//     { icon: <VscAccount size={24} />, label: 'Profile',  onClick: () => alert('Profile!') },
//     { icon: <VscSettingsGear size={24} />, label: 'Settings', onClick: () => alert('Settings!') },
//   ]

//   // Animation ScrollReveal
//   useEffect(() => {
//     ScrollReveal().reveal('.reveal', {
//       duration: 1000,
//       distance: '50px',
//       origin: 'bottom',
//       easing: 'ease-in-out',
//       reset: false,
//     })
//   }, [])

//   return (
//     // Laisse de la place en bas pour le Dock (qui est positionné en absolute)
//     <div style={{ minHeight: '100vh', position: 'relative', paddingBottom: 96, margin: 0 }}>
//       <img id="imagePrincipale" src={imagePrincipale} alt="description de l'image" />
//       <div style={{ margin: 0, padding: 0 }}>
        
        
//         <h1 className="reveal">Frontend Vite ⚡</h1>
//         <button className="reveal" onClick={fetchMessage}>Parle moi backend !</button>
//         {message && <p className="reveal">{message}</p>}
//         <h1 className="reveal">Frontend Vite ⚡</h1>
//         <h1 className="reveal">Frontend Vite ⚡</h1>
//         <h1 className="reveal">Frontend Vite ⚡</h1>
//         <h1 className="reveal">Frontend Vite ⚡</h1>
//         <h1 className="reveal">Frontend Vite ⚡</h1>
//         <h1 className="reveal">Frontend Vite ⚡</h1>
//         <h1 className="reveal">Frontend Vite ⚡</h1>
//         <h1 className="reveal">Frontend Vite ⚡</h1>
//         <h1 className="reveal">Frontend Vite ⚡</h1>
//         <h1 className="reveal">Frontend Vite ⚡</h1>
//         <h1 className="reveal">Frontend Vite ⚡</h1>
//         <h1 className="reveal">Frontend Vite ⚡</h1>
//         <h1 className="reveal">Frontend Vite ⚡</h1>
//         <h1 className="reveal">Frontend Vite ⚡</h1>
//         <h1 className="reveal">Frontend Vite ⚡</h1>
//         <h1 className="reveal">Frontend Vite ⚡</h1>
//         <h1 className="reveal">Frontend Vite ⚡</h1>
//         <h1 className="reveal">Frontend Vite ⚡</h1>
//         <h1 className="reveal">Frontend Vite ⚡</h1>
//         <h1 className="reveal">Frontend Vite ⚡</h1>
//       </div>

//       <Dock
//         items={dockItems}
//         panelHeight={88}
//         baseItemSize={80}
//         magnification={120}
//         distance={200}
//       />
//     </div>
//   )
// }


import { useState, useEffect } from 'react'

import Dock from './components/Dock'
import { VscHome, VscArchive, VscAccount, VscSettingsGear } from 'react-icons/vsc'

import ScrollReveal from 'scrollreveal'
import styled from 'styled-components'

import './App.css'
import imagePrincipale from './assets/image.jpg'

const Page = styled.div`
  width: 100vw;
  height: 100%;
  min-height: 100%;
  box-sizing: border-box;
  padding-bottom: 96px; /* Laisse de la place pour le Dock */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  text-align: center;
`

export default function App() {
  const [message, setMessage] = useState('')

  const fetchMessage = async () => {
    try {
      const res = await fetch('/api/hello')
      const data = await res.json()
      setMessage(data.message)
    } catch (e) {
      setMessage(`Erreur: ${e.message}`)
    }
  }

  const dockItems = [
    { icon: <VscHome size={24} />, label: 'Home', onClick: () => alert('Home!') },
    { icon: <VscArchive size={24} />, label: 'Archive', onClick: () => alert('Archive!') },
    { icon: <VscAccount size={24} />, label: 'Profile', onClick: () => alert('Profile!') },
    { icon: <VscSettingsGear size={24} />, label: 'Settings', onClick: () => alert('Settings!') },
  ]

  useEffect(() => {
    ScrollReveal().reveal('.reveal', {
      duration: 1000,
      distance: '50px',
      origin: 'bottom',
      easing: 'ease-in-out',
      reset: false,
    })
  }, [])

  return (
    <Page>
      <img className="reveal" src={imagePrincipale} alt="Description de l'image" />
      <h1 className="reveal">Frontend Vite ⚡</h1>
      <button className="reveal" onClick={fetchMessage}>Parle moi backend !</button>
      {message && <p className="reveal">{message}</p>}

      <Dock
        items={dockItems}
        panelHeight={88}
        baseItemSize={80}
        magnification={120}
        distance={200}
      />
    </Page>
  )
}
