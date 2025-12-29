from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class WorkflowExecution(BaseModel):
    execution_id: str

    workflow_id: str
    workflow_version: int

    org_id: str
    sub_org_id: str

    input_payload: Dict[str, Any]

    status: str  # PENDING, RUNNING, SUCCESS, FAILED

    started_at: datetime
    finished_at: Optional[datetime]


class ExecutionStepLog(BaseModel):
    execution_id: str

    step_id: str
    step_type: str

    status: str  # SUCCESS, FAILED
    started_at: datetime
    finished_at: datetime

    output_summary: Optional[Dict[str, Any]]
    error_message: Optional[str]


class ExecutionLog(BaseModel):
    execution_id: str

    workflow_id: str
    workflow_version: int

    org_id: str
    sub_org_id: str

    status: str
    total_duration_ms: int

    steps: List[ExecutionStepLog]
