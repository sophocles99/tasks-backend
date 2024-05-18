from motor import motor_asyncio

MONGO_URI = "mongodb://localhost:27017"

client = motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.students
student_collection = db.get_collection("students_collection")
