# ============================================================
# routes/apps.py — App CRUD Endpoints
# Owner: Pranav (Backend), starter code by Aryan
#
# ENDPOINTS:
#   GET    /apps              — list all apps (with search + filter)
#   POST   /apps              — submit a new app
#   GET    /apps/{id}         — get one app's details
#   POST   /apps/{id}/upvote  — upvote an app
#   POST   /apps/{id}/collab  — express collaboration interest
#   GET    /apps/discover/trending — top 5 most upvoted apps
# ============================================================

from fastapi import APIRouter, HTTPException, Query
from bson import ObjectId
from datetime import datetime
from typing import Optional

from db import apps_collection
from models.schemas import AppSubmit, AppResponse, VALID_CATEGORIES

# Create a router — this groups all /apps endpoints together
# The prefix="/apps" means all routes below start with /apps
router = APIRouter(prefix="/apps", tags=["Apps"])


# ---- HELPER FUNCTION ----
def app_to_response(doc) -> dict:
    """
    Convert a raw MongoDB document into a clean JSON-friendly dict.
    
    Why we need this:
      MongoDB stores IDs as ObjectId("abc123...") which isn't JSON serializable.
      We convert it to a plain string.
      We also exclude submitter_email from the response (privacy).
    """
    return {
        "id": str(doc["_id"]),
        "name": doc["name"],
        "description": doc["description"],
        "url": doc["url"],
        "category_tags": doc["category_tags"],
        "submitter_name": doc["submitter_name"],
        "upvotes": doc.get("upvotes", 0),
        "collab_requests": doc.get("collab_requests", 0),
        "created_at": doc.get("created_at", datetime.utcnow()),
    }


# ---- GET /apps/discover/trending ----
# IMPORTANT: This must be ABOVE /{app_id} or FastAPI thinks
# "discover" is an app_id and tries to look it up in MongoDB
@router.get("/discover/trending")
def trending_apps():
    """Get the top 5 most upvoted apps (for the trending section on the home page)."""
    cursor = apps_collection.find().sort("upvotes", -1).limit(5)
    return [app_to_response(doc) for doc in cursor]


# ---- GET /apps ----
@router.get("/")
def list_apps(
    category: Optional[str] = Query(None, description="Filter by category tag"),
    search: Optional[str] = Query(None, description="Search name and description"),
):
    """
    List all apps. Supports optional filtering:
      GET /apps                     → all apps, sorted by most upvoted
      GET /apps?category=Study      → only Study apps
      GET /apps?search=shuttle      → apps matching "shuttle"
      GET /apps?category=Study&search=grade → both filters at once
    """
    query = {}

    # If category was provided, filter by it
    if category:
        query["category_tags"] = category

    # If search was provided, use MongoDB's text search
    # This searches the name and description fields (thanks to our text index)
    if search:
        query["$text"] = {"$search": search}

    # Find matching documents, sorted by most upvoted, max 50 results
    cursor = apps_collection.find(query).sort("upvotes", -1).limit(50)
    return [app_to_response(doc) for doc in cursor]


# ---- POST /apps ----
@router.post("/", status_code=201)
def create_app(app: AppSubmit):
    """
    Submit a new app to TerpLaunch.
    
    The request body must match AppSubmit schema (see schemas.py).
    FastAPI validates this automatically — if fields are missing or
    the wrong type, it returns a 422 error without us writing any code.
    """
    # Validate that all category tags are from our allowed list
    for tag in app.category_tags:
        if tag not in VALID_CATEGORIES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid category '{tag}'. Must be one of: {VALID_CATEGORIES}",
            )

    # Build the document to insert
    doc = {
        **app.dict(),           # spread all fields from the request
        "upvotes": 0,           # new apps start with 0 upvotes
        "collab_requests": 0,   # and 0 collab requests
        "created_at": datetime.utcnow(),
    }

    # Insert into MongoDB
    result = apps_collection.insert_one(doc)
    doc["_id"] = result.inserted_id

    return app_to_response(doc)


# ---- GET /apps/{id} ----
@router.get("/{app_id}")
def get_app(app_id: str):
    """Get a single app by its ID."""
    try:
        doc = apps_collection.find_one({"_id": ObjectId(app_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid app ID format")

    if not doc:
        raise HTTPException(status_code=404, detail="App not found")

    return app_to_response(doc)


# ---- POST /apps/{id}/upvote ----
@router.post("/{app_id}/upvote")
def upvote_app(app_id: str):
    """
    Upvote an app. Increments the upvote count by 1.
    
    Uses MongoDB's $inc operator which is atomic — even if two people
    upvote at the exact same millisecond, both votes count.
    """
    try:
        result = apps_collection.update_one(
            {"_id": ObjectId(app_id)},       # find this app
            {"$inc": {"upvotes": 1}},        # increment upvotes by 1
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid app ID format")

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="App not found")

    # Return the updated app
    updated = apps_collection.find_one({"_id": ObjectId(app_id)})
    return app_to_response(updated)


# ---- POST /apps/{id}/collab ----
@router.post("/{app_id}/collab")
def collab_request(app_id: str):
    """Register collaboration interest on an app."""
    try:
        result = apps_collection.update_one(
            {"_id": ObjectId(app_id)},
            {"$inc": {"collab_requests": 1}},
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid app ID format")

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="App not found")

    return {"message": "Collaboration interest registered! 🤝"}
