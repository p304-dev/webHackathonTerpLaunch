# ============================================================
# routes/leaderboard.py — Leaderboard Endpoint
# Owner: Pranav (Backend)
#
# TODO (Pranav):
#   GET /leaderboard — top developers ranked by total upvotes
#
# HINT: Use MongoDB aggregation pipeline:
#   pipeline = [
#       {"$group": {
#           "_id": "$submitter_name",
#           "total_upvotes": {"$sum": "$upvotes"},
#           "app_count": {"$sum": 1}
#       }},
#       {"$sort": {"total_upvotes": -1}},
#       {"$limit": 10}
#   ]
#   results = apps_collection.aggregate(pipeline)
# ============================================================

from fastapi import APIRouter

router = APIRouter(tags=["Leaderboard"])

# Pranav: build your endpoint here
