from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.requirements import RequirementAnalysisResponse


class CodeGenerationRequest(BaseModel):
    requirements_text: str
    analysis: Optional[RequirementAnalysisResponse] = None


class GeneratedFile(BaseModel):
    path: str
    description: Optional[str] = None
    content: str


class CodeGenerationResponse(BaseModel):
    files: List[GeneratedFile] = Field(default_factory=list)
