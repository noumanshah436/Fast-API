"""
Why v2 is fast
==============
Validation core (`pydantic-core`) is compiled Rust. 5-50x over v1 out of the box.

Where the speed comes from:
- No per-field Python calls; the validation graph runs in Rust.
- JSON -> model is one pass (see 03_model_validate_json.py).
- Schema is built once per class; instance validation just walks it.

Hot paths that benefit most:
- Request handlers (every request validates input + response).
- Stream consumers (Kafka, SQS, Kinesis) -- millions of JSON messages.
- Bulk importers / ETL -- large list[dict] -> list[Model].

You already get it. No config flag, no opt-in.
"""

import time
from pydantic import BaseModel


class Item(BaseModel):
    id: int
    name: str
    price: float


# Illustrative only -- not a real benchmark.
payloads = [{"id": i, "name": f"item-{i}", "price": i * 1.5} for i in range(1_000)]

start = time.perf_counter()
items = [Item.model_validate(p) for p in payloads]
elapsed = time.perf_counter() - start
print(f"Validated {len(items)} items in {elapsed*1000:.2f} ms")
