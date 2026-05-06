# ============================================================
# seed.py — Load Demo Data Into the Database
#
#   1. Clears all existing data (safe reset)
#   2. Inserts 10 realistic UMD student apps
#   3. Inserts 8 feedback comments on some of those apps
#
# HOW TO RUN:
#   cd backend
#   python seed.py


from datetime import datetime, timedelta
from db import apps_collection, feedback_collection, test_connection


# ==================== 10 DEMO APPS ====================
# These are realistic UMD student-built app ideas
# Each has: name, description (≤280 chars), url, categories,
#           submitter info, upvotes, collab_requests, created_at

SEED_APPS = [
    {
        "name": "TerpDining",
        "description": "Real-time dining hall menus and crowd levels across all UMD dining facilities. Never walk into a packed South Campus Dining Hall again.",
        "url": "https://github.com/terp-dev/terpdining",
        "category_tags": ["Food & Dining"],
        "submitter_name": "Marcus Chen",
        "submitter_email": "mchen@umd.edu",
        "upvotes": 47,
        "collab_requests": 5,
        "created_at": datetime(2025, 9, 15),
    },
    {
        "name": "ShuttleTerp",
        "description": "Live GPS tracking for UMD shuttle buses with arrival predictions. Know exactly when the 104 is coming instead of standing in the rain.",
        "url": "https://github.com/terp-dev/shuttleterp",
        "category_tags": ["Campus Transit"],
        "submitter_name": "Priya Patel",
        "submitter_email": "ppatel@umd.edu",
        "upvotes": 62,
        "collab_requests": 8,
        "created_at": datetime(2025, 8, 20),
    },
    {
        "name": "TerpHousing",
        "description": "Student-reviewed off-campus housing listings around College Park. Filter by price, distance to campus, and actual student ratings.",
        "url": "https://terphousing.vercel.app",
        "category_tags": ["Housing"],
        "submitter_name": "David Kim",
        "submitter_email": "dkim@umd.edu",
        "upvotes": 38,
        "collab_requests": 3,
        "created_at": datetime(2025, 10, 1),
    },
    {
        "name": "StudySpot",
        "description": "Find open study spaces on campus right now. Real-time occupancy data for McKeldin, STEM, and ESJ libraries plus lesser-known quiet spots.",
        "url": "https://github.com/terp-dev/studyspot",
        "category_tags": ["Study"],
        "submitter_name": "Aaliyah Johnson",
        "submitter_email": "ajohnson@umd.edu",
        "upvotes": 55,
        "collab_requests": 6,
        "created_at": datetime(2025, 7, 10),
    },
    {
        "name": "GradeDistro",
        "description": "Historical grade distributions for every UMD course and professor. Make smarter schedule decisions with real data from PlanetTerp.",
        "url": "https://gradedistro.app",
        "category_tags": ["Study", "Career"],
        "submitter_name": "Tyler Brooks",
        "submitter_email": "tbrooks@umd.edu",
        "upvotes": 71,
        "collab_requests": 2,
        "created_at": datetime(2025, 6, 5),
    },
    {
        "name": "TerpFit",
        "description": "Eppley Rec Center crowd tracker and workout buddy matcher. See gym capacity in real-time and find people training at your level.",
        "url": "https://github.com/terp-dev/terpfit",
        "category_tags": ["Health & Wellness", "Social"],
        "submitter_name": "Jordan Rivera",
        "submitter_email": "jrivera@umd.edu",
        "upvotes": 29,
        "collab_requests": 4,
        "created_at": datetime(2025, 11, 12),
    },
    {
        "name": "CampusCash",
        "description": "Split expenses with roommates, track dining dollars balance, and find student discounts around College Park. Venmo meets campus life.",
        "url": "https://campuscash.dev",
        "category_tags": ["Finance"],
        "submitter_name": "Saharsh Mehta",
        "submitter_email": "smehta@umd.edu",
        "upvotes": 33,
        "collab_requests": 7,
        "created_at": datetime(2025, 10, 20),
    },
    {
        "name": "TerpConnect",
        "description": "Match with other UMD students by major, interests, and career goals. Networking app built specifically for Terps, not another generic LinkedIn.",
        "url": "https://terpconnect.vercel.app",
        "category_tags": ["Social", "Career"],
        "submitter_name": "Amara Okafor",
        "submitter_email": "aokafor@umd.edu",
        "upvotes": 44,
        "collab_requests": 9,
        "created_at": datetime(2025, 9, 1),
    },
    {
        "name": "ParkTerp",
        "description": "Real-time parking availability across all UMD lots and garages. Get alerts when your lot opens up and never circle Lot 1 again.",
        "url": "https://github.com/terp-dev/parkterp",
        "category_tags": ["Campus Transit"],
        "submitter_name": "Chris Nguyen",
        "submitter_email": "cnguyen@umd.edu",
        "upvotes": 51,
        "collab_requests": 3,
        "created_at": datetime(2025, 8, 15),
    },
    {
        "name": "TerpIntern",
        "description": "Aggregated internship postings relevant to UMD students with salary data, interview tips from Terps who got the offer, and deadline reminders.",
        "url": "https://terpintern.app",
        "category_tags": ["Career"],
        "submitter_name": "Rachel Torres",
        "submitter_email": "rtorres@umd.edu",
        "upvotes": 58,
        "collab_requests": 11,
        "created_at": datetime(2025, 7, 25),
    },
]


# ==================== SAMPLE FEEDBACK ====================
# Feedback on some of the apps above. We'll link them by app_id
# after inserting the apps.

SEED_FEEDBACK = [
    {
        "app_name": "TerpDining",  # used to look up the app_id
        "feedback": [
            {
                "reviewer_name": "Sarah L.",
                "comment": "This saved me so many wasted walks to South Campus. The crowd data is surprisingly accurate.",
                "rating": 5,
            },
            {
                "reviewer_name": "Jake M.",
                "comment": "Works great but would love to see nutritional info for each meal.",
                "rating": 4,
            },
        ],
    },
    {
        "app_name": "ShuttleTerp",
        "feedback": [
            {
                "reviewer_name": "Emily R.",
                "comment": "Way better than the official TransLoc app. Actually shows where the bus is.",
                "rating": 5,
            },
            {
                "reviewer_name": "Omar K.",
                "comment": "The 104 predictions are off during rush hour but otherwise solid.",
                "rating": 3,
            },
            {
                "reviewer_name": "Lisa T.",
                "comment": "Finally someone built this properly. Using it every day.",
                "rating": 5,
            },
        ],
    },
    {
        "app_name": "GradeDistro",
        "feedback": [
            {
                "reviewer_name": "Mike P.",
                "comment": "Helped me pick professors for spring registration. The grade curves are eye-opening.",
                "rating": 5,
            },
            {
                "reviewer_name": "Anna S.",
                "comment": "Clean design and the data is all sourced properly from PlanetTerp.",
                "rating": 4,
            },
        ],
    },
    {
        "app_name": "StudySpot",
        "feedback": [
            {
                "reviewer_name": "Derek W.",
                "comment": "Found a quiet spot in ESJ I never knew existed. This app is underrated.",
                "rating": 5,
            },
        ],
    },
]


def seed_database():
    """Clear everything and insert fresh demo data."""

    # Step 0: Check connection
    print("=" * 50)
    print("  TerpLaunch Database Seeder")
    print("=" * 50)
    print()

    if not test_connection():
        print("\n⛔ Aborting — can't connect to database.")
        return

    # Step 1: Clear existing data
    print("\n🗑️  Clearing existing data...")
    apps_collection.delete_many({})
    feedback_collection.delete_many({})
    print("   Done — both collections are empty now.")

    # Step 2: Insert apps
    print("\n📱 Inserting apps...")
    result = apps_collection.insert_many(SEED_APPS)
    inserted_ids = result.inserted_ids
    print(f"   Inserted {len(inserted_ids)} apps")

    # Step 3: Build a lookup so we can link feedback to apps
    # name_to_id maps "TerpDining" → ObjectId("abc123...")
    name_to_id = {}
    for app_data, obj_id in zip(SEED_APPS, inserted_ids):
        name_to_id[app_data["name"]] = obj_id

    # Step 4: Insert feedback with correct app_id references
    print("\n💬 Inserting feedback...")
    feedback_count = 0
    for group in SEED_FEEDBACK:
        app_id = name_to_id.get(group["app_name"])
        if not app_id:
            print(f"   ⚠️  Skipping feedback for '{group['app_name']}' — app not found")
            continue

        for fb in group["feedback"]:
            feedback_collection.insert_one({
                "app_id": str(app_id),      # stored as string for easy JSON serialization
                "reviewer_name": fb["reviewer_name"],
                "comment": fb["comment"],
                "rating": fb["rating"],
                "created_at": datetime.utcnow() - timedelta(days=feedback_count),
            })
            feedback_count += 1

    print(f"   Inserted {feedback_count} feedback entries")

    # Step 5: Print summary
    print("\n" + "=" * 50)
    print("  ✅ DATABASE SEEDED SUCCESSFULLY")
    print("=" * 50)

    print(f"\n  Total apps:     {apps_collection.count_documents({})}")
    print(f"  Total feedback: {feedback_collection.count_documents({})}")

    print("\n  🏆 Top 5 by upvotes:")
    for app in apps_collection.find().sort("upvotes", -1).limit(5):
        print(f"     {app['upvotes']:>3}⬆  {app['name']}")

    print("\n  📂 Categories represented:")
    pipeline = [
        {"$unwind": "$category_tags"},
        {"$group": {"_id": "$category_tags", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
    ]
    for cat in apps_collection.aggregate(pipeline):
        print(f"     {cat['_id']}: {cat['count']} app(s)")

    print()


if __name__ == "__main__":
    seed_database()
