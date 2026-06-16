from fastapi import APIRouter, File, UploadFile

from app.premium_analyze import premium_analyze_file

router=APIRouter(
    prefix="/premium",
    tags=["Premium"]
)


@router.post("/check")
async def premium_check(resume: UploadFile = File(...)):
    return await premium_analyze_file(resume)