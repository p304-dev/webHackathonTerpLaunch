import { useEffect, useState } from 'react'
import { getTrending } from '../services/api'
import { mockApps } from '../mock/apps'
import AppCard from './AppCard'
import './TrendingSection.css'

export default function TrendingSection() {
  const [apps, setApps] = useState([])

  useEffect(() => {
    getTrending()
      .then(setApps)
      .catch(() => setApps(mockApps))
  }, [])

  return (
    <section className="trending-section">
      <h2 className="trending-title">Trending This Month</h2>
      <div className="trending-scroll">
        {apps.map(app => (
          <div key={app._id} className="trending-item">
            <AppCard app={app} />
          </div>
        ))}
      </div>
    </section>
  )
}
