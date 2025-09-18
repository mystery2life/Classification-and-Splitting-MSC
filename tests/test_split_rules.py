from split.rules import apply_thresholds, merge_adjacent

def test_merge_adjacent_basic():
    pages = [
        {"page":1,"doc_type":"paystub","confidence":0.9},
        {"page":2,"doc_type":"paystub","confidence":0.8},
        {"page":3,"doc_type":"ev_form","confidence":0.95},
    ]
    merged = merge_adjacent(pages)
    assert merged[0]["pages"] == [1,2]
    assert merged[1]["pages"] == [3]

def test_thresholds_force_unknown():
    pages = [
        {"page":1,"doc_type":"paystub","confidence":0.50},
        {"page":2,"doc_type":"ev_form","confidence":0.70},
    ]
    out = apply_thresholds(pages)
    assert out[0]["doc_type"] == "unknown"
    assert out[1]["doc_type"] == "ev_form"
