from google import genai
from google.genai import types

from dotenv import load_dotenv
import os

from app.prompts.basic_prompt import SYSTEM_INSTRUCTION
from app.schema.basic_schema import (
    CategoryAssessment,
    GeminiAssessment,
    Recommendation,
    SkillAssessment,
)
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
DEFAULT_WEIGHTS = {
    "skills": 45.0,
    "experience": 25.0,
    "projects": 15.0,
    "education": 15.0,
}




def build_prompt(resume_text: str, jd_text: str) -> str:
    return f"""
Compare the resume with the job description and return the complete assessment.

Scoring guidance:
- Skill scores should reflect both presence and demonstrated depth.
- Experience should receive proportional credit when relevant experience is
  below the requested duration.
- Projects should count only when their relevance is supported by the resume.
- CGPA/GPA must not be scored unless the JD explicitly requires it.
- Missing information is not evidence; explain uncertainty instead of guessing.

<job_description>
{jd_text}
</job_description>

<resume>
{resume_text}
</resume>
""".strip()


def call_gemini(
    resume_text: str,
    jd_text: str,
    model: str = DEFAULT_MODEL,
) -> GeminiAssessment:
    response = client.models.generate_content(
        model=model,
        contents=build_prompt(resume_text, jd_text),
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.2,
            response_mime_type="application/json",
            response_json_schema=GeminiAssessment.model_json_schema(),
        ),
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    return GeminiAssessment.model_validate_json(response.text)



def average_skill_score(skills: list[SkillAssessment]) -> float | None:
    if not skills:
        return None
    weighted_total = 0.0
    weight_total = 0.0
    for item in skills:
        weight = 2.0 if item.requirement == "required" else 1.0
        weighted_total += item.score * weight
        weight_total += weight
    return weighted_total / weight_total

def assemble_report(assessment: GeminiAssessment, model: str) -> dict:
    category_scores = {
        "skills": average_skill_score(assessment.skills),
        "experience": (
            assessment.experience.score
            if assessment.experience.requirement_found
            else None
        ),
        "projects": (
            assessment.projects.score
            if assessment.projects.requirement_found
            else None
        ),
        "education": (
            assessment.education.score
            if assessment.education.requirement_found
            else None
        ),
    }

    active_weight = sum(
        DEFAULT_WEIGHTS[name]
        for name, score in category_scores.items()
        if score is not None
    )
    effective_weights = {
        name: (
            DEFAULT_WEIGHTS[name] / active_weight * 100
            if score is not None and active_weight
            else 0.0
        )
        for name, score in category_scores.items()
    }
    overall_score = sum(
        score * effective_weights[name] / 100
        for name, score in category_scores.items()
        if score is not None
    )

    return {
        "provider": "Google Gemini",
        "model": model,
        "overall_score": round(overall_score, 2),
        "category_scores": {
            name: round(score, 2) if score is not None else None
            for name, score in category_scores.items()
        },
        "effective_weights": {
            name: round(weight, 2) for name, weight in effective_weights.items()
        },
        "role_summary": assessment.role_summary,
        "skills": [item.model_dump() for item in assessment.skills],
        "experience": assessment.experience.model_dump(),
        "projects": assessment.projects.model_dump(),
        "education": assessment.education.model_dump(),
        "strengths": assessment.strengths,
        "concerns": assessment.concerns,
        "recommendations": [
            item.model_dump() for item in assessment.recommendations
        ],
        "final_summary": assessment.final_summary,
        "disclaimer": (
            "This AI assessment is a decision-support tool, not an automatic "
            "hiring decision. A human reviewer should verify its evidence."
        ),
    }


def analyze(
    resume_text: str,
    jd_text: str,
    model: str = DEFAULT_MODEL,
) -> dict:
    assessment = call_gemini(resume_text, jd_text, model)
    return assemble_report(assessment, model)

def print_summary(report: dict) -> None:
    print(f"\nOverall match: {report['overall_score']:.2f}/100")
    print(f"Model: {report['model']}")
    print("\nCategory scores:")
    for name, score in report["category_scores"].items():
        value = "Not required by JD" if score is None else f"{score:.2f}/100"
        print(f"  {name.title()}: {value}")

    print("\nSkill assessment:")
    if not report["skills"]:
        print("  No specific skills were extracted from the JD.")
    for skill in report["skills"]:
        print(
            f"  {skill['skill']}: {skill['score']:.0f}/100 "
            f"({skill['match']}, {skill['requirement']})"
        )

    print("\nRecommendations:")
    if not report["recommendations"]:
        print("  No major gaps identified.")
    for item in report["recommendations"]:
        print(f"  [{item['priority'].upper()}] {item['area']}: {item['action']}")

