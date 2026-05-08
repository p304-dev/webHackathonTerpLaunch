import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const CATEGORIES = ['Study', 'Food & Dining', 'Housing', 'Campus Transit', 'Health & Wellness', 'Social', 'Finance', 'Career', 'Other']

export default function Submit() {
  const navigate = useNavigate()
  const [form, setForm] = useState({ name: '', description: '', url: '', submitter_name: '', submitter_email: '', category_tags: [] })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleChange = e => setForm(prev => ({ ...prev, [e.target.name]: e.target.value }))

  const toggleTag = (tag) => {
    setForm(prev => ({
      ...prev,
      category_tags: prev.category_tags.includes(tag)
        ? prev.category_tags.filter(t => t !== tag)
        : [...prev.category_tags, tag]
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (form.category_tags.length === 0) { setError('Please select at least one category.'); return }
    if (form.description.length > 280) { setError('Description must be 280 characters or less.'); return }
    setLoading(true)
    try {
      const res = await fetch(`${BASE_URL}/apps`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form)
      })
      if (!res.ok) throw new Error()
      navigate('/browse')
    } catch {
      setError('Something went wrong. Please try again.')
    }
    setLoading(false)
  }

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '40px 20px' }}>
      <Link to="/browse" style={{ color: '#e03030', textDecoration: 'none' }}>← Back to Browse</Link>
      <h1 style={{ color: '#e03030', marginTop: '16px' }}>Submit Your App</h1>

      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <div>
          <label style={{ fontWeight: 'bold', display: 'block', marginBottom: '6px', color: '#986262', marginTop: '16px' }}>App Name *</label>
          <input required name="name" value={form.name} onChange={handleChange} placeholder="My Cool App" style={{ width: '100%', padding: '10px', borderRadius: '8px', border: '1px solid #ddd', boxSizing: 'border-box' }} />
        </div>

        <div>
          <label style={{ fontWeight: 'bold', display: 'block', marginBottom: '6px', color: '#986262'  }}>Description * <span style={{ color: '#999', fontWeight: 'normal', color: '#986262'  }}>({form.description.length}/280)</span></label>
          <textarea required name="description" value={form.description} onChange={handleChange} placeholder="What does your app do?" rows={4} maxLength={280} style={{ width: '100%', padding: '10px', borderRadius: '8px', border: '1px solid #ddd', resize: 'vertical', boxSizing: 'border-box' }} />
        </div>

        <div>
          <label style={{ fontWeight: 'bold', display: 'block', marginBottom: '6px', color: '#986262' }}>App URL <span style={{ fontWeight: 'normal', color: '#999' }}>(optional)</span></label>
          <input name="url" value={form.url} onChange={handleChange} placeholder="https://myapp.com" style={{ width: '100%', padding: '10px', borderRadius: '8px', border: '1px solid #ddd', boxSizing: 'border-box' }} />
        </div>

        <div>
          <label style={{ fontWeight: 'bold', display: 'block', marginBottom: '6px', color: '#986262'  }}>Your Name *</label>
          <input required name="submitter_name" value={form.submitter_name} onChange={handleChange} placeholder="Jane Smith" style={{ width: '100%', padding: '10px', borderRadius: '8px', border: '1px solid #ddd', boxSizing: 'border-box' }} />
        </div>

        <div>
          <label style={{ fontWeight: 'bold', display: 'block', marginBottom: '6px', color: '#986262'  }}>Your Email *</label>
          <input required type="email" name="submitter_email" value={form.submitter_email} onChange={handleChange} placeholder="jane@umd.edu" style={{ width: '100%', padding: '10px', borderRadius: '8px', border: '1px solid #ddd', boxSizing: 'border-box' }} />
        </div>

        <div>
          <label style={{ fontWeight: 'bold', display: 'block', marginBottom: '10px' , color: '#986262'  }}>Categories * (select all that apply)</label>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
            {CATEGORIES.map(cat => (
              <button type="button" key={cat} onClick={() => toggleTag(cat)}
                style={{ background: form.category_tags.includes(cat) ? '#e03030' : 'white', color: form.category_tags.includes(cat) ? 'white' : '#333', border: '1px solid #ddd', borderRadius: '20px', padding: '6px 14px', cursor: 'pointer' }}>
                {cat}
              </button>
            ))}
          </div>
        </div>

        {error && <p style={{ color: 'red', margin: 0 }}>{error}</p>}

        <button type="submit" disabled={loading} style={{ background: '#e03030', color: 'white', border: 'none', padding: '14px', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold', fontSize: '16px', marginTop: '8px' }}>
          {loading ? 'Submitting...' : 'Submit App 🐢'}
        </button>
      </form>
    </div>
  )
}
