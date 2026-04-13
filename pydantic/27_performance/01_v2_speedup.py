"""
Why v2 is fast
==============
The validation core (`pydantic-core`) is compiled Rust. Typical speedups
over v1 are 5-50x depending on model shape.
"""

from pydantic import BaseModel


class Item(BaseModel):
    id: int
    name: str
    price: float


# Imagine an ingestion endpoint receiving N records.
# In v1 this loop was the bottleneck; in v2 it's usually negligible.
payloads = [{"id": i, "name": f"item-{i}", "price": i * 1.5} for i in range(1_000)]


# Illustrative sketch -- don't treat the numbers as a real benchmark.
import time
start = time.perf_counter()
items = [Item.model_validate(p) for p in payloads]
elapsed = time.perf_counter() - start
print(f"Validated {len(items)} items in {elapsed*1000:.2f} ms")


# Why it matters:
# - No per-field Python function calls; validation graph runs in Rust.
# - JSON -> model is a single pass (see 03_model_validate_json.py).
# - Lets you validate at boundaries without worrying about throughput.
