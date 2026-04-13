"""
Parse JSON in one step
======================
`model_validate_json` parses AND validates in a single Rust pass,
skipping the intermediate Python dict built by `json.loads`.
"""

import json
from pydantic import BaseModel


class Event(BaseModel):
    id: int
    type: str
    payload: dict


raw = b'{"id": 1, "type": "click", "payload": {"x": 10, "y": 20}}'


# Slower: two passes -- json.loads builds a dict, then Pydantic walks it again.
slow = Event.model_validate(json.loads(raw))

# Faster: one pass -- pydantic-core parses JSON straight into the model.
fast = Event.model_validate_json(raw)

assert slow == fast


# Accepts bytes or str -- prefer bytes from the network, avoids a decode step.
also_ok = Event.model_validate_json('{"id": 2, "type": "view", "payload": {}}')
print(also_ok)


# Use this in:
# - FastAPI-style request handlers reading raw body bytes.
# - Kafka / SQS / Kinesis consumers where messages arrive as bytes.
# - Any log/event pipeline processing millions of JSON lines.
