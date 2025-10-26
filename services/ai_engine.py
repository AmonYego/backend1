from backend.services.prompts import (
    question_generation_prompt,
    simplifification_prompt,
    similar_questions_prompt,
    generate_marking_prompt,
)
import google.generativeai as genai
from fastapi import UploadFile
from backend.services.file_reader import extract_text

genai.configure(api_key="AIzaSyARKbi8gr-3sLsw5KOEsZMUsudHA53sxBA")
model = genai.GenerativeModel("gemini-2.5-flash")


async def extract_study_topics(
    lecture_text: UploadFile, pastpaper_text: UploadFile, level_find: str
):
    lecture_content = await extract_text(lecture_text)
    pastpaper_content = await extract_text(pastpaper_text)
    prompt = f"""{level_find}

You are an expert academic assistant.
Your task is to extract study topics and subtopics based on the textual content provided below from a set of lecture notes and a past paper. Do not attempt to access any files, as the content is already here.

---
BEGIN LECTURE NOTES CONTENT
---
{lecture_content}
---
END LECTURE NOTES CONTENT
---

---
BEGIN PAST PAPER CONTENT
---
{pastpaper_content}
---
END PAST PAPER CONTENT
---

Based *only* on the text provided above, identify the key topics and subtopics.

✅ Output Format:
1. Main Topic
   - Subtopic 1
   - Subtopic 2
2. Main Topic
   - Subtopic 1
"""
    response = model.generate_content(prompt)
    return response.text


async def generate_practice_questions(
    lecture_text: UploadFile, pastpaper_text: UploadFile, level_find: str
):
    lecture_content = await extract_text(lecture_text)
    pastpaper_content = await extract_text(pastpaper_text)
    prompt = await question_generation_prompt(
        lecture_content, pastpaper_content, level_find
    )
    response = model.generate_content(prompt)
    return response.text


async def generating_similar_questions(question_file: UploadFile, level_find: str):
    question_content = await extract_text(question_file)
    prompt = await similar_questions_prompt(question_content, level_find)
    response = model.generate_content(prompt)
    return response.text


async def simplify_explanation(lecture_text: UploadFile, level_find: str):
    extracted_text = await extract_text(lecture_text)
    prompt = await simplifification_prompt(extracted_text, level_find)
    response = model.generate_content(prompt)
    return response.text


async def mark_questions(question_file: UploadFile, level_find: str):
    extracted = await extract_text(question_file)
    prompt = await generate_marking_prompt(extracted, level_find)
    print(prompt)
    response = model.generate_content(prompt)
    return response.text
