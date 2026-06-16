from fastapi import FastAPI, UploadFile, File
from app.routes.premium import router as premium_router
from app.document_reader import read_document

from app.gemini_service import analyze as analyze_gemini
from app.premium_analyze import premium_analyze_file

from fastapi.middleware.cors import CORSMiddleware
import os
origin= os.getenv("ALLOWED_ORIGINS")
app = FastAPI(
    title="Resume Analyzer API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "status": "running"
    }
@app.post("/analyse")
async def analyse(
    resume: UploadFile = File(...),
    jd: UploadFile = File(...)
    ):
    resume_text = await  read_document(resume)
    if(isinstance(jd, str)):
        jd_text= jd
    else:
        jd_text = await  read_document(jd)

    report= analyze_gemini(resume_text, jd_text)

    return {
        "status": "success",
        "report": report
}


@app.post("/analyse/premium")
async def premium_analyse(
    resume: UploadFile = File(...),

):
    report = await premium_analyze_file(resume)

    return {
        "status": "success",
        "report": report
    }

app.include_router(premium_router)