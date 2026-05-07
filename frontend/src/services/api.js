const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"

export const getTrending = async () => {
  const res = await fetch(`${BASE_URL}/trending`)
  return res.json()
}

export const getAllApps = async (category = "", search = "") => {
  const params = new URLSearchParams()
  if (category) params.append('category', category)
  if (search) params.append('search', search)
  const res = await fetch(`${BASE_URL}/apps?${params}`)
  return res.json()
}

export const upvoteApp = async (id) => {
  const res = await fetch(`${BASE_URL}/apps/${id}/upvote`, { method: "POST" })
  return res.json()
}

export const getAppById = async (id) => {
  const res = await fetch(`${BASE_URL}/apps/${id}`)
  return res.json()
}

export const getLeaderboard = async () => {
  const res = await fetch(`${BASE_URL}/leaderboard`)
  return res.json()
}
