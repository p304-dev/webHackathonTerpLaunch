import { useState } from 'react'
import { upvoteApp } from '../services/api'
import './AppCard.css'

export default function AppCard({ app }) {
  const [upvotes, setUpvotes] = useState(app.upvotes)

  const handleUpvote = async () => {
    try {
      const updated = await upvoteApp(app.id)
      setUpvotes(updated.upvotes)
    } catch {
      setUpvotes(prev => prev + 1)
    }
  }

  return (
    <div className="card">
      <h3 className="card-title">{app.name}</h3>
      <p className="card-description">{app.description}</p>
      <div className="card-tags">
        {app.category_tags.map(tag => (
          <span key={tag} className="card-tag">{tag}</span>
        ))}
      </div>
      <div className="card-footer">
        <span className="card-author">by {app.submitter_name}</span>
        <button className="card-upvote" onClick={handleUpvote}>
          ▲ {upvotes}
        </button>
      </div>
    </div>
  )
}
