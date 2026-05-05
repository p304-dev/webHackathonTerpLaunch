import { Link } from 'react-router-dom'
import TrendingSection from '../components/TrendingSection'
import './Home.css'

export default function Home() {
  return (
    <div>
      <nav className="navbar">
        <span className="navbar-logo">TerpLaunch</span>
        <div className="navbar-links">
          <Link to="/browse" className="navbar-link">Browse</Link>
          <Link to="/leaderboard" className="navbar-link">Leaderboard</Link>
          <Link to="/submit" className="navbar-cta">Submit App</Link>
        </div>
      </nav>

      <section className="hero">
        <h1 className="hero-title">
          Built by <span className="hero-highlight">Terps</span>,<br />
          for <span className="hero-highlight">Terps</span>.
        </h1>
        <p className="hero-subtitle">
          Discover, upvote, and collaborate on apps made by UMD students.
          Every semester students build great tools — now they won't disappear.
        </p>
        <div className="hero-buttons">
          <Link to="/browse" className="btn-primary">Browse Apps</Link>
          <Link to="/submit" className="btn-secondary">Submit Yours</Link>
        </div>
      </section>

      <div className="content-container">
        <TrendingSection />
      </div>
    </div>
  )
}
