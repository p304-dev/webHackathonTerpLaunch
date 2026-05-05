import { useState } from 'react'
import { upvoteApp } from '../services/api'

export default function AppCard({ app }) {
  const [upvotes, setUpvotes] = useState(app.upvotes)

  const handleUpvote = async () => {
    try {
      const updated = await upvoteApp(app._id)
      setUpvotes(updated.upvotes)
    } catch {
      setUpvotes(prev => prev + 1)
    }
  }

  return (
    <div style={{
      background: 'var(--card-bg)',
      borderRadius: '10px',
      padding: '16px',
      boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
      display: 'flex',
      flexDirection: 'column',
      gap: '8px',
    }}>
      <h3 style={{ fontSize: '1rem', fontWeight: 600 }}>{app.name}</h3>
      <p style={{ fontSize: '0.85rem', color: '#555', lineHeight: 1.4 }}>{app.description}</p>
      <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
        {app.category_tags.map(tag => (
          <span key={tag} style={{
            background: 'var(--umd-gold)',
            color: '#1a1a1a',
            fontSize: '0.7rem',
            fontWeight: 600,
            padding: '2px 8px',
            borderRadius: '12px',
          }}>{tag}</span>
        ))}
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '4px' }}>
        <span style={{ fontSize: '0.8rem', color: '#888' }}>by {app.submitter_name}</span>
        <button onClick={handleUpvote} style={{
          background: 'var(--umd-red)',
          color: '#fff',
          border: 'none',
          borderRadius: '6px',
          padding: '6px 12px',
          cursor: 'pointer',
          fontWeight: 600,
          fontSize: '0.85rem',
        }}>
          ▲ {upvotes}
        </button>
      </div>
    </div>
  )
}
