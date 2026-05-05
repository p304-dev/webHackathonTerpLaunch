import { Link } from 'react-router-dom'
import TrendingSection from '../components/TrendingSection'

export default function Home() {
  return (
    <div style={{ maxWidth: '1100px', margin: '0 auto', padding: '0 20px' }}>
      {/* Navbar */}
      <nav style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '16px 0',
        borderBottom: '2px solid var(--umd-gold)',
      }}>
        <span style={{ fontWeight: 800, fontSize: '1.4rem', color: 'var(--umd-red)' }}>TerpLaunch</span>
        <div style={{ display: 'flex', gap: '20px' }}>
          <Link to="/browse" style={{ color: 'var(--text)', textDecoration: 'none', fontWeight: 500 }}>Browse</Link>
          <Link to="/leaderboard" style={{ color: 'var(--text)', textDecoration: 'none', fontWeight: 500 }}>Leaderboard</Link>
          <Link to="/submit" style={{
            background: 'var(--umd-red)',
            color: '#fff',
            padding: '8px 16px',
            borderRadius: '6px',
            textDecoration: 'none',
            fontWeight: 600,
          }}>Submit App</Link>
        </div>
      </nav>

      {/* Hero */}
      <section style={{ textAlign: 'center', padding: '60px 20px 40px' }}>
        <h1 style={{ fontSize: '2.8rem', fontWeight: 800, lineHeight: 1.2, marginBottom: '16px' }}>
          Built by <span style={{ color: 'var(--umd-red)' }}>Terps</span>,<br />
          for <span style={{ color: 'var(--umd-red)' }}>Terps</span>.
        </h1>
        <p style={{ fontSize: '1.1rem', color: '#555', maxWidth: '520px', margin: '0 auto 28px' }}>
          Discover, upvote, and collaborate on apps made by UMD students.
          Every semester students build great tools — now they won't disappear.
        </p>
        <div style={{ display: 'flex', gap: '12px', justifyContent: 'center' }}>
          <Link to="/browse" style={{
            background: 'var(--umd-red)',
            color: '#fff',
            padding: '12px 28px',
            borderRadius: '8px',
            textDecoration: 'none',
            fontWeight: 700,
            fontSize: '1rem',
          }}>Browse Apps</Link>
          <Link to="/submit" style={{
            background: 'var(--umd-gold)',
            color: '#1a1a1a',
            padding: '12px 28px',
            borderRadius: '8px',
            textDecoration: 'none',
            fontWeight: 700,
            fontSize: '1rem',
          }}>Submit Yours</Link>
        </div>
      </section>

      {/* Trending */}
      <TrendingSection />
    </div>
  )
}
