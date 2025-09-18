from pydantic import BaseModel, Field
from typing import List, Literal, Optional

DocType = Literal["paystub","ev_form","bank_stmt","passport","dl","ssn","unknown"]

class PagePrediction(BaseModel):
    page: int = Field(..., ge=1)
    doc_type: DocType
    confidence: float = Field(..., ge=0, le=1)

class Part(BaseModel):
    doc_type: DocType
    pages: List[int] = Field(..., min_items=1)
    confidence: float = Field(..., ge=0, le=1)

class ClassifyRequest(BaseModel):
    blob_url: Optional[str] = None
    correlation_id: Optional[str] = None

class ClassifyResponse(BaseModel):
    sha256: str
    model_id: str
    model_version: str
    pages: List[PagePrediction]
    parts: List[Part]