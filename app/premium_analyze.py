from google import genai
from google.genai import types

from dotenv import load_dotenv
import os
from fastapi import UploadFile

from app.document_reader import read_document
from app.prompts.premium_prompt import PREMIUM_SYSTEM
from app.schema.premium import PremiumAssessment

load_dotenv()

key=os.getenv("GEMINI_API_KEY")
if not key:
    raise ValueError(
        "GEMINI_API_KEY not found."
    )

client = genai.Client(
    api_key=key
)
DEFAULT_MODEL = "gemini-2.5-flash-lite"
def build_premium_prompt(resume_text: str):

    return f"""

Analyze this resume.

<resume>

{resume_text}

</resume>

"""
def premium_analyze(resume_text: str):
    response = client.models.generate_content(

model=DEFAULT_MODEL,

contents=build_premium_prompt(
    resume_text
),

config=types.GenerateContentConfig(

system_instruction=PREMIUM_SYSTEM,

temperature=0.2,

response_mime_type="application/json",

response_json_schema=
PremiumAssessment.model_json_schema()

)

)
    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return PremiumAssessment.model_validate_json(
        response.text
    )


async def premium_analyze_file(resume: UploadFile) -> PremiumAssessment:
    resume_text = await read_document(resume)
    return premium_analyze(resume_text)