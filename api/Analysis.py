from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel

from backend.services.prompts import get_level_prompt
from ..services.ai_engine import extract_study_topics

router = APIRouter(tags=["Extract Topics"])


class QuestionsRequest(BaseModel):
    level: str


@router.post("/topics")
async def extract_topics(
    level: str = Form(...),
    lecture_text: UploadFile = File(...),
    pastpaper_text: UploadFile = File(...),
):
    try:
        level_find = await get_level_prompt(level)
        content = await extract_study_topics(lecture_text, pastpaper_text, level_find)
        return {
            "message": "Successfully extracted key topics and subtopics.",
            "content": content,
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
