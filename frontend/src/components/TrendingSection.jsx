import { useEffect, useState } from 'react'
import { getTrending } from '../services/api'
import { mockApps } from '../mock/apps'
import AppCard from './AppCard'

export default function TrendingSection() {
  const [apps, setApps] = useState([])

  useEffect(() => {
    getTrending()
      .then(setApps)
      .catch(() => setApps(mockApps))
  }, [])

  return (
    <section style={{ padding: '24px 0' }}>
      <h2 style={{ fontSize: '1.3rem', fontWeight: 700, marginBottom: '16px', color: 'var(--umd-red)' }}>
        Trending This Month
      </h2>
      <div style={{
        display: 'flex',
        gap: '16px',
        overflowX: 'auto',
        paddingBottom: '8px',
      }}>
        {apps.map(app => (
          <div key={app._id} style={{ minWidth: '260px', maxWidth: '280px', flexShrink: 0 }}>
            <AppCard app={app} />
          </div>
        ))}
      </div>
    </section>
  )
}
