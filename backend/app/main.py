from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.app.core.db import init_db, get_db_connection
from backend.app.modules.autosar_hld.router import router as autosar_router

app = FastAPI(
    title="AUTOSAR HLD AI Assistant",
    description="Case Study 1: Document Analysis & Entity Traceability Assistant",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()
app.include_router(autosar_router)

class ReviewAction(BaseModel):
    query: str
    disposition: str  # Accepted, Rejected, Modified
    comments: str
    reviewed_by: str

@app.post("/audit/record-review")
def record_review(review: ReviewAction):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO review_approvals (query, disposition, comments, reviewed_by) VALUES (?, ?, ?, ?)",
        (review.query, review.disposition, review.comments, review.reviewed_by)
    )
    conn.commit()
    conn.close()
    return {"status": "Review disposition logged in SQLite"}

@app.get("/audit/history")
def get_audit_history():
    conn = get_db_connection()
    records = conn.execute("SELECT * FROM review_approvals ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in records]

@app.get("/health")
def health_check():
    return {"status": "healthy", "module": "AUTOSAR HLD Assistant"}