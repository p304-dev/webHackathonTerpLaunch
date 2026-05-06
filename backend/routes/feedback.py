# ============================================================
# routes/feedback.py — Feedback Endpoints
# Owner: Pranav (Backend)
#
# TODO (Pranav):
#   GET  /apps/{id}/feedback  — get all feedback for an app
#   POST /apps/{id}/feedback  — submit feedback on an app
#
# Use the same pattern as apps.py. Import from:
#   from db import feedback_collection
#   from models.schemas import FeedbackSubmit, FeedbackResponse
# ============================================================

from fastapi import APIRouter

router = APIRouter(tags=["Feedback"])

# Pranav: build your endpoints here
