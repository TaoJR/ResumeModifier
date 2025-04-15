from app.job_api import fetch_and_store_jobs

# ✅ 关键词列表：覆盖多个热门岗位方向
preload_keywords = [
    "backend developer", "frontend developer", "full stack developer",
    "python developer", "java developer", "data scientist", "data engineer",
    "machine learning engineer", "software engineer intern", "web developer",
    "mobile developer", "AI engineer", "cloud engineer", "devops engineer", "software architect"
]

# ✅ 每个关键词抓取 2 页（约 20 条职位）
for keyword in preload_keywords:
    print(f"\n📥 Fetching jobs for: {keyword}")
    fetch_and_store_jobs(query=keyword, max_pages=2)

print("\n✅ Preloading complete: Initial job dataset is ready.")