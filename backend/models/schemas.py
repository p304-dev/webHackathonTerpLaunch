# ============================================================
# schemas.py — Data Shapes (Pydantic Models)
# Database
#
#   Defines the exact structure of data going INTO and OUT OF the API.
#   FastAPI uses these to:
#     - Validate incoming requests (reject bad data automatically)
#     - Generate the /docs page with correct field descriptions
#     - Serialize responses to JSON

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# -------------------- APPS --------------------

class AppSubmit(BaseModel):
    """
    What the frontend sends when a student submits a new app.
    This is the REQUEST body for POST /apps.
    """
    name: str = Field(
        ...,                    # ... means "required"
        max_length=100,
        description="Name of the app",
        json_schema_extra={"example": "ShuttleTerp"}
    )
    description: str = Field(
        ...,
        max_length=280,
        description="Short description (like a tweet)",
        json_schema_extra={"example": "Live GPS tracking for UMD shuttle buses"}
    )
    url: str = Field(
        ...,
        description="Link to live app or GitHub repo",
        json_schema_extra={"example": "https://github.com/example/shuttleterp"}
    )
    category_tags: List[str] = Field(
        ...,
        description="One or more category tags",
        json_schema_extra={"example": ["Campus Transit"]}
    )
    submitter_name: str = Field(
        ...,
        max_length=100,
        description="Developer's name",
        json_schema_extra={"example": "Priya Patel"}
    )
    submitter_email: str = Field(
        ...,
        max_length=200,
        description="Developer's contact email",
        json_schema_extra={"example": "ppatel@umd.edu"}
    )


class AppResponse(BaseModel):
    """
    What the API sends BACK to the frontend for each app.
    This is the RESPONSE shape for GET /apps and GET /apps/:id.
    
    Notice: submitter_email is NOT included here — we don't
    expose emails publicly. Only submitter_name is shown.
    """
    id: str
    name: str
    description: str
    url: str
    category_tags: List[str]
    submitter_name: str
    upvotes: int
    collab_requests: int
    created_at: datetime


# -------------------- FEEDBACK --------------------

class FeedbackSubmit(BaseModel):
    """
    What the frontend sends when someone leaves feedback on an app.
    REQUEST body for POST /apps/:id/feedback.
    """
    reviewer_name: str = Field(
        ...,
        max_length=100,
        json_schema_extra={"example": "Sarah L."}
    )
    comment: str = Field(
        ...,
        max_length=1000,
        json_schema_extra={"example": "This saved me so many wasted walks to South Campus."}
    )
    rating: int = Field(
        ...,
        ge=1,           # ge = greater than or equal to (minimum 1)
        le=5,           # le = less than or equal to (maximum 5)
        description="Star rating from 1 to 5",
        json_schema_extra={"example": 4}
    )


class FeedbackResponse(BaseModel):
    """
    What the API sends back for each feedback entry.
    RESPONSE shape for GET /apps/:id/feedback.
    """
    id: str
    app_id: str
    reviewer_name: str
    comment: str
    rating: int
    created_at: datetime


# -------------------- LEADERBOARD --------------------

class LeaderboardEntry(BaseModel):
    """
    One row in the developer leaderboard.
    RESPONSE shape for GET /leaderboard.
    """
    submitter_name: str
    total_upvotes: int
    app_count: int


# -------------------- VALID CATEGORIES --------------------
# These are the only allowed values for category_tags.
# UMD-specific problem categories that make discovery feel native.

VALID_CATEGORIES = [
    "Study",
    "Food & Dining",
    "Housing",
    "Campus Transit",
    "Health & Wellness",
    "Social",
    "Finance",
    "Career",
    "Other",
]
