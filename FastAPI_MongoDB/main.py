import uvicorn
from bson import json_util
from fastapi import FastAPI
from pymongo import MongoClient
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

# Define the database and collection
db = client.EmployeeDemo
collection = db["Employee"]

app = FastAPI()


# @app.get("/emp")
# def get_employee():
#     documents = list(collection.find({}))
#     return json_util.dumps(documents)  # Convert documents to JSON string


@app.get("/emp")
def get_employee():
    # Use projection to specify only the fields you want to include
    documents = list(collection.find({"_id": 0}))
    # Convert documents to JSON string
    return json_util.dumps(documents)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)