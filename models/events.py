from pydantic import BaseModel
from typing import List, Optional

class DocumentReceived(BaseModel):
    submission_id: str
    blob_url: str
    sha256: str
    correlation_id: Optional[str] = None

class PartCreated(BaseModel):
    submission_id: str
    part_id: str
    blob_url: str
    doc_type: str
    pages: List[int]
    classification_conf: float
    model_id: str
    model_version: str
    correlation_id: Optional[str] = None
