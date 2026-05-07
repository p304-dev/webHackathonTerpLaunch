import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { getAppById, upvoteApp } from '../services/api'

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function AppDetail() {
  const { id } = useParams()
  const [app, setApp] = useState(null)
  const [feedback, setFeedback] = useState([])
  const [loading, setLoading] = useState(true)
  const [upvotes, setUpvotes] = useState(0)
  const [collabMsg, setCollabMsg] = useState('')

  // feedback form state
  const [reviewerName, setReviewerName] = useState('')
  const [comment, setComment] = useState('')
  const [rating, setRating] = useState(5)
  const [feedbackMsg, setFeedbackMsg] = useState('')

  useEffect(() => {
    const load = async () => {
      try {
        const data = await getAppById(id)
        setApp(data)
        setUpvotes(data.upvotes)
        const fbRes = await fetch(`${BASE_URL}/apps/${id}/feedback`)
        const fbData = await fbRes.json()
        setFeedback(fbData)
      } catch (err) {
        console.error(err)
      }
      setLoading(false)
    }
    load()
  }, [id])

  const handleUpvote = async () => {
    try {
      const updated = await upvoteApp(id)
      setUpvotes(updated.upvotes)
    } catch {
      setUpvotes(prev => prev + 1)
    }
  }

  const handleCollab = async () => {
    try {
      await fetch(`${BASE_URL}/apps/${id}/collab`, { method: 'POST' })
      setCollabMsg('Interest registered! The creator will be notified.')
    } catch {
      setCollabMsg('Something went wrong.')
    }
  }

  const handleFeedback = async (e) => {
    e.preventDefault()
    try {
      await fetch(`${BASE_URL}/apps/${id}/feedback`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ reviewer_name: reviewerName, comment, rating: parseInt(rating) })
      })
      setFeedbackMsg('Feedback submitted!')
      setReviewerName('')
      setComment('')
      setRating(5)
      const fbRes = await fetch(`${BASE_URL}/apps/${id}/feedback`)
      setFeedback(await fbRes.json())
    } catch {
      setFeedbackMsg('Something went wrong.')
    }
  }

  if (loading) return <div style={{ padding: '40px' }}>Loading...</div>
  if (!app) return <div style={{ padding: '40px' }}>App not found.</div>

  return (
    <div style={{ maxWidth: '700px', margin: '0 auto', padding: '40px 20px' }}>
      <Link to="/browse" style={{ color: '#e03030', textDecoration: 'none' }}>← Back to Browse</Link>

      <h1 style={{ marginTop: '16px', color: '#e03030', marginBottom: '16px' }}>{app.name}</h1>
      <p style={{ fontSize: '16px', color: '#444', marginBottom: '16px' }}>{app.description}</p>

      <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', marginBottom: '16px' }}>
        {app.category_tags.map(tag => (
          <span key={tag} style={{ background: '#fde8e8', color: '#e03030', padding: '4px 10px', borderRadius: '20px', fontSize: '13px' }}>{tag}</span>
        ))}
      </div>

      <p style={{ color: '#ffffff', marginBottom: '16px' }}>by <strong>{app.submitter_name}</strong></p>

      <div style={{ display: 'flex', gap: '12px', marginBottom: '32px' }}>
        <a href={app.url} target="_blank" rel="noreferrer" style={{ background: '#e03030', color: 'white', padding: '10px 20px', borderRadius: '8px', textDecoration: 'none', fontWeight: 'bold' }}>
          Visit App →
        </a>
        <button onClick={handleUpvote} style={{ background: 'white', border: '1px solid #e03030', color: '#e03030', padding: '10px 20px', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' }}>
          ▲ Upvote ({upvotes})
        </button>
        <button onClick={handleCollab} style={{ background: '#fff8e1', border: '1px solid #f0c040', color: '#b8860b', padding: '10px 20px', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' }}>
          🤝 I want to help
        </button>
      </div>
      {collabMsg && <p style={{ color: 'green' }}>{collabMsg}</p>}

      <hr style={{ margin: '32px 0', borderColor: '#eee' }} />

      <h2>Leave Feedback</h2>
      <form onSubmit={handleFeedback} style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: '32px' }}>
        <input required placeholder="Your name" value={reviewerName} onChange={e => setReviewerName(e.target.value)} style={{ padding: '10px', borderRadius: '8px', border: '1px solid #ddd' }} />
        <textarea required placeholder="Your comment" value={comment} onChange={e => setComment(e.target.value)} rows={3} style={{ padding: '10px', borderRadius: '8px', border: '1px solid #ddd', resize: 'vertical' }} />
        <div>
          <label style={{ display: 'block', marginBottom: '4px' }}>Rating:</label>
          <select value={rating} onChange={e => setRating(e.target.value)} style={{ padding: '8px', borderRadius: '6px', border: '1px solid #ddd' }}>
            {[5,4,3,2,1].map(n => <option key={n} value={n}>{n} ⭐</option>)}
          </select>
        </div>
        <button type="submit" style={{ background: '#e03030', color: 'white', border: 'none', padding: '10px', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' }}>
          Submit Feedback
        </button>
        {feedbackMsg && <p style={{ color: 'green' }}>{feedbackMsg}</p>}
      </form>

      <h2>Reviews ({feedback.length})</h2>
      {feedback.length === 0 ? <p style={{ color: '#888' }}>No reviews yet. Be the first!</p> : (
        feedback.map(fb => (
          <div key={fb.id} style={{ background: 'white', border: '1px solid #eee', borderRadius: '10px', padding: '16px', marginBottom: '12px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <strong>{fb.reviewer_name}</strong>
              <span>{'⭐'.repeat(fb.rating)}</span>
            </div>
            <p style={{ margin: '8px 0 0', color: '#444' }}>{fb.comment}</p>
          </div>
        ))
      )}
    </div>
  )
}
