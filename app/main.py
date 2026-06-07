from fastapi import FastAPI, UploadFile, File

from app.document_reader import read_document

from app.gemini_service import analyze as analyze_gemini

from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(
    title="Resume Analyzer API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
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
    jd_text = await  read_document(jd)

    report= analyze_gemini(resume_text, jd_text)

    return {
        "status": "success",
        "report": report
}