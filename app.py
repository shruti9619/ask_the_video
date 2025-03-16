import streamlit as st
import time

from setup_configs import load_configs, get_logger
from engine import run_engine, load_llm_model, load_transcripts, load_retriever

logger = get_logger()

load_configs()


st.session_state.setdefault(
    "chat_history", [{"role": "assistant", "content": "How can I help you?"}]
)


def stream_response(response):
    logger.info("Getting chat response in app")
    model_response, success_flag = response[0], response[1]

    if success_flag:
        # stream the response
        response = st.write_stream(model_response)
    return response


st.set_page_config(
    page_title="Ask the Video",
    layout="wide",
)


st.title("Ask the Video")

st.write(
    "A Youtube video text mining app which will help you to find the answers \
         to your questions on the youtube videos you want to."
)

with st.sidebar:

    st.write("__Model to use__")
    llm_option = st.selectbox(
        label="Select LLM",
        options=["GPT-4"],
        key="llm_option",
    )
    st.write("__Enter the Video ID:__")
    with st.form("user_input"):
        st.text_input(
            label="__Video Id__",
            key="video_id",
            placeholder="For example FgakZw6K1QQ from the url \
        https://www.youtube.com/watch?v=FgakZw6K1QQ",
        )

        submit_button = st.form_submit_button(label="Load Video")

        if submit_button:
            with st.status("Loading transcripts...", expanded=True) as status:
                status.update(
                    label="Loading transcripts...", state="running", expanded=True
                )
                st.session_state.transcript = load_transcripts(
                    st.session_state.video_id
                )
                if st.session_state.transcript:
                    st.session_state.retriever = load_retriever(
                        st.session_state.transcript
                    )
                    status.update(
                        label="Transcripts Loaded", state="complete", expanded=True
                    )
                else:
                    status.update(
                        label="Transcripts Loading Failed", state="error", expanded=True
                    )


# Display chat messages from history on app rerun
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask the video!"):

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.status("Parsing Question...", expanded=True) as status:
            if st.session_state.llm_option == "GPT-4":
                llm = load_llm_model(model_type="OAI")

            status.update(
                label="Generating response...", state="running", expanded=True
            )
            response = run_engine(
                llm, st.session_state.retriever, prompt, st.session_state.chat_history
            )
            response = stream_response(response=response)
            status.update(label="Query Complete", state="complete", expanded=True)

    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    # Add assistant response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": response})
