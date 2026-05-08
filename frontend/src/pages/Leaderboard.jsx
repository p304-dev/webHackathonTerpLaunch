import { useState, useEffect } from 'react'
import { getLeaderboard } from '../services/api'
import { Link } from 'react-router-dom'

export default function Leaderboard() {
  const [leaders, setLeaders] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getLeaderboard().then(data => { setLeaders(data); setLoading(false) }).catch(() => setLoading(false))
  }, [])

  const medals = ['🥇', '🥈', '🥉']

  return (
    <div style={{ maxWidth: '700px', margin: '0 auto', padding: '40px 20px' }}>
      <Link to="/" style={{ color: '#e03030', textDecoration: 'none' }}>← Home</Link>
      <h1 style={{ color: '#e03030', marginTop: '16px' }}>🏆 Developer Leaderboard</h1>
      <p style={{ color: '#986262', fontWeight: 'bold', marginTop: '16px' }}>Top UMD developers ranked by total upvotes across all their apps.</p>

      {loading ? <p>Loading...</p> : leaders.length === 0 ? <p>No developers yet. <Link to="/submit">Submit an app!</Link></p> : (
        <div style={{ marginTop: '24px' }}>
          {leaders.map((dev, i) => (
            <div key={dev.submitter_name} style={{ display: 'flex', alignItems: 'center', background: 'white', border: '1px solid #eee', borderRadius: '12px', padding: '16px 20px', marginBottom: '12px', boxShadow: i < 3 ? '0 2px 8px rgba(224,48,48,0.1)' : 'none' }}>
              <span style={{ fontSize: '28px', width: '40px' }}>{medals[i] || `#${i + 1}`}</span>
              <div style={{ flex: 1, marginLeft: '16px' }}>
                <div style={{ fontWeight: 'bold', fontSize: '17px' }}>{dev.submitter_name}</div>
                <div style={{ color: '#888', fontSize: '13px' }}>{dev.app_count} app{dev.app_count !== 1 ? 's' : ''} submitted</div>
              </div>
              <div style={{ textAlign: 'right' }}>
                <div style={{ fontWeight: 'bold', color: '#e03030', fontSize: '20px' }}>{dev.total_upvotes}</div>
                <div style={{ color: '#888', fontSize: '12px' }}>upvotes</div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
