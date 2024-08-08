# Import the modules required
import streamlit as st
import time

welcome = ("Welcome to the demo streamlit application. Here you can see the demo for some of the functionalities like "
           "write, write_stream and many more functionalities. If any doubts refer to streamlit's official "
           "documentation --> docs.streamlit.io")


def stream_data(data):
    for word in data.split(" "):
        yield word + " "
        time.sleep(0.05)


def streamlit_app():
    st.header("Basic Chat Application")
    # st.write("Hello Streamlit", unsafe_allow_html=False)
    # st.write("<h1>This is a Heading</h1> <p>This is a paragraph.</p>", unsafe_allow_html=True)
    st.write("Do you want to see the demo of the write_stream ?")
    if st.button("Demo"):
        st.write_stream(stream_data(welcome))
        st.write_stream(stream_data("You can chat below"))


if __name__ == '__main__':
    streamlit_app()
