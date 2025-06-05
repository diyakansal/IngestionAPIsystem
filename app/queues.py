from collections import defaultdict, deque
from uuid import uuid4
import time

priority_map = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}

ingestions = {}  # ingestion_id: dict
queue = []  # List of (priority, timestamp, ingestion_id, batch)

def add_to_queue(ingestion_id, priority, batches):
    timestamp = time.time()
    for batch in batches:
        queue.append((priority_map[priority], timestamp, ingestion_id, batch))
    queue.sort()
