from motor import motor_asyncio
from bson import ObjectId

MONGO_URI = "mongodb://localhost:27017"

client = motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.students
student_collection = db.get_collection("students_collection")


# helper
def student_helper(student) -> dict:
    return {
        "id": str(student["_id"]),
        "fullname": student["fullname"],
        "email": student["email"],
        "course_of_study": student["course_of_study"],
        "year": student["year"],
        "gpa": student["gpa"],
    }


# create student
async def create_student(student: dict) -> dict | None:
    insert_one_result = await student_collection.insert_one(student)
    new_student = await student_collection.find_one(insert_one_result.inserted_id)
    return student_helper(new_student)


# retrieve all students
async def retrieve_students() -> list[dict]:
    students = [student_helper(student) async for student in student_collection.find()]
    return students


# retrieve student by id
async def retrieve_student(id: str) -> dict | None:
    object_id = ObjectId(id)
    student = await student_collection.find_one({"_id": object_id})
    if student:
        return student_helper(student)
    return None


# update a student by id
async def update_student(id: str, update_dict: dict) -> dict | None:
    object_id = ObjectId(id)
    updated_student = await student_collection.find_one_and_update(
        {"_id": object_id}, {"$set": update_dict}, return_document=True
    )
    return student_helper(updated_student)


# delete a student by id
async def delete_student(id: str) -> dict | None:
    student = student_collection.find_one_and_delete({"_id": id})
    if student:
        return student_helper(student)
    return None
