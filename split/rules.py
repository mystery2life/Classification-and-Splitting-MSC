from typing import List, Dict, Any
from core.config import settings

def apply_thresholds(page_preds: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Force very-low confidence predictions to 'unknown'.
    """
    out = []
    for x in page_preds:
        conf = float(x.get("confidence", 0.0))
        doc_type = x["doc_type"] if conf >= settings.CONF_SECONDARY else "unknown"
        out.append({"page": int(x["page"]), "doc_type": doc_type, "confidence": conf})
    return sorted(out, key=lambda r: r["page"])

def merge_adjacent(pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Merge contiguous pages with the same doc_type into parts.
    Part confidence = MIN of member pages (conservative).
    """
    if not pages: 
        return []
    pages = sorted(pages, key=lambda r: r["page"])
    parts = []
    cur = {"doc_type": pages[0]["doc_type"], "pages": [pages[0]["page"]], "confidence": pages[0]["confidence"]}
    for x in pages[1:]:
        if x["doc_type"] == cur["doc_type"] and x["page"] == cur["pages"][-1] + 1:
            cur["pages"].append(x["page"])
            cur["confidence"] = min(cur["confidence"], x["confidence"])
        else:
            parts.append(cur)
            cur = {"doc_type": x["doc_type"], "pages": [x["page"]], "confidence": x["confidence"]}
    parts.append(cur)
    return parts
