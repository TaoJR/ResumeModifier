from pymongo import MongoClient


client = MongoClient("mongodb://mongo:27017")

# ✅ 选择数据库（可以自己命名，比如 resumemodifier）
db = client["jobSearch"]

# ✅ 选择集合名（比如 jobs）
collection = db["jobs"]


