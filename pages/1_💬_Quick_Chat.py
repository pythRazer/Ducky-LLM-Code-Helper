import streamlit as st

from services import prompts
from helpers import util

st.set_page_config(
    page_title="Quick Chat",
    page_icon="💬",
    layout="wide"
)

import helpers.sidebar
import asyncio

helpers.sidebar.show()

st.header("Quick Chat")
st.write("Get instant answers to your software development and coding questions.")
# ask_book = st.checkbox("Ask the Pragmatic Programmer book?", value=False)

# Ensure the session state is initialized
if "messages" not in st.session_state:
    initial_messages = [{"role": "system",
                         "content": prompts.quick_chat_system_prompt()}]
    st.session_state.messages = initial_messages

# Print all messages in the session state
for message in [m for m in st.session_state.messages if m["role"] != "system"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# React to the user prompt
if prompt := st.chat_input("Ask a software development or coding question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    # if ask_book:
    #     asyncio.run(util.ask_book(st.session_state.messages, prompt))
    asyncio.run(util.chat(st.session_state.messages, prompt))
