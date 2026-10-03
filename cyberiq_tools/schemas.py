from __future__ import annotations
import re
SCHEMAS={
 "finding":{"required":("schema","kind","severity","title","evidence")},
 "analysis":{"required":("schema","findings")},
 "batch":{"required":("schema","processed","results")},
 "case":{"required":("schema","name","created_utc","evidence")},
}
SEVERITIES={"info","low","medium","high","critical"}
SHA256=re.compile(r"^[0-9a-fA-F]{64}$")
def validate_document(data: dict, kind: str) -> dict:
 if kind not in SCHEMAS: raise ValueError(f"Unknown schema kind: {kind}")
 errors=[f"missing required field: {k}" for k in SCHEMAS[kind]["required"] if k not in data]
 if kind=="finding" and data.get("severity") not in SEVERITIES: errors.append("invalid severity")
 if kind=="case" and isinstance(data.get("evidence"),list):
  ids=set()
  for i,item in enumerate(data["evidence"]):
   if not isinstance(item,dict): errors.append(f"evidence[{i}] must be an object"); continue
   if not SHA256.fullmatch(str(item.get("sha256",""))): errors.append(f"evidence[{i}] invalid sha256")
   eid=item.get("id")
   if eid and eid in ids: errors.append(f"duplicate evidence id: {eid}")
   if eid: ids.add(eid)
 return {"kind":kind,"valid":not errors,"missing":[x for x in errors if x.startswith("missing")],"errors":errors}
