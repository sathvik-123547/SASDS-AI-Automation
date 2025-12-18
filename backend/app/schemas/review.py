from typing import List, Optional

from pydantic import BaseModel, Field


class ReviewFile(BaseModel):
    path: str
    content: str
    description: Optional[str] = None


class ReviewIssue(BaseModel):
    severity: str = Field(
        description="One of: info, low, medium, high, critical"
    )
    file: Optional[str] = None
    line: Optional[int] = None
    summary: str
    recommendation: str


class CodeReviewRequest(BaseModel):
    requirements_text: Optional[str] = Field(
        default=None,
        description="Optional requirements for context."
    )
    files: List[ReviewFile] = Field(
        default_factory=list,
        description="Files to review (path + content)."
    )


class CodeReviewResponse(BaseModel):
    summary: str
    issues: List[ReviewIssue] = Field(default_factory=list)


