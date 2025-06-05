import asyncio
import time
from app.queues import queue, ingestions
import threading

async def mock_api_call(id):
    await asyncio.sleep(1)
    return {"id": id, "data": "processed"}

async def process_batch(ingestion_id, batch):
    batch["status"] = "triggered"
    await asyncio.gather(*[mock_api_call(i) for i in batch["ids"]])
    batch["status"] = "completed"

async def scheduler():
    while True:
        if queue:
            _, _, ingestion_id, batch = queue.pop(0)
            await process_batch(ingestion_id, batch)
        await asyncio.sleep(5)

def start_scheduler():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(scheduler())

threading.Thread(target=start_scheduler, daemon=True).start()
