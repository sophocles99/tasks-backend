from motor import motor_asyncio

# not sure if this is necessary - depends whether Motor needs ObjectId type as parameter for find_one etc. methods
# from bson.objectid import ObjectId

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
async def create_student(student_data: dict) -> dict | None:
    insert_one_result = await student_collection.insert_one(student_data)
    student = await student_collection.find_one(insert_one_result.inserted_id)
    return student_helper(student)


# retrieve all students
async def retrieve_students() -> list[dict]:
    students = [student_helper(student) async for student in student_collection.find()]
    return students


# retrieve student by id
async def retrieve_student(id: str) -> dict | None:
    student = await student_collection.find({"_id": id})
    if student:
        return student_helper(student)
    return None


# update a student by id
async def update_student(id: str, data: dict) -> dict | None:
    # return False if an empty data dict is sent
    if len(data) == 0:
        return None
    student = await student_collection.find_one_and_update({"_id": id}, {"$set": data})
    return student_helper(student)


# delete a student by id
async def delete_student(id: str) -> dict | None:
    student = student_collection.find_one_and_delete({"_id": id})
    if student:
        return student_helper(student)
    return None
