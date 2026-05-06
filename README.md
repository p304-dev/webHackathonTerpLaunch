# 🐢 TerpLaunch

> The student app showcase platform built by Terps, for Terps.

TerpLaunch is a UMD-specific platform where student developers can submit their apps and tools, and other students can discover, upvote, and collaborate on them. Think **Product Hunt × GitHub**, but built exclusively for the University of Maryland community.

---

## 🎯 The Problem

Every semester, UMD students build impressive apps — dining tools, shuttle trackers, study helpers, housing finders. And every semester, those apps quietly disappear. There's no central place to find them, no way to know if something already exists before building it, and no marketing channel within the campus community.

**TerpLaunch solves that.**

---

## ✨ Features

### Must-Have (Demo Scope)
- 📋 **App Listings** — Browse all student-built apps with name, description, category, and link
- 🔍 **Search & Filter** — Filter apps by the problem they solve (Study, Food, Housing, Transit, etc.)
- 📈 **Monthly Trending** — Top apps of the month surfaced automatically
- 👍 **Upvoting** — One-click upvote on any app
- 📝 **Submit an App** — Simple form for developers to add their project

### Differentiators
- 🏆 **Developer Leaderboard** — Ranked list of top devs by total upvotes (gamification)
- 🤝 **Collaboration Requests** — Click "I want to help" on any app to signal interest to the creator
- 💬 **Feedback System** — Leave a star rating + comment on any app
- 🏷️ **Problem-Tag Taxonomy** — UMD-specific categories that make discovery feel native to campus life

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React (Vite) + React Router |
| Backend | Python + FastAPI |
| Database | MongoDB (Atlas free tier) |
| HTTP Client | Axios |

---

## 🗂️ Project Structure

```
terpLaunch/
├── frontend/                  # React app
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Home.jsx       # Hero + trending section
│   │   │   ├── Browse.jsx     # All apps + search/filter
│   │   │   ├── AppDetail.jsx  # Single app page
│   │   │   ├── Submit.jsx     # Submit new app form
│   │   │   └── Leaderboard.jsx
│   │   ├── components/
│   │   │   ├── AppCard.jsx
│   │   │   ├── FilterSidebar.jsx
│   │   │   ├── TrendingSection.jsx
│   │   │   └── LeaderboardTable.jsx
│   │   └── App.jsx
│
└── backend/                   # FastAPI app
    ├── main.py
    ├── routes/
    │   ├── apps.py
    │   ├── feedback.py
    │   └── leaderboard.py
    ├── models/
    │   └── schemas.py
    ├── db.py                  # MongoDB connection
    └── .env                   # MONGO_URI (gitignored)
```

---

## 🚀 Local Setup

### Frontend
```bash
npm create vite@latest frontend -- --template react
cd frontend
npm install axios react-router-dom
npm run dev        # http://localhost:5173
```

### Backend
```bash
pip install fastapi uvicorn pymongo python-dotenv
# Add .env file with:
# MONGO_URI=<your MongoDB Atlas connection string>
uvicorn main:app --reload    # http://localhost:8000
```

### MongoDB
1. Create a free cluster at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Create database: `terpLaunch`
3. Create collections: `apps`, `feedback`
4. Whitelist `0.0.0.0/0` for network access (hackathon only)
5. Copy your connection string into `.env` as `MONGO_URI`

---

## 📡 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/apps` | List all apps (supports `?category=` and `?search=`) |
| POST | `/apps` | Submit a new app |
| GET | `/apps/:id` | Get app details |
| POST | `/apps/:id/upvote` | Upvote an app |
| GET | `/apps/:id/feedback` | Get feedback for an app |
| POST | `/apps/:id/feedback` | Submit feedback |
| POST | `/apps/:id/collab` | Register collaboration interest |
| GET | `/leaderboard` | Top developers ranked by upvotes |
| GET | `/trending` | Top 5 apps this month |

API docs auto-generated at `http://localhost:8000/docs` via FastAPI.

---

## 🗄️ Database Schema

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

## 🏷️ App Categories

UMD-specific problem tags used for filtering:

`Study` · `Food & Dining` · `Housing` · `Campus Transit` · `Health & Wellness` · `Social` · `Finance` · `Career` · `Other`

---

## 🗓️ 24-Hour Build Plan

| Time | Goal |
|------|------|
| Hour 0–1 | Repo setup, agree on API contract, seed schema |
| Hour 1–3 | AppCard + routing (FE) · GET/POST /apps (BE) |
| Hour 3–6 | Browse + filter page · Upvote endpoint |
| Hour 6–9 | Submit form · Leaderboard · Feedback |
| Hour 9–12 | UMD theme, polish, seed 8–10 demo apps |
| Hour 12–18 | Buffer, integration testing, demo prep |
| Hour 18–24 | Final fixes, pitch practice |

---

## 🔮 Future Roadmap (Post-Hackathon)

- GitHub OAuth for user accounts
- Email notifications when your app gets upvoted
- Featured listings for monetization
- Verified "built at UMD" badge system
- Expand to other University of Maryland System schools

---

## 👥 Team Split

| Person | Role | Owns |
|--------|------|------|
| Pranav | Frontend Lead | Home page, TrendingSection, AppCard, routing, UMD theme/styling |
| Saharsh| Frontend | Browse/search page, FilterSidebar, App detail, SubmitForm, Leaderboard page |
| David Ahn | Backend | FastAPI setup, all API endpoints, upvote logic, CORS config, frontend wiring |
| Aryan Sharma | Database | MongoDB Atlas setup, schema design, seed data, indexes, db.py connection module |

Fear the Turtle 🐢
