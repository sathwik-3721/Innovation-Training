from fastapi import FastAPI
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://sathwik3721:FM8a2M9i2aaf5WPD@cluster0.snpfe.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.EmployeeDemo
collection = db["Employee"]

emp_details = [
    {
        "id": 1,
        "name": "sai",
        "dept": "Labs"
    },
    {
        "id": 2,
        "name": "sri",
        "dept": "MApps"
    },
    {
        "id": 3,
        "name": "ram",
        "dept": "DB"
    },
    {
        "id": 4,
        "name": "John",
        "dept": "DB"
    },
    {
        "id": 5,
        "name": "Jack",
        "dept": "Labs"
    },
    {
        "id": 6,
        "name": "Jane",
        "dept": "DB"
    }
]

result = collection.insert_many(emp_details)
print(result)
# inserted_count =
# app = FastAPI()
#
# @app.get("/emp")
# async def root():
#     db = client.EmployeeDB
#     collection = db.Employee
