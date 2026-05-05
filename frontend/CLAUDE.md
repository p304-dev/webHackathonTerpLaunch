# TerpLaunch — Claude Code Context

## Project Overview
TerpLaunch is a UMD-specific student app showcase platform. Students can submit, discover, upvote, and collaborate on apps built by fellow Terps. Think **Product Hunt × GitHub**, but exclusively for UMD.

**Tagline:** Built by Terps, for Terps.

---

## My Role: Person 1 — Frontend Lead

I am responsible for:
- `Home.jsx` — Hero section + trending apps display
- `TrendingSection.jsx` — Horizontally scrollable top apps of the month
- `AppCard.jsx` — Reusable card component (name, tags, upvote count, one-click upvote)
- Routing setup (`App.jsx` with React Router)
- UMD theme and global styling (red/gold color scheme)

---

## Tech Stack

| Layer    | Technology                  |
|----------|-----------------------------|
| Frontend | React (Vite) + React Router |
| Backend  | Python + FastAPI            |
| Database | MongoDB Atlas (free tier)   |
| HTTP     | Axios                       |

---

## Project Structure

```
terpLaunch/
├── frontend/
│   └── src/
│       ├── pages/
│       │   ├── Home.jsx          ← MY PAGE
│       │   ├── Browse.jsx
│       │   ├── AppDetail.jsx
│       │   ├── Submit.jsx
│       │   └── Leaderboard.jsx
│       ├── components/
│       │   ├── AppCard.jsx       ← MY COMPONENT
│       │   ├── TrendingSection.jsx ← MY COMPONENT
│       │   ├── FilterSidebar.jsx
│       │   ├── LeaderboardTable.jsx
│       │   └── SubmitForm.jsx
│       └── App.jsx               ← MY ROUTING SETUP
│
└── backend/
    ├── main.py
    ├── routes/
    │   ├── apps.py
    │   ├── feedback.py
    │   └── leaderboard.py
    ├── models/
    │   └── schemas.py
    ├── db.py
    └── .env                      ← MONGO_URI (gitignored)
```

---

## API Endpoints (Backend — NOT my code, but I call these)

| Method | Endpoint              | Description                              |
|--------|-----------------------|------------------------------------------|
| GET    | `/apps`               | List all apps (`?category=` `?search=`)  |
| POST   | `/apps`               | Submit a new app                         |
| GET    | `/apps/:id`           | Get single app details                   |
| POST   | `/apps/:id/upvote`    | Increment upvote count                   |
| GET    | `/apps/:id/feedback`  | Get feedback for an app                  |
| POST   | `/apps/:id/feedback`  | Submit feedback                          |
| POST   | `/apps/:id/collab`    | Register collaboration interest          |
| GET    | `/leaderboard`        | Top developers ranked by upvotes         |
| GET    | `/trending`           | Top 5 most upvoted apps this month       |

Backend runs at: `http://localhost:8000`  
Auto-generated API docs: `http://localhost:8000/docs`

---

## Connecting to Backend (api.js)

All fetch calls live in `src/services/api.js`. Use the `VITE_API_URL` env variable so the base URL is configurable:

```javascript
// src/services/api.js
const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const getTrending = async () => {
  const res = await fetch(`${BASE_URL}/trending`);
  return res.json();
};

export const getAllApps = async (category = "", search = "") => {
  const res = await fetch(`${BASE_URL}/apps?category=${category}&search=${search}`);
  return res.json();
};

export const upvoteApp = async (id) => {
  const res = await fetch(`${BASE_URL}/apps/${id}/upvote`, { method: "POST" });
  return res.json();
};
```

```
# frontend/.env.local  (gitignored)
VITE_API_URL=http://localhost:8000
```

---

## Database Schema (for reference — owned by Person 4)

### `apps` collection
```json
{
  "_id": "ObjectId",
  "name": "String",
  "description": "String (max 280 chars)",
  "url": "String",
  "category_tags": ["Study", "Housing", "Food"],
  "submitter_name": "String",
  "submitter_email": "String",
  "upvotes": 0,
  "collab_requests": 0,
  "created_at": "Date"
}
```

### `feedback` collection
```json
{
  "_id": "ObjectId",
  "app_id": "ObjectId",
  "reviewer_name": "String",
  "comment": "String",
  "rating": 4,
  "created_at": "Date"
}
```

---

## App Categories (UMD-specific tags)

`Study` · `Food & Dining` · `Housing` · `Campus Transit` · `Health & Wellness` · `Social` · `Finance` · `Career` · `Other`

---

## UMD Theme

- **Primary:** UMD Red `#E03A3E`
- **Accent:** UMD Gold `#FFD200`
- **Background:** White / light gray
- Use these as CSS variables in `index.css`:

```css
:root {
  --umd-red: #E03A3E;
  --umd-gold: #FFD200;
  --bg: #f9f9f9;
  --card-bg: #ffffff;
  --text: #1a1a1a;
}
```

---

## Features — My Scope

### Must Have
- App listing cards with name, description, tags, upvote count
- One-click upvote button on AppCard
- Trending section on Home (top 5 this month)
- React Router routing setup for all pages

### Differentiators (my pages touch these)
- Monthly trending surfaced automatically on Home page
- UMD red/gold theme applied globally

### Explicitly Out of My Scope
- Browse/search page → Person 2
- Submit form → Person 2 (FE) + Person 3 (BE)
- Leaderboard page → Person 2
- All backend endpoints → Person 3
- MongoDB setup → Person 4

---

## Mock Data (use while backend isn't ready)

```javascript
// src/mock/apps.js
export const mockApps = [
  {
    _id: "1",
    name: "UMD Shuttle Tracker",
    description: "Real-time shuttle locations for all UMD routes.",
    url: "https://github.com",
    category_tags: ["Campus Transit"],
    submitter_name: "Alex T.",
    upvotes: 142,
    created_at: "2026-04-01"
  },
  {
    _id: "2",
    name: "Dining Hall Rater",
    description: "Rate and review UMD dining halls in real time.",
    url: "https://github.com",
    category_tags: ["Food & Dining"],
    submitter_name: "Jamie L.",
    upvotes: 98,
    created_at: "2026-04-10"
  },
  {
    _id: "3",
    name: "Study Room Finder",
    description: "Shows available study rooms across campus libraries.",
    url: "https://github.com",
    category_tags: ["Study"],
    submitter_name: "Morgan K.",
    upvotes: 76,
    created_at: "2026-04-15"
  }
];
```

---

## Local Setup

```bash
# Clone repo
git clone <github-repo-url>
cd terpLaunch/frontend

# Install dependencies
npm install
npm install axios react-router-dom

# Add environment variable
echo "VITE_API_URL=http://localhost:8000" > .env.local

# Run dev server
npm run dev  # http://localhost:5173
```

---

## 24-Hour Timeline (my tasks highlighted)

| Time      | My Tasks                                              |
|-----------|-------------------------------------------------------|
| Hour 0–1  | Repo setup, Vite scaffold, agree on API contract      |
| Hour 1–3  | Build `AppCard.jsx`, routing in `App.jsx`, mock data  |
| Hour 3–6  | `TrendingSection.jsx` wired to `GET /trending`        |
| Hour 6–9  | `Home.jsx` fully built, hero section, layout polish   |
| Hour 9–12 | UMD theme applied globally, mobile responsiveness     |
| Hour 12+  | Integration testing, demo prep, bug fixes             |

---

## Judging Criteria (keep these in mind)

1. **Styling** — UMD theme, clean cards, responsive layout
2. **Ease of Use** — intuitive navigation, one-click actions
3. **Usefulness/Practicality** — solves a real UMD student problem
4. **Creativity** — leaderboard, collab requests, problem-tag discovery

---

## Presentation Structure (8 minutes total)

- **Slides (3 min):** Problem → Solution → Features → Roadmap
- **Demo (5 min):** Browse → filter → app detail → upvote → submit → leaderboard
- **Key talking points:**
  - "Every semester students build great tools. Every semester they disappear."
  - Highlight leaderboard gamification and collab request as differentiators
  - Mention seeded with real UMD projects from past 2 semesters
  - Roadmap: Auth, email notifications, featured listings

---