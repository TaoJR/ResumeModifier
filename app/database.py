import os
from pymongo import MongoClient
from dotenv import load_dotenv

# 加载 .env 中的环境变量
load_dotenv()

# 从环境变量中获取 Atlas 的 URI
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)

# 连接数据库和集合
db = client["resume_modifier"]
collection = db["jobs"]
