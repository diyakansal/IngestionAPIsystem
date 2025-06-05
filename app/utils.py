from uuid import uuid4

def batch_ids(ids, batch_size=3):
    for i in range(0, len(ids), batch_size):
        yield ids[i:i+batch_size]

def generate_batches(ids):
    return [{"batch_id": str(uuid4()), "ids": batch, "status": "yet_to_start"} for batch in batch_ids(ids)]

def get_ingestion_status(ingestion_id, data):
    statuses = [batch['status'] for batch in data['batches']]
    if all(s == "yet_to_start" for s in statuses):
        return "yet_to_start"
    elif all(s == "completed" for s in statuses):
        return "completed"
    else:
        return "triggered"
