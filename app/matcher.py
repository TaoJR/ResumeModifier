import openai
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def generate_embedding(text, model="text-embedding-3-small"):
    try:
        response = openai.embeddings.create(input=[text], model=model)
        return response.data[0].embedding
    except Exception as e:
        print(f"⚠️ Failed to generate query embedding: {e}")
        return None

def match_jobs(candidate_keywords, job_docs, top_k=5):
    query_vector = generate_embedding(candidate_keywords)
    if not query_vector:
        return []

    job_vectors = []
    job_infos = []

    for job in job_docs:
        if "embedding" in job:
            job_vectors.append(job["embedding"])
            job_infos.append(job)

    if not job_vectors:
        return []

    similarities = cosine_similarity([query_vector], job_vectors)[0]

    scored_jobs = [
        {
            "title": job.get("title", "N/A"),
            "company": job.get("company", "N/A"),
            "location": job.get("location", "N/A"),
            "salary": job.get("salary", "N/A"),
            "apply_link": job.get("apply_link", "N/A"),
            "posted_at": job.get("posted_at", "N/A"),
            "job_description": job.get("job_description", "N/A"),
            "score": round(float(sim), 4)
        }
        for job, sim in zip(job_infos, similarities)
    ]

    return sorted(scored_jobs, key=lambda x: x["score"], reverse=True)[:top_k]
