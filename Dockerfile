# 使用官方 Python 3.9 镜像
FROM python:3.9-slim-bullseye

# 设置工作目录
WORKDIR /app

# 复制依赖文件 requirements.txt（这样可以利用 Docker 缓存）
COPY requirements.txt .

# 安装系统依赖和 Python 依赖
RUN apt-get update && apt-get install -y \
    openssl \
    libssl-dev \
 && apt-get clean \
 && pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 设置 PYTHONPATH，确保 Flask 能正确导入 app 目录
ENV PYTHONPATH=/app

# 公开 Flask 运行的端口
EXPOSE 5000

# 运行 Flask 应用
CMD ["python", "run.py"]
