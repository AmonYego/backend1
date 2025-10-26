from fastapi import FastAPI

from backend.api.Analysis import router as extract_router
from backend.api.questions import router as questions_router
from backend.api.Marking import router as marking_router
from backend.api.similar import router as similar_router
from backend.api.simplify import router as simplify_router

app = FastAPI(
    title="Classroom AI Backend",
    version="1.0.0",
    description="AI-powered academic assistant",
)

# Register routers
app.include_router(extract_router, prefix="/extract")
app.include_router(questions_router, prefix="/questions")
app.include_router(simplify_router, prefix="/simplify")
app.include_router(similar_router, prefix="/similar")
app.include_router(marking_router, prefix="/marking")


@app.get("/")
def home():
    return {"message": "FastAPI backend running successfully! 🚀"}
