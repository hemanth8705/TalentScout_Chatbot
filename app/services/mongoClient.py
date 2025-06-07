import pymongo

MONGO_URI = "mongodb://localhost:27017"
client = pymongo.MongoClient(MONGO_URI)
db = client["talent_scout"]  # Use a database name of your choice
collection = db["candidates"]