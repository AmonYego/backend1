from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel

from backend.services.prompts import get_level_prompt
from ..services.ai_engine import simplify_explanation

router = APIRouter(tags=["Simplify Explanation"])


class QuestionsRequest(BaseModel):
    level: str


@router.post("/explanation")
async def simplify(level: str = Form(...), lecture_text: UploadFile = File(...)):
    try:
        level_find = await get_level_prompt(level)
        content = await simplify_explanation(lecture_text, level_find)
        return {
            "message": "The explanation has been successfully simplified.",
            "content": content,
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
