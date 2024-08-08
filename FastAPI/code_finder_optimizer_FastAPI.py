import os
import google.generativeai as genai
import time
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()


class CodeRequest(BaseModel):
    code_snippet: str
    find_function: str


# def stream_data(data: str):
#     for word in data.split(" "):
#         yield word + " "
#         time.sleep(0.05)


@app.post("/find/")
async def find_function_from_snippet(request: CodeRequest):
    code_snippet = request.code_snippet
    find_function = request.find_function

    prompt = f"""Given a code snippet and a function name or description, identify if the function exists in the 
                      code. If found, return only the block of function code along with the line number, else generate the function based on input. 
                      If the function exists but is not optimized, optimize it and return the improved code. 
                      The code snippet is : {code_snippet}
                      The function name or description is : {find_function}"""

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return {"response": response.text}


# find_function()
