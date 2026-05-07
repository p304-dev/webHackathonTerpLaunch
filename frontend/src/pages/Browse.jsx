import { useState, useEffect } from 'react'
import { getAllApps } from '../services/api'
import AppCard from '../components/AppCard'
import FilterSidebar from '../components/FilterSidebar'
import { Link } from 'react-router-dom'

export default function Browse() {
  const [apps, setApps] = useState([])
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchApps()
  }, [category])

  const fetchApps = async () => {
    setLoading(true)
    try {
      const data = await getAllApps(category, search)
      setApps(data)
    } catch (err) {
      console.error(err)
    }
    setLoading(false)
  }

  const handleSearch = (e) => {
    e.preventDefault()
    fetchApps()
  }

  return (
    <div style={{ display: 'flex', minHeight: '100vh', background: '#f9f9f9' }}>
      <FilterSidebar selected={category} onSelect={setCategory} />
      <main style={{ flex: 1, padding: '40px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
          <h1 style={{ margin: 0, color: '#e03030' }}>🐢 Browse Apps</h1>
          <Link to="/submit" style={{ background: '#e03030', color: 'white', padding: '10px 20px', borderRadius: '8px', textDecoration: 'none', fontWeight: 'bold' }}>
            + Submit App
          </Link>
        </div>

        <form onSubmit={handleSearch} style={{ marginBottom: '24px', display: 'flex', gap: '10px' }}>
          <input
            type="text"
            placeholder="Search apps..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            style={{ flex: 1, padding: '10px 16px', borderRadius: '8px', border: '1px solid #ddd', fontSize: '15px' }}
          />
          <button type="submit" style={{ background: '#e03030', color: 'white', border: 'none', padding: '10px 20px', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' }}>
            Search
          </button>
        </form>

        {loading ? (
          <p>Loading apps...</p>
        ) : apps.length === 0 ? (
          <p>No apps found. <Link to="/submit">Submit the first one!</Link></p>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '20px' }}>
            {apps.map(app => (
              <Link key={app.id} to={`/apps/${app.id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
                <AppCard app={app} />
              </Link>
            ))}
          </div>
        )}
      </main>
    </div>
  )
}
