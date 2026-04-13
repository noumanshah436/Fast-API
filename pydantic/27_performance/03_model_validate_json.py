"""
Parse JSON in one step
======================
`model_validate_json` parses AND validates in a single Rust pass,
skipping the intermediate Python dict that `json.loads` would build.

Path                                            Passes   Intermediate
-----------------------------------------------------------------------
Model.model_validate(json.loads(raw))           2        Python dict
Model.model_validate_json(raw)                  1        none (Rust)

Accepts bytes OR str -- prefer bytes, avoids a utf-8 decode step.

Use in:
- FastAPI handlers reading raw request body bytes.
- Kafka / SQS / Kinesis consumers (messages arrive as bytes).
- Log pipelines, NDJSON ingest, anything millions-of-lines shaped.
"""

import json
from pydantic import BaseModel


class Event(BaseModel):
    id: int
    type: str
    payload: dict


raw = b'{"id": 1, "type": "click", "payload": {"x": 10, "y": 20}}'

# Slower: json.loads builds a dict, Pydantic walks it again.
slow = Event.model_validate(json.loads(raw))

# Faster: pydantic-core parses JSON straight into the model.
fast = Event.model_validate_json(raw)

assert slow == fast
print(fast)
