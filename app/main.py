from fastapi import FastAPI, UploadFile, File, Form, HTTPException
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
    jd: UploadFile | None = File(None),
    jd_text: str | None = Form(None),
    job_description: str | None = Form(None),
    jobDescription: str | None = Form(None),
    role: str | None = Form(None),
    ):
    resume_text = await  read_document(resume)
    pasted_jd = next(
        (
            value for value in (jd_text, job_description, jobDescription, role)
            if value is not None and value.strip()
        ),
        None,
    )
    if pasted_jd is not None:
        jd_content = pasted_jd.strip()
    elif jd is not None:
        jd_content = await read_document(jd)
    else:
        raise HTTPException(
            status_code=400,
            detail="Provide either a JD file or pasted JD text."
        )

    if not jd_content.strip():
        raise HTTPException(
            status_code=400,
            detail="The job description cannot be empty."
        )

    report= analyze_gemini(resume_text, jd_content)

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