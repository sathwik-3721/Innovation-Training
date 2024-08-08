# Import the required modules
import os
import time
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the Streamlit app
st.set_page_config(page_title="Basic Chatbot Application")
st.header("Basic Chatbot Application Using Gemini")


# Function to stream the response
def stream_data(data):
    for word in data.split(" "):
        yield word + " "
        time.sleep(0.05)


# Function to get the Gemini response
def get_gemini_response(question):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(question)
    return response.text


# Function to handle chat messages
def display_result():
    # Create placeholders for chat messages
    user_message_placeholder = st.empty()
    assistant_message_placeholder = st.empty()

    # Take user input
    question = st.chat_input("Enter your question", key="unique_chat_input_key")

    if question:
        # Display user message
        user_message_placeholder.chat_message("human").write(question)

        # Get and display the response
        response = get_gemini_response(question)
        assistant_message_placeholder.chat_message("assistant").write_stream(stream_data(response))

    else:
        # Inform the user to enter a question
        user_message_placeholder.chat_message("human").info("Please enter your question")


# Main function
def main():
    # Continuously display results based on user input
    display_result()


if __name__ == "__main__":
    main()
