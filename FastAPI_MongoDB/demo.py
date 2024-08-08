import uvicorn
from bson import ObjectId, json_util
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pydantic import BaseModel, Field
from typing import List

uri = "mongodb+srv://sathwik3721:FM8a2M9i2aaf5WPD@cluster0.snpfe.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Define the database and collection
db = client.EmployeeDemo
collection = db["Employee"]

app = FastAPI()


class Employee(BaseModel):
    id: int
    name: str
    dept: str


class EmployeeUpdate(BaseModel):
    id: int = None
    name: str = None
    dept: str = None


@app.get("/emp", response_model=List[Employee])
def get_employees():
    documents = list(collection.find({}, {"_id": 0}))
    return json_util.loads(json_util.dumps(documents))


@app.post("/emp", response_model=Employee)
def create_employee(employee: Employee):
    result = collection.insert_one(employee.dict())
    if not result.acknowledged:
        raise HTTPException(status_code=500, detail="Employee could not be created")
    return employee


@app.get("/emp/{employee_id}", response_model=Employee)
def get_employee(employee_id: str):
    document = collection.find_one({"_id": ObjectId(employee_id)})
    if not document:
        raise HTTPException(status_code=404, detail="Employee not found")
    return json_util.loads(json_util.dumps(document))


@app.put("/emp/{employee_id}", response_model=Employee)
def update_employee(employee_id: str, employee: EmployeeUpdate):
    updated_data = {k: v for k, v in employee.dict().items() if v is not None}
    result = collection.update_one({"_id": ObjectId(employee_id)}, {"$set": updated_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    document = collection.find_one({"_id": ObjectId(employee_id)})
    return json_util.loads(json_util.dumps(document))


@app.delete("/emp/{employee_id}")
def delete_employee(employee_id: str):
    result = collection.delete_one({"_id": ObjectId(employee_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"detail": "Employee deleted"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
