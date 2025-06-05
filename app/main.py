from fastapi import FastAPI
from app.models import IngestionRequest
from app.queues import ingestions, add_to_queue
from app.utils import generate_batches, get_ingestion_status
from uuid import uuid4
from app import tasks
import time

app = FastAPI()

@app.post("/ingest")
def ingest(request: IngestionRequest):
    ingestion_id = str(uuid4())
    batches = generate_batches(request.ids)
    ingestions[ingestion_id] = {
        "priority": request.priority,
        "created_time": time.time(),
        "batches": batches
    }
    add_to_queue(ingestion_id, request.priority, batches)
    return {"ingestion_id": ingestion_id}

@app.get("/status/{ingestion_id}")
def status(ingestion_id: str):
    if ingestion_id not in ingestions:
        return {"error": "Not found"}
    data = ingestions[ingestion_id]
    return {
        "ingestion_id": ingestion_id,
        "status": get_ingestion_status(ingestion_id, data),
        "batches": data["batches"]
    }
