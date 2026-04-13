"""
Parsing JSON strings into models
================================
One call parses AND validates — skip the json.loads detour.

Two paths
---------
Model.model_validate_json(raw)     →  direct  — Rust parses + validates in one pass
Model.model_validate(json.loads(r))→  two-step — works, but extra Python round-trip

Why prefer the direct path
--------------------------
- Faster: parsing happens inside pydantic-core (Rust), no Python dict materialized
- Shorter: one call, one try/except
- Clearer errors: JSON syntax issues surface as ValidationError(type="json_invalid")

When the two-step path is fine
------------------------------
- You already have a `dict` (e.g., from a middleware that parsed JSON for you)
- You need to mutate the dict before validation
"""

import json
import time

from pydantic import BaseModel


class WebhookEvent(BaseModel):
    id: str
    type: str
    amount: float
    currency: str


# Typical source: HTTP body, Kafka message, file on disk.
raw = '{"id": "evt_123", "type": "charge.succeeded", "amount": "19.99", "currency": "USD"}'


# Direct path — preferred. Note "19.99" (str) is coerced to float.
event = WebhookEvent.model_validate_json(raw)
print(event)


# Two-step — same result, more code and slower.
event2 = WebhookEvent.model_validate(json.loads(raw))
assert event == event2


# Micro-benchmark: the gap widens at scale (batch jobs, log ingestion).
N = 10_000
t0 = time.perf_counter()
for _ in range(N):
    WebhookEvent.model_validate_json(raw)
t_direct = time.perf_counter() - t0

t0 = time.perf_counter()
for _ in range(N):
    WebhookEvent.model_validate(json.loads(raw))
t_two_step = time.perf_counter() - t0

print(f"direct: {t_direct:.3f}s   two-step: {t_two_step:.3f}s")
