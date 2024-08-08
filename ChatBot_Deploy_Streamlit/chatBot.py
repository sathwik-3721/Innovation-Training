# Import the required modules
import os
import time
import streamlit as st
import google.generativeai as genai
# from dotenv import load_dotenv

# Load the environment variables
# load_dotenv()

# Configure the gemini in local
genai.configure(api_key="YOUR_GEMINI_API_KEY_HERE")

# Initialize the Streamlit app
st.set_page_config(page_title="Basic Chatbot Application")
st.header("Basic Chatbot Application Using Gemini")


# Function to stream the response
def stream_data(data):
    for word in data.split(" "):
        yield word + " "
        time.sleep(0.05)


# Function to take the user input
def user_input():
    # Provide a unique key to avoid duplicate widget IDs
    question = st.chat_input("Enter your question", key="unique_chat_input_key")
    return question


# Function to get the Gemini response
def get_gemini_response(question):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(question)
    return response.text


# Display the bot response
def display_result():
    chats = "chats"
    if chats not in st.session_state:
        st.session_state[chats] = ["How can I help you?"]
    for i, chat in enumerate(st.session_state[chats]):
        if i % 2 == 0:
            st.chat_message("assistant").write(chat)
        else:
            st.chat_message("human").write(chat)

    question = user_input()
    # Display the response genertated by the bot
    if question:
        st.session_state[chats].append(question)
        st.chat_message("human").write(question)
        response = get_gemini_response(question)
        st.session_state[chats].append(response)
        message = st.chat_message("assistant")
        message.write_stream(stream_data(response))

        # st.snow()


# Main function
def main():
    # Call display_result directly since user_input is called inside it
    display_result()


if __name__ == "__main__":
    main()
