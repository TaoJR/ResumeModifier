import sys
import os
from flask import Blueprint, jsonify, request
import requests
from app.database import collection  # 确保正确导入 MongoDB 连接
import openai
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))  # 确保 `app` 目录在路径里

job_api = Blueprint("job_api", __name__)

API_URL = "https://jsearch.p.rapidapi.com/search"
HEADERS = {
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com",
    "X-RapidAPI-Key": "eaa381d7f1msh6d53c9dad8ab410p118824jsneb2763f234dd"
}

# ✅ 向量生成函数（使用 OpenAI）
def generate_embedding(text, model="text-embedding-3-small"):
    try:
        response = openai.embeddings.create(input=[text], model=model)
        return response.data[0].embedding
    except Exception as e:
        print(f"⚠️ Failed to generate embedding: {e}")
        return None

# ✅ 主逻辑函数：爬取 + 向量计算 + 入库
def fetch_and_store_jobs(query="developer", location=None, max_pages=3, remote_only=None, min_salary=None, date_posted=None):
    print("🚀 Fetching jobs with filters...")

    for page in range(1, max_pages + 1):
        print(f"📡 Fetching page {page}...")

        params = {
            "query": query,
            "num_pages": page,
        }

        if location:
            params["location"] = location
        if remote_only is not None:
            params["remote_jobs_only"] = str(remote_only).lower()
        if min_salary:
            params["salary_min"] = min_salary
        if date_posted:
            params["date_posted"] = date_posted

        response = requests.get(API_URL, headers=HEADERS, params=params)
        print(f"📡 API response code: {response.status_code}")

        if response.status_code == 200:
            jobs_data = response.json().get("data", [])
            if not jobs_data:
                print("⚠️ No more job data available, stopping fetch.")
                break

            print(f"✅ Page {page} - {len(jobs_data)} job postings received")

            for job in jobs_data:
                job_record = {
                    "title": job.get("job_title", "N/A"),
                    "company": job.get("employer_name", "N/A"),
                    "location": job.get("job_location", "N/A"),
                    "salary": job.get("job_salary", "N/A"),
                    "apply_link": job.get("job_apply_link", "N/A"),
                    "posted_at": job.get("job_posted_at", "N/A"),
                    "job_description": job.get("job_description", "N/A")
                }

                # 👇 拼接文本用于生成向量
                full_text = f"{job_record['title']} at {job_record['company']}. {job_record['job_description']}"
                embedding = generate_embedding(full_text)

                if embedding:
                    job_record["embedding"] = embedding

                # ❗避免重复插入
                if not collection.find_one({"apply_link": job_record["apply_link"]}):
                    collection.insert_one(job_record)
                    print(f"📌 Stored job: {job_record['title']} - {job_record['company']}")

        else:
            print(f"❌ API request failed at page {page}, stopping fetch.")
            break

    print("🎯 Data successfully stored in MongoDB")


# ✅ API 端点
@job_api.route("/fetch_jobs", methods=["GET"])
def fetch_jobs_endpoint():
    query = request.args.get("query", "developer")
    location = request.args.get("location", None)
    max_pages = int(request.args.get("max_pages", 1))
    remote_only = request.args.get("remote_only", None)
    min_salary = request.args.get("min_salary", None)
    date_posted = request.args.get("date_posted", None)

    fetch_and_store_jobs(query, location, max_pages, remote_only, min_salary, date_posted)

    return jsonify({"message": "Job data fetching initiated"}), 200
