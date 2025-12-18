from typing import List

from pydantic import BaseModel, Field

class TestGenerationRequest(BaseModel):
    requirements_text: str
    files: List[dict]  # from previous code generation

class GeneratedTestFile(BaseModel):
    path: str
    content: str

class TestGenerationResponse(BaseModel):
    tests: List[GeneratedTestFile] = Field(default_factory=list)
