"""
Parsing JSON strings into models
================================
model_validate_json parses + validates in one pass -- skip json.loads.
"""

import json
import time

from pydantic import BaseModel


class WebhookEvent(BaseModel):
    id: str
    type: str
    amount: float
    currency: str


# Raw JSON as you would receive it from an HTTP request body,
# a Kafka message, or a file on disk.
raw = '{"id": "evt_123", "type": "charge.succeeded", "amount": "19.99", "currency": "USD"}'


# Direct: Pydantic parses the bytes/str itself (Rust-backed, no Python json.loads).
event = WebhookEvent.model_validate_json(raw)
print(event)


# Equivalent two-step -- works, but slower and more code.
data = json.loads(raw)
event2 = WebhookEvent.model_validate(data)
assert event == event2


# Quick benchmark on a batch -- the direct path wins noticeably at scale.
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
