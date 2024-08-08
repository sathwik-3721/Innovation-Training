import streamlit as st
import time


def stream_data(data):
    for words in data.split(" "):
        yield words + " "
        time.sleep(0.05)


# Create a placeholder to update the text in place
placeholder = st.empty()

dev = "I'm a Developer"
con = "I'm a Contributor"

# Infinite loop to cycle between 'dev' and 'con'
while True:
    # Display the 'dev' message
    placeholder.text(dev)
    time.sleep(2)  # Pause before switching to 'con'

    # Display the 'con' message
    # for word in stream_data(con):
    placeholder.text(con)
    time.sleep(2)  # Pause before repeating the cycle
