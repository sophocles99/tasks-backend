from bson import ObjectId
from server.database import student_collection

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
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        return student_helper(student)
    return None


# update a student by id
async def update_student(id: str, update_dict: dict) -> dict | None:
    updated_student = await student_collection.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": update_dict}, return_document=True
    )
    return student_helper(updated_student)


# delete a student by id
async def remove_student(id: str) -> dict | None:
    student = student_collection.find_one_and_delete({"_id": ObjectId(id)})
    if student:
        return True
    return False
