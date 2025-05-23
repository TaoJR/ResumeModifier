import os
from flask import Flask
from app.job_api import job_api, fetch_and_store_jobs  # ✅ 引入 fetch_and_store_jobs
from app.routes import api
from app.database import collection  # ✅ 用于检查数据库中已有职位数量
from flask_cors import CORS



app = Flask(__name__)
CORS(app)
app.register_blueprint(job_api, url_prefix="/jobs")
app.register_blueprint(api)

print("Mongo URI:", os.environ.get("MONGO_URI"))

# ✅ 自动预加载逻辑
def preload_if_needed():
    job_count = collection.count_documents({"embedding": {"$exists": True}})
    if job_count < 300:
        print(f"📦 Job count is {job_count}, starting preload...")
        preload_keywords = [
            "backend developer", "frontend developer", "full stack developer",
            "python developer", "java developer", "data scientist", "data engineer",
            "machine learning engineer", "software engineer intern", "web developer",
            "mobile developer", "AI engineer", "cloud engineer", "devops engineer", "software architect"
        ]
        for keyword in preload_keywords:
            print(f"\n📥 Fetching jobs for: {keyword}")
            fetch_and_store_jobs(query=keyword, max_pages=2)
        print("\n✅ Preloading complete.")
    else:
        print(f"✅ Job count already sufficient ({job_count} jobs), skipping preload.")

if __name__ == "__main__":
    preload_if_needed()
    port = int(os.environ.get("PORT", 5000))  # Railway 会注入 PORT 环境变量
    app.run(host="0.0.0.0", port=port)

