**FastAPI’s `BackgroundTasks` does not run tasks in parallel**.

Here’s why:

* `BackgroundTasks` is just a thin wrapper over **Starlette’s `BackgroundTask`**.
* It schedules functions to be executed **after the response is sent**.
* Those functions are **blocking sync functions** by design — they run sequentially in the same event loop thread.
* Even if you give it an async function, FastAPI will run it in a threadpool, but not as a true parallel `asyncio.create_task`.

---

### Example with `BackgroundTasks`

```python
from fastapi import FastAPI, BackgroundTasks
import time

app = FastAPI()

def task(name: str):
    time.sleep(5)  # blocking work
    print(f"Task {name} done")

@app.post("/run")
def run(background_tasks: BackgroundTasks):
    background_tasks.add_task(task, "A")
    background_tasks.add_task(task, "B")
    return {"message": "Tasks scheduled"}
```

🚨 Both tasks will **not** run in parallel. They run one after the other (A then B).

---

### If you want **parallel execution**

You should **not** rely on FastAPI’s `BackgroundTasks`. Instead, use:

1. **`asyncio.create_task`** (best for lightweight async jobs).
2. **Celery / RQ / Dramatiq** (best for heavy, long-running jobs, distributed workers).
3. **ThreadPoolExecutor / ProcessPoolExecutor** (if jobs are CPU-heavy).

---

✅ So, if your goal is **parallel processing of hospital validations**, you already made the right move with `asyncio.create_task` instead of `BackgroundTasks`.

---

Would you like me to show you a **comparison demo** where I run 3 dummy tasks with `BackgroundTasks` vs `asyncio.create_task` so you can *see the difference in execution speed*?