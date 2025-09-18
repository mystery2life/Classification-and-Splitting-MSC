# di/classify.py
import hashlib
from typing import Dict, List
from azure.core.exceptions import AzureError
from core.config import settings, DOC_TYPE_MAP
from .client import make_client


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def map_doc_type(di_type: str | None) -> str:
    if not di_type:
        return "unknown"
    key = str(di_type).strip().lower().replace(" ", "")
    return DOC_TYPE_MAP.get(key) or DOC_TYPE_MAP.get(str(di_type).strip().lower()) or "unknown"


def run_classifier(pdf_bytes: bytes) -> Dict:
    """
    Returns:
      {
        "meta": {"model_id","model_version"},
        "page_preds": [{"page", "doc_type", "confidence"}],
        "doc_parts": [{"doc_type","pages":[...],"confidence": float}]   # <- NEW (from DI Auto split)
      }
    """
    client = make_client()

    try:
        poller = client.begin_classify_document(
            classifier_id=settings.DI_CLASSIFIER_MODEL_ID,
            body=pdf_bytes,
            content_type="application/pdf",
            split="auto",                          # mirror Studio
        )
        result = poller.result(timeout=180)
    except AzureError as e:
        raise RuntimeError(f"DI classify failed: {e}") from e

    page_preds: List[Dict] = []
    doc_parts: List[Dict] = []

    for doc in getattr(result, "documents", []) or []:
        di_type = getattr(doc, "doc_type", None) or getattr(doc, "document_type", None)
        conf = float(getattr(doc, "confidence", 0.0) or 0.0)
        regions = getattr(doc, "bounding_regions", None) or []
        pages = sorted({int(getattr(br, "page_number", 0)) for br in regions if getattr(br, "page_number", None)})

        # per-page predictions (still useful to show)
        for p in pages:
            page_preds.append({"page": p, "doc_type": map_doc_type(di_type), "confidence": conf})

        # one part per *document instance* (don’t merge adjacent instances!)
        if pages:
            doc_parts.append({
                "doc_type": map_doc_type(di_type),
                "pages": pages,
                "confidence": conf
            })

    # Fallback if SDK didn’t return documents (rare)
    if not page_preds and getattr(result, "pages", None):
        for p in result.pages:
            page_preds.append({"page": int(p.page_number), "doc_type": "unknown", "confidence": 0.0})

    meta = {
        "model_id": getattr(result, "model_id", settings.DI_CLASSIFIER_MODEL_ID),
        "model_version": getattr(result, "model_version", "unknown"),
    }

    page_preds.sort(key=lambda x: x["page"])
    return {"meta": meta, "page_preds": page_preds, "doc_parts": doc_parts}
