import os
import mysql.connector
import google.generativeai as genai
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# DB config file
config = { 
    'host': "localhost",
    'user': "root",
    'password': "root", 
    'database': "pydb"
}


def get_table_info(config):
    schema = ""
    try:
        conn = mysql.connector.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )
        cursor = conn.cursor()
        cursor.execute("DESCRIBE Employee")
        td = cursor.fetchall()
        for col in td:
            schema += str(col) + "\n"
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return schema


app = FastAPI(title="Text to SQL query generator")


class TextInput(BaseModel):
    textinput: str


class CodeResponse(BaseModel):
    result: str


def get_table_output(query):
    print("2")
    result = ""
    try:
        conn = mysql.connector.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )
        cursor = conn.cursor()
        cursor.execute(query)
        td = cursor.fetchall()
        for col in td:
            result += str(col) + "\n"
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        conn.close()
        cursor.close()
    return result


@app.post("/find", response_model=CodeResponse)
def func_tool(req: TextInput):
    enter_text = req.textinput

    # Get database schema
    schema = get_table_info(config)
    print(schema)

    prompt = f"""You are a technical assistant. Given a text, understand the problem statement and generate a SQL query based on the input provided.
                 If no specific data is provided in the text, demonstrate the generated query with static data.
                 Table name is: Employee
                 The text given by the user is: {enter_text}
                 The database schema is as follows:
                 {schema}
                 If the user input is not related to the database schema return the response like "Please ask the queries related to this table only" """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        print("Response: ", response)
        print("Response Text", response.text)
        print("1")
        exe_query = response.text.replace("```", "")
        exe_query = exe_query.replace("sql", "")
        print(get_table_output(exe_query))
        print("formated query :", exe_query)
        query_output = get_table_output(exe_query)
        print("3")
        # return CodeResponse(request_body=response.text)
        return CodeResponse(result=response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6969)