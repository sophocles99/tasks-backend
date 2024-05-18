from motor import motor_asyncio

MONGO_URI = "mongodb://localhost:27017"

client = motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.students
student_collection = db.get_collection("students_collection")


# helpers
def student_helper(student) -> dict:
    return {
        "id": str(student["_id"]),
        "fullname": student["fullname"],
        "email": student["email"],
        "course_of_study": student["course_of_study"],
        "year": student["year"],
        "gpa": student["gpa"],
    }
