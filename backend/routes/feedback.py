from fastapi import APIRouter, HTTPException
from bson import ObjectId
from datetime import datetime

from db import apps_collection, feedback_collection
from models.schemas import FeedbackSubmit

router = APIRouter(prefix="/apps", tags=["Feedback"])


def feedback_to_response(doc) -> dict:
    return {
        "id": str(doc["_id"]),
        "app_id": str(doc["app_id"]),
        "reviewer_name": doc["reviewer_name"],
        "comment": doc["comment"],
        "rating": doc["rating"],
        "created_at": doc.get("created_at", datetime.utcnow()),
    }


@router.get("/{app_id}/feedback")
def get_feedback(app_id: str):
    try:
        oid = ObjectId(app_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid app ID format")

    docs = feedback_collection.find({"app_id": oid}).sort("created_at", -1)
    return [feedback_to_response(doc) for doc in docs]


@router.post("/{app_id}/feedback", status_code=201)
def submit_feedback(app_id: str, feedback: FeedbackSubmit):
    try:
        oid = ObjectId(app_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid app ID format")

    if not apps_collection.find_one({"_id": oid}):
        raise HTTPException(status_code=404, detail="App not found")

    doc = {
        "app_id": oid,
        "reviewer_name": feedback.reviewer_name,
        "comment": feedback.comment,
        "rating": feedback.rating,
        "created_at": datetime.utcnow(),
    }
    result = feedback_collection.insert_one(doc)
    doc["_id"] = result.inserted_id

    return feedback_to_response(doc)
