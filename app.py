import streamlit as st

st.title("Ask the Video")

st.write("A Youtube video text mining app which will help you to find the answers \
         to your questions on the youtube videos you want to.")

st.text_input(label = "Video Id", 
              key="video_id", 
              on_change = lambda: st.write(st.session_state.video_id),  
              placeholder= "For example FgakZw6K1QQ from the url \
              https://www.youtube.com/watch?v=FgakZw6K1QQ")


