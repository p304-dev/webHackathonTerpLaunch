#Create database indexes for TerpLaunch

from pymongo import ASCENDING, DESCENDING, TEXT
from db import apps_collection, feedback_collection, test_connection


def create_indexes():
    """Create all indexes needed for TerpLaunch."""

    # First, verify we can actually connect
    if not test_connection():
        print("\n⛔ Aborting — can't connect to database.")
        return

    print("\n📊 Creating indexes...\n")

    # ---- APPS COLLECTION ----

    # Index 1: Text search on name + description
    # This powers the search bar on the Browse page
    # Without it, searching "shuttle tracker" would be painfully slow
    apps_collection.create_index(
        [("name", TEXT), ("description", TEXT)],
        name="text_search"
    )
    print("  ✅ apps: text search index (name + description)")

    # Index 2: Category tags
    # This powers the filter sidebar (e.g., show only "Study" apps)
    apps_collection.create_index(
        [("category_tags", ASCENDING)],
        name="category_filter"
    )
    print("  ✅ apps: category_tags index")

    # Index 3: Upvotes descending
    # This powers trending (most upvoted first) and leaderboard
    apps_collection.create_index(
        [("upvotes", DESCENDING)],
        name="upvotes_sort"
    )
    print("  ✅ apps: upvotes descending index")

    # Index 4: Created_at descending
    # This powers "newest first" sorting on the browse page
    apps_collection.create_index(
        [("created_at", DESCENDING)],
        name="newest_first"
    )
    print("  ✅ apps: created_at descending index")

    # Index 5: Submitter name
    # This speeds up the leaderboard aggregation query
    apps_collection.create_index(
        [("submitter_name", ASCENDING)],
        name="submitter_lookup"
    )
    print("  ✅ apps: submitter_name index")

    # ---- FEEDBACK COLLECTION ----

    # Index 6: app_id
    # When someone opens an app's page, we need to fetch all feedback
    # for that specific app. This index makes that query fast.
    feedback_collection.create_index(
        [("app_id", ASCENDING)],
        name="feedback_by_app"
    )
    print("  ✅ feedback: app_id index")

    # Index 7: Created_at descending
    # Show newest feedback first
    feedback_collection.create_index(
        [("created_at", DESCENDING)],
        name="feedback_newest"
    )
    print("  ✅ feedback: created_at descending index")

    # ---- VERIFY ----
    print("\n✅ All indexes created!\n")

    print("--- apps indexes ---")
    for idx in apps_collection.list_indexes():
        print(f"  {idx['name']}: {dict(idx['key'])}")

    print("\n--- feedback indexes ---")
    for idx in feedback_collection.list_indexes():
        print(f"  {idx['name']}: {dict(idx['key'])}")


if __name__ == "__main__":
    create_indexes()
