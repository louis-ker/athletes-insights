import { useState } from 'react'
import Dock from './components/Dock'
import { VscHome, VscArchive, VscAccount, VscSettingsGear } from 'react-icons/vsc'

export default function App() {
  const [message, setMessage] = useState('')

  // Garde cette route telle quelle si tu as déjà configuré ton proxy Vite en dev
  // et CORS côté backend en prod. Sinon remplace par ton URL publique complète.
  const fetchMessage = async () => {
    try {
      const res = await fetch('/api/hello')
      const data = await res.json()
      setMessage(data.message)
    } catch (e) {
      setMessage(`Erreur: ${e.message}`)
    }
  }

  // Items du Dock
  const dockItems = [
    { icon: <VscHome size={18} />,    label: 'Home',     onClick: () => alert('Home!') },
    { icon: <VscArchive size={18} />, label: 'Archive',  onClick: () => alert('Archive!') },
    { icon: <VscAccount size={18} />, label: 'Profile',  onClick: () => alert('Profile!') },
    { icon: <VscSettingsGear size={18} />, label: 'Settings', onClick: () => alert('Settings!') },
  ]

  return (
    // Laisse de la place en bas pour le Dock (qui est positionné en absolute)
    <div style={{ minHeight: '100vh', position: 'relative', paddingBottom: 96 }}>
      <main style={{ maxWidth: 880, margin: '0 auto', padding: '2rem 1rem' }}>
        <h1>Frontend Vite ⚡</h1>
        <p>Exemple d’appel à ton backend Flask sur Render.</p>
        <button onClick={fetchMessage}>Parle moi backend !</button>
        {message && <p style={{ marginTop: 12 }}>{message}</p>}
      </main>

      {/* Dock au bas de la page */}
      <Dock
        items={dockItems}
        panelHeight={88}
        baseItemSize={80}
        magnification={120}
        distance={200}
      />
    </div>
  )
}
