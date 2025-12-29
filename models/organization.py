from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class Organization(BaseModel):
    id: str
    name: str

    metadata: Dict[str, Any] = {}

    created_at: datetime
    updated_at: datetime


class SubOrganization(BaseModel):
    id: str
    org_id: str

    name: str
    metadata: Dict[str, Any] = {}

    created_at: datetime
    updated_at: datetime
