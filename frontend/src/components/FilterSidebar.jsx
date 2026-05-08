import './FilterSidebar.css'

const CATEGORIES = ['Study', 'Food & Dining', 'Housing', 'Campus Transit', 'Health & Wellness', 'Social', 'Finance', 'Career', 'Other']

export default function FilterSidebar({ selected, onSelect }) {
  return (
    <aside style={{ width: '200px', padding: '40px 20px', borderRight: '1px solid #eee', background: 'white' }}>
      <h3 className="filter-heading">Filter by</h3>
      <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
        <li style={{ marginBottom: '10px' }}>
          <button
            onClick={() => onSelect('')}
            className="filter-btn"
            style={{ background: selected === '' ? '#e03030' : 'transparent', color: selected === '' ? 'white' : '#333' }}
          >
            All
          </button>
        </li>
        {CATEGORIES.map(cat => (
          <li key={cat} style={{ marginBottom: '10px' }}>
            <button
              onClick={() => onSelect(cat)}
              className="filter-btn"
              style={{ background: selected === cat ? '#e03030' : 'transparent', color: selected === cat ? 'white' : '#333' }}
            >
              {cat}
            </button>
          </li>
        ))}
      </ul>
    </aside>
  )
}
