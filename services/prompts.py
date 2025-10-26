"""
This module contains reusable prompt templates for different features.
We dynamically build prompts by injecting level, lecture content, and past paper content.
"""


async def get_level_prompt(level: str) -> str:
    level = level.lower()
    if "lower primary" in level:
        return """
        The learner is in LOWER PRIMARY (Grade 1–5 in Kenyan CBC).
        ✅ Use VERY SIMPLE English or Kiswahili-friendly language.
        ✅ Explain like teaching a young child (short, joyful, friendly sentences).
        ✅ Give fun and relatable examples (toys, animals, food, games, family, cartoons).
        ✅ Use a playful and encouraging tone (e.g. “Great job! Let’s try another one!”).
        ✅ Avoid complex terms, abstract ideas, or deep reasoning.
        ✅ Encourage learning with excitement and imagination.
        ✅ If explaining a concept:
            1. Say what it is in 1 easy line.
            2. Give one playful example.
            3. Ask a tiny question or give a fun quick activity (optional).
        """

    elif "upper primary" in level:
        return """
        The learner is in UPPER PRIMARY (Grade 6–9 in Kenyan CBC).
        ✅ Use simple English with mild academic structure.
        ✅ Explain concepts step-by-step with clear logic.
        ✅ Use relatable examples from school, hobbies, friends, or basic science.
        ✅ Introduce basic academic terms and define them simply.
        ✅ Tone should be supportive, like a kind school tutor.
        ✅ If explaining a concept:
            1. Give a short definition.
            2. Explain step-by-step using relatable examples.
            3. Give one worked-out example.
            4. Point out one common mistake or misconception.
            5. Provide a 2-question practice quiz with answers.
            6. End with one “challenge” question for extra thinking.
        """

    elif "high school" in level or "secondary" in level:
        return """
        The learner is in HIGH SCHOOL (Grade 10–12 in Kenyan CBC / KCSE level).
        ✅ Provide deeper understanding suitable for KCSE revision and critical thinking.
        ✅ Use more formal academic language and introduce subject terminology (define terms briefly).
        ✅ Explain logically with cause-effect reasoning or analytical breakdowns.
        ✅ Include exam-focused insights, marking scheme awareness, and common pitfalls.
        ✅ Use relatable teenage scenarios (career paths, innovation, social issues, science & tech).
        ✅ If explaining a concept:
            1. Provide a clear, exam-ready definition (1–2 lines).
            2. Break down the concept into 3–4 logical points or processes.
            3. Give one fully worked example/exercise with reasoning.
            4. Include a KCSE tip or misconception warning.
            5. Provide two exam-style practice questions (Standard + Advanced), with marking scheme guidance.
            6. End with a real-world, industry, or university-level application.
        """
    else:
        # Detect numeric grades
        grade_num = None
        for word in level.split():
            if word.isdigit():
                grade_num = int(word)
                break

        # Early Primary: Grade 1-2
        if grade_num in [1, 2]:
            return """
            The learner is in EARLY PRIMARY (Grade 1–2).
            ✅ Use VERY simple and playful language.
            ✅ Explain using everyday examples: toys, colors, family, animals.
            ✅ Keep sentences short.
            ✅ Use storytelling or scenarios.
            ✅ Avoid complex terms; if used, explain like talking to a child.
            """

        # Upper Primary: Grade 3–5
        if grade_num in [3, 4, 5]:
            return """
            The learner is in UPPER PRIMARY (Grade 3–5).
            ✅ Use simple language.
            ✅ Explain using relatable examples: school life, food, games, daily routines.
            ✅ Break down concepts into steps.
            ✅ Use fun comparisons and short explanations.
            """

        # Junior Secondary / Middle School: Grade 6–8
        if grade_num in [6, 7, 8]:
            return """
            The learner is in JUNIOR SECONDARY (Grade 6–8).
            ✅ Use clear and slightly more detailed explanations.
            ✅ Introduce basic reasoning and logic.
            ✅ Use relatable everyday analogies.
            ✅ Encourage understanding rather than memorization.
            """

        # High School / Senior Secondary / Grade 9–12 or Form 1–4
        if grade_num in [9, 10, 11, 12] or "form" in level:
            return """
            The learner is in HIGH SCHOOL (Grade 9–12 / Form 1–4).
            ✅ Provide structured explanations.
            ✅ Use subject-specific terminology but explain it clearly.
            ✅ Provide logical flow: definition → explanation → example.
            ✅ Can include basic problem-solving steps or exam tips.
            """

        # University/College Detection
        if (
            "university" in level
            or "college" in level
            or "undergraduate" in level
            or "year" in level
        ):
            return f"""
            The learner is a {level} student (Year 1–5 or equivalent).
            ✅ Use advanced academic and technical language where appropriate.
            ✅ Provide structured and logically coherent explanations.
            ✅ Reference theories, frameworks, formulas, research insights, or case studies.
            ✅ Encourage critical thinking, comparison, and problem-solving.
            ✅ If explaining a topic:
                1. Begin with a concise abstract/overview.
                2. Provide a detailed conceptual explanation with logical sectioning.
                3. Introduce models or theoretical frameworks where relevant.
                4. Include a real-world or industry case study or application.
                5. Offer a solved advanced problem or scenario.
                6. Suggest further exploration or extension questions.
            """

        # Default fallback
        return """
        The learner's level is unspecified, so assume an adaptable explanation.
        ✅ Start with a simple explanation.
        ✅ Gradually increase technical depth.
        ✅ Adjust based on complexity expected for general understanding.
        """


async def topic_extraction_prompt(lecture_text, pastpaper_text, level_find):
    return f"""{level_find}

You are an expert academic assistant.
Your task is to extract study topics and subtopics based on the textual content provided below from a set of lecture notes and a past paper. Do not attempt to access any files, as the content is already here.

---
BEGIN LECTURE NOTES CONTENT
---
{lecture_text}
---
END LECTURE NOTES CONTENT
---

---
BEGIN PAST PAPER CONTENT
---
{pastpaper_text}
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


async def question_generation_prompt(lecture_text, pastpaper_text, level_find):
    return f"""{level_find}

You are an expert examiner.
Your task is to create 30 exam-style questions based on the textual content provided below. Do not attempt to access any files, as the content is already here.

---
BEGIN LECTURE NOTES CONTENT
---
{lecture_text}
---
END LECTURE NOTES CONTENT
---

---
BEGIN PAST PAPER CONTENT
---
{pastpaper_text}
---
END PAST PAPER CONTENT
---

Using *only* the content above, create 30 exam-style questions of mixed difficulty (easy, moderate, hard).

✅ Include:
- 10 Multiple-choice questions
- 10 Short-answer questions
- 5 Structured questions (step-based answers)
- 5 Essay questions
"""


async def generate_marking_prompt(extracted_text, level_find):
    """
    Create a prompt using extracted question text and level.
    """
    return f"""You are an expert KCSE examiner. Your task is to grade the student's answer provided below.

Student Level: {level_find}

---
BEGIN STUDENT ANSWER
---
{extracted_text}
---
END STUDENT ANSWER
---

Based *only* on the text provided above, grade the student's physics answer fairly and strictly based on the KCSE marking scheme.

Provide:
1. Final Score (out of 100)
2. Correct Points
3. Mistakes and Corrections
4. Suggested Improvements
5. A Model Perfect Answer
"""


async def simplifification_prompt(lecture_text, level_find):
    return f"""You are a friendly, student-centered tutor.
Your task is to simplify the lecture content provided below, using the learner’s level and style guide.

Learner's Level and Style Guide: {level_find}

---
BEGIN LECTURE CONTENT
---
{lecture_text}
---
END LECTURE CONTENT
---

Now, simplify the provided lecture content based *only* on the text above.
✅ Break complex ideas into simple points.
✅ Use relatable real-life examples.
✅ Define technical terms briefly when first introduced.
✅ Avoid jargon unless necessary.
✅ Make the explanation engaging and easy to understand.
✅ If relevant, end with a short summary or an example for better retention.

Return the simplified explanation in a structured, easy-to-read format.
"""


async def similar_questions_prompt(question_file, level_find):
    return f"""You are an expert exam setter.
The learner’s level is:
{level_find}

Your task is to generate 10 new questions that test the same concept as the original question provided below.

---
BEGIN ORIGINAL QUESTION
---
{question_file}
---
END ORIGINAL QUESTION
---

Based *only* on the original question provided above, generate 10 new questions that test the same concept, difficulty level, and learning objective.

Guidelines:
✅ Maintain the same question format (MCQ, short answer, structured, essay, etc.).
✅ Paraphrase using different contexts, examples, or numerical values where appropriate.
✅ Avoid repeating words too closely from the original question.
✅ Ensure all questions are clear, appropriate for the learner's level, and logically sound.
✅ Keep exam relevance and assessment accuracy in mind.

Return the questions neatly in a numbered list (1–10).
"""
