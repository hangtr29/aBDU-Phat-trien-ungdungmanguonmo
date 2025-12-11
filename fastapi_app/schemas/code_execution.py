from pydantic import BaseModel
from typing import Optional


class CodeExecutionRequest(BaseModel):
    code: str
    language: str  # python, javascript, cpp, java
    stdin: Optional[str] = None


class CodeExecutionResponse(BaseModel):
    output: str
    error: Optional[str] = None
    execution_time: Optional[float] = None
    exit_code: Optional[int] = None

