from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel

from backend.services.prompts import get_level_prompt
from ..services.ai_engine import mark_questions

router = APIRouter(tags=["Mark Exams"])


class QuestionsRequest(BaseModel):
    level: str


@router.post("/markanswer")
async def mark_answer(
    level: str = Form(...), question_file: UploadFile = File(...)
):
    try:
        level_find = await get_level_prompt(level)
        content = await mark_questions(question_file, level_find)
        return {
            "message": "Your work has been successfully marked.",
            "content": content,
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
