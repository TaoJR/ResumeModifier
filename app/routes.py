from flask import Blueprint, jsonify, request
from app.database import collection
from app.matcher import match_jobs  # ✅ 引入匹配逻辑

api = Blueprint("api", __name__)

# ✅ 获取所有职位（原接口保留）
@api.route("/jobs", methods=["GET"])
def get_jobs():
    jobs = list(collection.find({}, {"_id": 0}))
    return jsonify(jobs)

# ✅ 关键词匹配职位接口
@api.route("/api/match_jobs", methods=["POST"])
def match_jobs_endpoint():
    data = request.get_json()
    keywords = data.get("candidate_keywords")
    top_k = int(data.get("top_k", 5))

    if not keywords:
        return jsonify({"error": "Missing 'candidate_keywords'"}), 400

    job_docs = list(collection.find({"embedding": {"$exists": True}}))

    if not job_docs:
        return jsonify({"error": "No jobs available for matching."}), 404

    results = match_jobs(keywords, job_docs, top_k)

    return jsonify({"matches": results}), 200
