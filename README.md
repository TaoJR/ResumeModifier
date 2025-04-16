# ResumeModifier

A Flask-based backend service for fetching, storing, and matching job postings with resume descriptions using semantic search powered by OpenAI.

---

## Features

- Fetch jobs from RapidAPI (JSearch API)
- Store jobs in MongoDB (with OpenAI vector embedding)
- Match jobs to user resumes using cosine similarity
- Preloading strategy for fallback when live API data is insufficient
- Dockerized for easy setup

---

## Requirements

- Docker
- Docker Compose
- OpenAI API Key (for embedding)
- RapidAPI Key (for job data)

---

## Setup & Usage

### 1. Clone this repo

```bash
git clone https://github.com/TaoJR/ResumeModifier.git
cd ResumeModifier
```

### 2. Create your `.env` file

In the root directory:

```bash
echo "OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" > .env
```

Replace the value with your actual OpenAI key.

> Do **NOT** commit `.env` to GitHub.

### 3. Build and start the containers

```bash
docker-compose up --build
```

This will:
- Start the Flask app on `localhost:5000`
- Start MongoDB (available at `mongodb://localhost:27017` for Compass, or `mongo:27017` inside Docker)

---

## API Endpoints

### `/jobs/fetch_jobs` (GET)
Fetch jobs from API and store them with embedding.

**Params** (as query):
- `query`: Job keyword (e.g., Python)
- `max_pages`: Number of pages (default 1)

```bash
curl "http://localhost:5000/jobs/fetch_jobs?query=Python&max_pages=1"
```

---

### `/api/match_jobs` (POST)
Match user resume with top-k job embeddings.

**Request body** (JSON):
```json
{
  "resume": "Experienced Python backend developer with MongoDB and Flask knowledge.",
  "candidate_keywords": ["Python", "Flask", "MongoDB"],
  "top_k": 5
}
```

```bash
curl -X POST http://localhost:5000/api/match_jobs \
  -H "Content-Type: application/json" \
  -d '{
        "resume": "Experienced Python backend developer with MongoDB and Flask knowledge.",
        "candidate_keywords": ["Python", "Flask", "MongoDB"],
        "top_k": 5
      }'
```

---

## Architecture

- `app/job_api.py`: Job fetching & embedding logic
- `app/routes.py`: Resume-job matching logic
- `app/database.py`: MongoDB connection
- `matcher.py`: Core cosine similarity logic
- `run.py`: Entrypoint

---

## Testing MongoDB (optional)

You can connect with [MongoDB Compass](https://www.mongodb.com/try/download/compass):
- **Host**: `localhost`
- **Port**: `27017`
- **Database**: `jobSearch`
- **Collection**: `jobs`

---

## Contributors
- @TaoJR — Backend / Docker / Matching logic

---

