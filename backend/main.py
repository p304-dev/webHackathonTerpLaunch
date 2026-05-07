from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime, timezone
 
from db import apps_collection, feedback_collection, test_connection

app = FastAPI(
    title="TerpLaunch API",
    description="Student app showcase platform for UMD 🐢",
    version="1.0.0",
)
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
def serialize_app(app: dict) -> dict:
    """Convert MongoDB ObjectId to string so it can be returned as JSON."""
    app["id"] = str(app["_id"])
    del app["_id"]
    return app
 
def serialize_feedback(fb: dict) -> dict:
    fb["id"] = str(fb["_id"])
    fb["app_id"] = str(fb["app_id"])
    del fb["_id"]
    return fb
 
def to_object_id(id: str) -> ObjectId:
    """Parse a string into a MongoDB ObjectId. Raises 400 if format is invalid."""
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ID format")
 
 
class AppSubmission(BaseModel):
    name: str
    description: str          
    url: str                  
    category_tags: List[str]  
    submitter_name: str
    submitter_email: str
 
class FeedbackSubmission(BaseModel):
    reviewer_name: str
    comment: str
    rating: int               

 
@app.get("/apps")
async def get_apps(category: str | None = None, search: str | None = None):
    appList = list(apps_collection.find())
 
    filterApps = []
    for app in appList:
        if category != None:
            allTags = app.get("category_tags", [])
            for curTag in allTags:
                if curTag.lower() == category.lower():
                    filterApps.append(app)
                    break
        else:
            filterApps.append(app)
 
    results = []
    for fApps in filterApps:
        if search:
            if search.lower() in (fApps.get("name").lower()) or search.lower() in (fApps.get("description".lower())):
                results.append(fApps)
        else:
            results.append(fApps)
 
    # Sort by upvotes, highest first
    for i in range(len(results)):
        for j in range(i + 1, len(results)):
            if results[j].get("upvotes", 0) > results[i].get("upvotes", 0):
                results[i], results[j] = results[j], results[i]
 
    serialized = []
    for app in results:
        serialized.append(serialize_app(app))
 
    return serialized
 
 
@app.post("/apps", status_code=201)
async def submit_app(app: AppSubmission):
    """Submit a new app. Upvotes and collab_requests start at 0."""
    new_app = app.model_dump()
    new_app["upvotes"] = 0
    new_app["collab_requests"] = 0
    new_app["created_at"] = datetime.now(timezone.utc)
 
    result = apps_collection.insert_one(new_app)
    return {"message": "App submitted successfully!", "id": str(result.inserted_id)}
 
 
@app.get("/apps/{app_id}")
async def get_app(app_id: str):
    """Get a single app by its MongoDB ID."""
    app = apps_collection.find_one({"_id": to_object_id(app_id)})
    if not app:
        raise HTTPException(status_code=404, detail="App not found")
    return serialize_app(app)
 
 
@app.post("/apps/{app_id}/upvote")
async def upvote_app(app_id: str):
    """Increment upvote count by 1. Returns the new total."""
    app = apps_collection.find_one({"_id": to_object_id(app_id)})
    if not app:
        raise HTTPException(status_code=404, detail="App not found")
 
    new_upvotes = app.get("upvotes", 0) + 1
    apps_collection.update_one({"_id": app["_id"]}, {"$set": {"upvotes": new_upvotes}})
 
    return {"message": "Upvoted!", "upvotes": new_upvotes}
 
 
@app.post("/apps/{app_id}/collab")
async def request_collab(app_id: str):
    """Register collaboration interest. Increments collab_requests by 1."""
    app = apps_collection.find_one({"_id": to_object_id(app_id)})
    if not app:
        raise HTTPException(status_code=404, detail="App not found")
 
    new_count = app.get("collab_requests", 0) + 1
    apps_collection.update_one({"_id": app["_id"]}, {"$set": {"collab_requests": new_count}})
 
    return {"message": "Collaboration interest registered!", "collab_requests": new_count}
 
 
@app.get("/apps/{app_id}/feedback")
async def get_feedback(app_id: str):
    """Get all feedback for an app, newest first."""
    obj_id = to_object_id(app_id)
 
    if not apps_collection.find_one({"_id": obj_id}):
        raise HTTPException(status_code=404, detail="App not found")
 
    all_feedback = list(feedback_collection.find())
 
    # Filter to only feedback belonging to this app
    app_feedback = []
    for fb in all_feedback:
        if fb.get("app_id") == obj_id:
            app_feedback.append(fb)
 
    # Sort by created_at, newest first
    for i in range(len(app_feedback)):
        for j in range(i + 1, len(app_feedback)):
            if app_feedback[j].get("created_at", datetime.min) > app_feedback[i].get("created_at", datetime.min):
                app_feedback[i], app_feedback[j] = app_feedback[j], app_feedback[i]
 
    serialized = []
    for fb in app_feedback:
        serialized.append(serialize_feedback(fb))
 
    return serialized
 
 
@app.post("/apps/{app_id}/feedback", status_code=201)
async def submit_feedback(app_id: str, feedback: FeedbackSubmission):
    """Submit a star rating + comment for an app."""
    if not (1 <= feedback.rating <= 5):
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
 
    obj_id = to_object_id(app_id)
 
    if not apps_collection.find_one({"_id": obj_id}):
        raise HTTPException(status_code=404, detail="App not found")
 
    new_feedback = feedback.model_dump()
    new_feedback["app_id"] = obj_id
    new_feedback["created_at"] = datetime.now(timezone.utc)
 
    result = feedback_collection.insert_one(new_feedback)
    return {"message": "Feedback submitted!", "id": str(result.inserted_id)}
 
 
@app.get("/leaderboard")
async def get_leaderboard():
    """
    Top 10 developers ranked by total upvotes across all their apps.
    Grouped and sorted in plain Python.
    """
    all_apps = list(apps_collection.find())
 
    totals = {}
    for app in all_apps:
        name = app.get("submitter_name", "Unknown")
        if name not in totals:
            totals[name] = {
                "submitter_name": name,
                "submitter_email": app.get("submitter_email", ""),
                "total_upvotes": 0,
                "app_count": 0,
            }
        totals[name]["total_upvotes"] += app.get("upvotes", 0)
        totals[name]["app_count"] += 1
 
    ranked_list = list(totals.values())
    for i in range(len(ranked_list)):
        for j in range(i + 1, len(ranked_list)):
            if ranked_list[j]["total_upvotes"] > ranked_list[i]["total_upvotes"]:
                ranked_list[i], ranked_list[j] = ranked_list[j], ranked_list[i]
 
    result = []
    for i in range(min(10, len(ranked_list))):
        entry = ranked_list[i]
        entry["rank"] = i + 1
        result.append(entry)
 
    return result
 
 
@app.get("/trending")
async def get_trending():
    """
    Top 5 most upvoted apps submitted this month.
    Falls back to all-time top 5 if no apps exist this month yet.
    """
    now = datetime.now(timezone.utc)
    all_apps = list(apps_collection.find())
 
    this_month = []
    for app in all_apps:
        created_at = app.get("created_at")
        if created_at and created_at.year == now.year and created_at.month == now.month:
            this_month.append(app)
 
    if len(this_month) >= 5:
        pool = this_month
    else:
        seen_ids = {app["_id"] for app in this_month}
        extras = [app for app in all_apps if app["_id"] not in seen_ids]
        pool = this_month + extras
 
    for i in range(len(pool)):
        for j in range(i + 1, len(pool)):
            if pool[j].get("upvotes", 0) > pool[i].get("upvotes", 0):
                pool[i], pool[j] = pool[j], pool[i]
 
    trending = []
    for i in range(min(5, len(pool))):
        trending.append(pool[i])
 
    serialized = []
    for app in trending:
        serialized.append(serialize_app(app))
 
    return serialized