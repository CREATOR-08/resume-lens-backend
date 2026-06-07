from fastapi import FastAPI, UploadFile, File

from app.document_reader import read_document

from app.gemini_service import analyze as analyze_gemini
app = FastAPI(
    title="Resume Analyzer API"
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