from __future__ import annotations

SCHEMAS={
 "finding":{"required":("schema","kind","severity","title","evidence")},
 "analysis":{"required":("schema","findings")},
 "batch":{"required":("schema","processed","results")},
 "case":{"required":("schema","name","created_utc","evidence")},
}

def validate_document(data: dict, kind: str) -> dict:
    if kind not in SCHEMAS: raise ValueError(f"Unknown schema kind: {kind}")
    missing=[k for k in SCHEMAS[kind]["required"] if k not in data]
    return {"kind":kind,"valid":not missing,"missing":missing}
