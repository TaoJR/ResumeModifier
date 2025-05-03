# scripts/update_and_clean_jobs.py

from datetime import datetime, timedelta
from app.database import collection
from app.job_api import fetch_and_store_jobs

def remove_expired_jobs(days=30):
    threshold = datetime.utcnow() - timedelta(days=days)
    result = collection.delete_many({
        "posted_at": {"$lt": threshold.isoformat()}
    })
    print(f"🧹 Deleted {result.deleted_count} expired jobs older than {days} days.")

def update_jobs():
    print("🚀 Starting scheduled job update...")
    keywords = [
        "software engineer", "backend developer", "frontend developer",
        "data scientist", "java developer", "python developer"
    ]
    for keyword in keywords:
        fetch_and_store_jobs(query=keyword, max_pages=2)
    print("✅ Update complete.")

if __name__ == "__main__":
    update_jobs()
    remove_expired_jobs()
