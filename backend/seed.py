# ============================================================
# seed.py — Load Demo Data Into the Database
#
#   1. Clears all existing data (safe reset)
#   2. Inserts 10 realistic UMD student apps
#   3. Inserts feedback comments on some of those apps
#
# HOW TO RUN:
#   cd backend
#   python3 seed.py


from datetime import datetime, timedelta
from db import apps_collection, feedback_collection, test_connection


# ==================== 10 DEMO APPS ====================

SEED_APPS = [
    {
        "name": "UMD Dining Hall Tracker",
        "description": "API and tracker for UMD dining hall info including menus, meal times, and locations for North Campus Diner, South Campus, Yahentamitsi, and 251 North.",
        "url": "https://github.com/Shivppatel/UMD-Dining-Hall-Tracker",
        "category_tags": ["Food & Dining"],
        "submitter_name": "Shiv Patel",
        "submitter_email": "spatel@umd.edu",
        "upvotes": 47,
        "collab_requests": 5,
        "created_at": datetime(2025, 9, 15),
    },
    {
        "name": "UMD.io",
        "description": "Open API for UMD data — courses, bus routes, buildings, professors, and majors. Built by students, for students. Powers dozens of campus apps.",
        "url": "https://github.com/umdio/umdio",
        "category_tags": ["Campus Transit", "Study"],
        "submitter_name": "UMD.io Team",
        "submitter_email": "team@umd.io",
        "upvotes": 104,
        "collab_requests": 12,
        "created_at": datetime(2024, 3, 10),
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
        "name": "Jupiterp",
        "description": "Course schedule planner for UMD students. Search courses, see professor reviews from PlanetTerp, and visualize your weekly schedule before registering.",
        "url": "https://github.com/atcupps/Jupiterp",
        "category_tags": ["Study"],
        "submitter_name": "Andrew Cupps",
        "submitter_email": "acupps@umd.edu",
        "upvotes": 55,
        "collab_requests": 6,
        "created_at": datetime(2025, 7, 10),
    },
    {
        "name": "PlanetTerp",
        "description": "Professor reviews, grade distributions for every UMD course, and tools to help Terps make informed decisions. The go-to resource during registration.",
        "url": "https://github.com/planetterp/PlanetTerp",
        "category_tags": ["Study", "Career"],
        "submitter_name": "PlanetTerp Team",
        "submitter_email": "team@planetterp.com",
        "upvotes": 71,
        "collab_requests": 8,
        "created_at": datetime(2024, 6, 5),
    },
    {
        "name": "UMD Degree Audit",
        "description": "iOS app that simulates the UMD degree audit system for CS majors. Track your progress through requirements offline without logging into Testudo.",
        "url": "https://github.com/raghavbhasin97/Degree-Audit-UMD",
        "category_tags": ["Study", "Career"],
        "submitter_name": "Raghav Bhasin",
        "submitter_email": "rbhasin@umd.edu",
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
        "url": "https://jupiterp.com",
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
        "url": "https://planetterp.com",
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
        "url": "https://umd.io",
        "category_tags": ["Career"],
        "submitter_name": "Rachel Torres",
        "submitter_email": "rtorres@umd.edu",
        "upvotes": 58,
        "collab_requests": 11,
        "created_at": datetime(2025, 7, 25),
    },
]


# ==================== SAMPLE FEEDBACK ====================

SEED_FEEDBACK = [
    {
        "app_name": "UMD Dining Hall Tracker",
        "feedback": [
            {
                "reviewer_name": "Sarah L.",
                "comment": "This saved me so many wasted walks to South Campus. The menu data is surprisingly up to date.",
                "rating": 5,
            },
            {
                "reviewer_name": "Jake M.",
                "comment": "Works great for checking menus. Would love to see crowd level data added too.",
                "rating": 4,
            },
        ],
    },
    {
        "app_name": "UMD.io",
        "feedback": [
            {
                "reviewer_name": "Emily R.",
                "comment": "This API powers like half the student apps on campus. The bus data endpoint is clutch.",
                "rating": 5,
            },
            {
                "reviewer_name": "Omar K.",
                "comment": "Documentation could be more detailed but the data itself is solid. Used it for my hackathon project.",
                "rating": 4,
            },
            {
                "reviewer_name": "Lisa T.",
                "comment": "Every CS student should know about this. Built my entire course planner on top of it.",
                "rating": 5,
            },
        ],
    },
    {
        "app_name": "PlanetTerp",
        "feedback": [
            {
                "reviewer_name": "Mike P.",
                "comment": "Used this every single registration period. The grade distributions completely changed how I pick professors.",
                "rating": 5,
            },
            {
                "reviewer_name": "Anna S.",
                "comment": "Clean design and the reviews feel honest. Way more useful than RateMyProfessor for UMD specifically.",
                "rating": 4,
            },
        ],
    },
    {
        "app_name": "Jupiterp",
        "feedback": [
            {
                "reviewer_name": "Derek W.",
                "comment": "The schedule visualizer is a game changer. Seeing my weekly layout before registering saved me from a terrible semester.",
                "rating": 5,
            },
            {
                "reviewer_name": "Nina K.",
                "comment": "Love that it pulls PlanetTerp reviews right into the course search. Two tools in one.",
                "rating": 5,
            },
        ],
    },
    {
        "app_name": "UMD Degree Audit",
        "feedback": [
            {
                "reviewer_name": "James R.",
                "comment": "Nice to check my degree progress without having to log into Testudo every time. Works offline too.",
                "rating": 4,
            },
        ],
    },
    {
        "app_name": "CampusCash",
        "feedback": [
            {
                "reviewer_name": "Priya S.",
                "comment": "The roommate expense splitting is exactly what we needed. No more awkward Venmo request chains.",
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
                "app_id": str(app_id),
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