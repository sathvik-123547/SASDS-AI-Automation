from pydantic import BaseModel
from typing import List, Optional

class RequirementAnalysisRequest(BaseModel):
    requirements_text: str

class ModuleItem(BaseModel):
    name: str
    description: Optional[str] = None

class EntityItem(BaseModel):
    name: str
    attributes: List[str] = []

class APIItem(BaseModel):
    name: str
    method: str
    path: str
    description: Optional[str] = None

class RequirementAnalysisResponse(BaseModel):
    modules: List[ModuleItem] = []
    entities: List[EntityItem] = []
    apis: List[APIItem] = []
    non_functional_requirements: List[str] = []
    tech_stack_suggestions: List[str] = []
    missing_information: List[str] = []
