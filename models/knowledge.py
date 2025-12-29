from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class KnowledgeCollection(BaseModel):
    id: str
    org_id: str
    sub_org_id: str

    name: str
    description: Optional[str]

    embedding_model: str
    metadata: Dict[str, Any] = {}

    created_at: datetime
    updated_at: datetime


class Document(BaseModel):
    id: str
    org_id: str
    sub_org_id: str
    collection_id: str

    source_type: str  # pdf, text, url, markdown
    source_uri: Optional[str]

    content_hash: str
    metadata: Dict[str, Any] = {}

    created_at: datetime


class DocumentChunk(BaseModel):
    id: str
    org_id: str
    sub_org_id: str
    collection_id: str
    document_id: str

    chunk_index: int
    text: str
    embedding: List[float]

    metadata: Dict[str, Any] = {}
