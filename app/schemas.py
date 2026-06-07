from pydantic import BaseModel, Field
from typing import Literal
class SkillAssessment(BaseModel):
    skill: str = Field(description="A skill required or preferred by the JD.")
    requirement: Literal["required", "preferred"]
    match: Literal["strong", "partial", "missing"]
    score: float = Field(ge=0, le=100)
    jd_evidence: str
    resume_evidence: str | None = None
    gap: str | None = None


class CategoryAssessment(BaseModel):
    requirement_found: bool
    score: float | None = Field(default=None, ge=0, le=100)
    jd_requirement: str | None = None
    resume_evidence: list[str] = Field(default_factory=list)
    explanation: str


class Recommendation(BaseModel):
    priority: Literal["high", "medium", "low"]
    area: str
    action: str
    suggested_project: str | None = None


class GeminiAssessment(BaseModel):
    role_summary: str
    skills: list[SkillAssessment]
    experience: CategoryAssessment
    projects: CategoryAssessment
    education: CategoryAssessment
    strengths: list[str]
    concerns: list[str]
    recommendations: list[Recommendation]
    final_summary: str