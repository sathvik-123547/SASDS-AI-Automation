from typing import List, Optional

from pydantic import BaseModel, Field

class RequirementAnalysisRequest(BaseModel):
    requirements_text: str

class ModuleItem(BaseModel):
    name: str
    description: Optional[str] = None

class EntityItem(BaseModel):
    name: str
    attributes: List[str] = Field(default_factory=list)

class APIItem(BaseModel):
    name: str
    method: str
    path: str
    description: Optional[str] = None

class RequirementAnalysisResponse(BaseModel):
    modules: List[ModuleItem] = Field(default_factory=list)
    entities: List[EntityItem] = Field(default_factory=list)
    apis: List[APIItem] = Field(default_factory=list)
    non_functional_requirements: List[str] = Field(default_factory=list)
    tech_stack_suggestions: List[str] = Field(default_factory=list)
    missing_information: List[str] = Field(default_factory=list)
