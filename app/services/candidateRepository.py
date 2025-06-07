from .mongoClient import collection

def upsert_candidate(session_id: str, field: str, value):
    """
    Upsert candidate data: update the given field's value,
    or insert a new document if it doesn't exist.
    """
    collection.update_one(
        {"session_id": session_id},
        {"$set": {field: value}},
        upsert=True
    )