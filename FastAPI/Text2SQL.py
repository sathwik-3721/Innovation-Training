import os
import streamlit as st
import time
import sqlite3
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
st.set_page_config(page_title="Code finder and Optimizer")
st.title("Text to SQL")

input_text = st.text_input("Enter the text to convert into query. ")

prompt = f"""You are an Expert in converting the Natural Language text into SQL Query. 
            Now your task is to convert the given Natural Language text to SQL Query.
            The Natural Language text input is {input_text}
            The output must be in the following format:
            Generated Query: 
            Expected Output/ Estimated Output: print the example table output for the query generated
            Explanation:"""


def get_gemini_response():
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text


# Function to stream the response
def stream_data(data):
    for word in data.split(" "):
        yield word + " "
        time.sleep(0.05)


def table_info():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(Employee_Details)")
    columns = cursor.fetchall()
    conn.close()
    return columns


def sql_query(sql):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    data = cursor.execute(sql)
    return data


if prompt and st.button("Convert"):
    st.write_stream(stream_data(get_gemini_response()))
    # st.write_stream(stream_data(sql_query(get_gemini_response())))
    st.write(table_info())
