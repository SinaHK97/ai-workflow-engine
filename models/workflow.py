from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class WorkflowStep(BaseModel):
    step_id: str
    step_type: str  # RAG, LLM, CONDITION, API_CALL, etc.

    label: str
    params: Dict[str, Any]

    next_step: Optional[str] = None


class Workflow(BaseModel):
    id: str
    org_id: str
    sub_org_id: str

    name: str
    description: Optional[str]

    version: int
    is_active: bool

    entry_step: str
    steps: List[WorkflowStep]

    metadata: Dict[str, Any] = {}

    created_at: datetime
