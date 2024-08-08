import os
import time
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
st.set_page_config(page_title="Code finder and Optimizer")

st.title("Code finder and Optimizer")

code_snippet = st.text_area("Enter/Paste the Code snippet")
function_input = st.text_input("Enter the function name or description to search for. If function not present, "
                               "plz mention description")

prompt = f"""Given a code snippet and a function name or description, identify if the function exists in the 
             code. If found, return only the block of function code along with the line number, else generate the function based on input. 
             If the function exists but is not  optimized, optimize it and return the improved code. 
             The code snippet is : {code_snippet}
             The function name or description is : {function_input}"""


def get_gemini_response():
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text


# Function to stream the response
def stream_data(data):
    for word in data.split(" "):
        yield word + " "
        time.sleep(0.05)


if st.button("Find"):
    st.write_stream(stream_data(get_gemini_response()))
