from fastapi import APIRouter

from db import apps_collection

router = APIRouter(tags=["Leaderboard"])


@router.get("/leaderboard")
def get_leaderboard():
    pipeline = [
        {"$group": {
            "_id": "$submitter_name",
            "total_upvotes": {"$sum": "$upvotes"},
            "app_count": {"$sum": 1}
        }},
        {"$sort": {"total_upvotes": -1}},
        {"$limit": 10}
    ]
    results = apps_collection.aggregate(pipeline)
    return [
        {
            "submitter_name": r["_id"],
            "total_upvotes": r["total_upvotes"],
            "app_count": r["app_count"],
        }
        for r in results
    ]
