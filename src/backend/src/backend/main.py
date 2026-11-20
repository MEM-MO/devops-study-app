import logging

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .config import (
    API_HOST,
    API_PORT,
    APP_NAME,
    CORS_ALLOW_CREDENTIALS,
    CORS_ALLOW_HEADERS,
    CORS_ALLOW_METHODS,
    CORS_ALLOW_ORIGINS,
)
from .models import Stats, StudySession, StudySessionCreate
from .storage import (
    get_all_sessions,
    get_sessions_by_tag,
    get_statistics,
    save_session,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=APP_NAME,
    description="API for tracking study time for DevOps studies",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOW_ORIGINS,
    allow_credentials=CORS_ALLOW_CREDENTIALS,
    allow_methods=CORS_ALLOW_METHODS,
    allow_headers=CORS_ALLOW_HEADERS,
)


@app.get("/")
async def root():
    return {"message": "DevOps Study Tracker API"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/sessions", response_model=StudySession)
async def create_session(session: StudySessionCreate):
    try:
        return save_session(session)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Error creating session",
        ) from exc


@app.get("/sessions", response_model=list[StudySession])
async def read_sessions(tag: str | None = None):
    try:
        if tag:
            return get_sessions_by_tag(tag)
        return get_all_sessions()
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Error fetching sessions",
        ) from exc


@app.get("/stats", response_model=Stats)
async def read_stats():
    try:
        return get_statistics()
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Error fetching statistics",
        ) from exc


def main():
    logger.info("Starting %s API", APP_NAME)
    uvicorn.run("backend.main:app", host=API_HOST, port=API_PORT, reload=True)


# this is just a comment to trigger the pipeline to tag this version and build an image of it
# secundary message to trigger a run after the previous one failed on me having a capitalized username
if __name__ == "__main__":
    main()
