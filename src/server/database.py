from motor import motor_asyncio

MONGO_URI = "mongodb://localhost:27017"

client = motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.tasks

student_collection = db.get_collection("students_collection")
task_collection = db.get_collection("task_collection")
