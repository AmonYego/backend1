from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel

from backend.services.prompts import get_level_prompt
from backend.services.ai_engine import generate_practice_questions

router = APIRouter(tags=["Generate"])


class QuestionsRequest(BaseModel):
    level: str


@router.post("/generate")
async def generate(
    level: str = Form(...),
    lecture_text: UploadFile = File(...),
    pastpaper_text: UploadFile = File(...),
):
    try:
        level_find = await get_level_prompt(level)
        content = await generate_practice_questions(
            lecture_text, pastpaper_text, level_find
        )
        return {
            "message": "Successfully generated a new set of practice questions.",
            "content": content,
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
