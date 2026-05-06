# ============================================================
# db.py — MongoDB Connection Module
# Database
# 
#   1. Reads MONGO_URI from the .env file
#   2. Connects to MongoDB Atlas
#   3. Exports "db", "apps_collection", and "feedback_collection"
#      so other files can do: from db import apps_collection
#

import os
from dotenv import load_dotenv
from pymongo import MongoClient

# This line reads the .env file and loads MONGO_URI into the environment
load_dotenv()

# Get the connection string
MONGO_URI = os.getenv("MONGO_URI")

# If .env is missing or empty, crash immediately with a helpful message
if not MONGO_URI:
    raise ValueError(
        "\n MONGO_URI not found!\n"
        "Make sure you have a file called .env in the backend/ folder\n"
        "with this line (using your real password):\n"
        "MONGO_URI=mongodb+srv://terpLaunchAdmin:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/terpLaunch?retryWrites=true&w=majority\n"
    )

# Connect to MongoDB Atlas
# MongoClient handles connection pooling automatically
client = MongoClient(MONGO_URI)

# Select the "terpLaunch" database
db = client["terpLaunch"]

# Shortcuts to the two collections
# Other files import these directly:
#   from db import apps_collection
#   apps_collection.find({})  ← queries the "apps" collection
apps_collection = db["apps"]
feedback_collection = db["feedback"]


def test_connection():
    """
    Quick test — sends a "ping" to MongoDB to verify the connection works.
    Run this file directly to test: python db.py
    """
    try:
        client.admin.command("ping")
        print("Connected to MongoDB Atlas successfully!")
        print(f"   Database: {db.name}")
        print(f"   Collections: {db.list_collection_names()}")
        return True
    except Exception as e:
        print(f" Failed to connect to MongoDB: {e}")
        print("\nCommon fixes:")
        print("  1. Check your password in .env — no < > brackets around it")
        print("  2. Check Network Access in Atlas — 0.0.0.0/0 should be whitelisted")
        print("  3. Check your internet connection")
        return False


# This block only runs when you do "python db.py" directly
# It does NOT run when other files do "from db import apps_collection"
if __name__ == "__main__":
    test_connection()
