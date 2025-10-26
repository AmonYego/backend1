from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel

from backend.services.prompts import get_level_prompt
from ..services.ai_engine import generating_similar_questions

router = APIRouter(tags=["Similar Questions"])


class QuestionsRequest(BaseModel):
    level: str


@router.post("/similarquiz")
async def similar(level: str = Form(...), question_file: UploadFile = File(...)):
    try:
        level_find = await get_level_prompt(level)
        content = await generating_similar_questions(question_file, level_find)
        return {
            "message": "Successfully generated a set of similar questions.",
            "content": content,
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
