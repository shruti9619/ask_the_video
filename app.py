import logging
import streamlit as st

from engine import run_engine

logging.root.setLevel(logging.INFO)
logger = logging.getLogger(__name__)

def get_chat(response):
    logger.info("Getting chat response in app")

    # stream the response
    with st.chat_message("AI"):
        #response = st.write_stream(response)
        for chunk in response:
            print(chunk, end="", flush=True)

st.title("Ask the Video")

st.write("A Youtube video text mining app which will help you to find the answers \
         to your questions on the youtube videos you want to.")



st.text_input(label = "Video Id", 
              key="video_id",  
              placeholder= "For example FgakZw6K1QQ from the url \
https://www.youtube.com/watch?v=FgakZw6K1QQ",
                value= "")

st.text_input(label = "Query/Instruction", 
              key="user_query",  
              placeholder= "For example: What is PCA?",
              )

if st.session_state.video_id and st.session_state.user_query:
    logger.info("Video Id and Query received")
    get_chat(run_engine(st.session_state.video_id, 
                        st.session_state.user_query))


