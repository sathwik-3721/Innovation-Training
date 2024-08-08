# Import the required modules
import os
import mysql.connector
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# DB config file
config = { 
    'host' : "localhost",
    'user' : "root",
    'password' : "root", 
    'database' : "pydb"
}

def get_table_info(config):
    schema = ""
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("DESCRIBE Employee")
    td = cursor.fetchall()
    for col in td:
        schema += str(col)
    return schema

app = FastAPI(title="Text to SQL query generator")

class TextInput(BaseModel):
    textinput: str

class CodeResponse(BaseModel):
    result: str

@app.post("/find", response_model=CodeResponse)
def func_tool(req: TextInput):
    enter_text = req.textinput

    # Get database schema
    schema = get_table_info()
    print(schema)

    prompt = f"""You are a technical assistant. Given a text, understand the problem statement and generate a SQL query based on the input provided.
                 If no specific data is provided in the text, demonstrate the generated query with static data.
                 The text given by the user is: {enter_text}
                 The database schema is as follows:
                 {schema}
                 If the user input is not related to the database schema return the response like "Please ask the queries related to this table only" """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return CodeResponse(result=response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
