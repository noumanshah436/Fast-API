To use the `arq` library in a FastAPI application, you need to integrate `arq` for handling background tasks with Redis. Here's a step-by-step guide:

### 1. Install the Required Libraries

First, ensure you have the necessary libraries installed. You can install them using pip:

```bash
pip install fastapi arq
```

### 2. Create an `arq` Worker File

Create a file for your `arq` worker configuration and tasks. For example, let's name it `worker.py`.

```python
# worker.py

from arq import cron
from arq.decorators import cron_job
import asyncio

async def example_task(ctx, param1, param2):
    print(f'Executing task with {param1} and {param2}')
    await asyncio.sleep(5)
    return f'Task completed with {param1} and {param2}'

@cron_job(cron('* * * * *'))
async def scheduled_task(ctx):
    print('This task runs every minute')

class WorkerSettings:
    functions = [example_task, scheduled_task]
    cron_jobs = [scheduled_task]
    redis_settings = 'redis://localhost:6379'
```

### 3. Create Your FastAPI Application

Set up your FastAPI application and integrate it with `arq` for submitting tasks.

```python
# main.py

from fastapi import FastAPI, BackgroundTasks
from arq.connections import ArqRedis, create_pool

app = FastAPI()

async def startup():
    app.state.redis = await create_pool()

async def shutdown():
    await app.state.redis.close()

app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)

@app.post("/run-task/")
async def run_task(param1: str, param2: str, background_tasks: BackgroundTasks):
    redis: ArqRedis = app.state.redis
    job = await redis.enqueue_job('example_task', param1, param2)
    return {"message": "Task submitted", "job_id": job.job_id}

@app.get("/check-task/{job_id}")
async def check_task(job_id: str):
    redis: ArqRedis = app.state.redis
    job = await redis.get_job(job_id)
    if job:
        result = await job.result(poll_delay=0.5)
        return {"status": job.status, "result": result}
    else:
        return {"status": "job not found"}
```

### 4. Run the `arq` Worker

You need to run the `arq` worker to process the background tasks. This is typically done in a separate terminal.

```bash
arq worker.WorkerSettings
```

### 5. Run Your FastAPI Application

Run your FastAPI application using an ASGI server like `uvicorn`.

```bash
uvicorn main:app --reload
```

### Summary

1. **Install FastAPI and `arq`.**
2. **Create an `arq` worker configuration file (`worker.py`).**
3. **Set up your FastAPI application (`main.py`) to submit and check background tasks.**
4. **Run the `arq` worker to process tasks.**
5. **Run your FastAPI application.**

With these steps, you'll have `arq` integrated into your FastAPI application, allowing you to handle background tasks efficiently.