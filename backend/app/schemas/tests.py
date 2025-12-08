from pydantic import BaseModel
from typing import List

class TestGenerationRequest(BaseModel):
    requirements_text: str
    files: List[dict]  # from previous code generation

class GeneratedTestFile(BaseModel):
    path: str
    content: str

class TestGenerationResponse(BaseModel):
    tests: List[GeneratedTestFile]
