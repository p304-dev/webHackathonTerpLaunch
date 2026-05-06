# ============================================================
# main.py — FastAPI Entry Point
#
#backend
# HOW TO RUN:
#   cd backend
#   uvicorn main:app --reload
#   → Server starts at http://localhost:8000
#   → API docs at http://localhost:8000/docs
#


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import test_connection

# Test database connection when the server starts
test_connection()

# Create the FastAPI app
app = FastAPI(
    title="TerpLaunch API",
    description="Student app showcase platform for UMD 🐢",
    version="1.0.0",
)

# ---- CORS MIDDLEWARE ----
# CORS = Cross-Origin Resource Sharing
# 
# Without this, the React frontend (running on localhost:5173)
# CANNOT make API calls to the backend (running on localhost:8000).
# The browser blocks it as a security measure.
#
# This middleware tells the browser: "it's okay, let the frontend talk to me."
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Allow ALL origins (fine for hackathon)
    allow_credentials=True,
    allow_methods=["*"],        # Allow GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],        # Allow all headers
)


# ---- HEALTH CHECK ----
# Simple endpoint to verify the server is running
@app.get("/")
def root():
    return {
        "message": "TerpLaunch API is running 🐢",
        "docs": "Go to /docs to see all endpoints",
    }


# ---- REGISTER ROUTES ----
# Import the route files and attach them to the app
# Each route file handles a group of related endpoints

from routes.apps import router as apps_router
app.include_router(apps_router)

# Backend person: uncomment these as you build each route file:
# from routes.feedback import router as feedback_router
# from routes.leaderboard import router as leaderboard_router
# app.include_router(feedback_router)
# app.include_router(leaderboard_router)
