# service/orchestrate.py
from models.api import ClassifyResponse, PagePrediction, Part
from di.classify import run_classifier, sha256_bytes

def classify_and_split(pdf_bytes: bytes) -> ClassifyResponse:
    di = run_classifier(pdf_bytes)

    pages = [PagePrediction(**p) for p in di["page_preds"]]

    parts: list[Part] = []
    if di.get("doc_parts"):   # <-- Prefer Azure Auto split
        for d in di["doc_parts"]:
            parts.append(Part(doc_type=d["doc_type"], pages=d["pages"], confidence=d["confidence"]))
    else:
        # fallback: merge contiguous pages with same label (your old behavior)
        if pages:
            cur = {"doc_type": pages[0].doc_type, "pages": [pages[0].page], "confidence": pages[0].confidence}
            for p in pages[1:]:
                if p.doc_type == cur["doc_type"] and p.page == cur["pages"][-1] + 1:
                    cur["pages"].append(p.page)
                    cur["confidence"] = min(cur["confidence"], p.confidence)
                else:
                    parts.append(Part(**cur))
                    cur = {"doc_type": p.doc_type, "pages": [p.page], "confidence": p.confidence}
            parts.append(Part(**cur))

    return ClassifyResponse(
        sha256=sha256_bytes(pdf_bytes),
        model_id=di["meta"]["model_id"],
        model_version=di["meta"]["model_version"],
        pages=pages,
        parts=parts,
    )
