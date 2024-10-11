import streamlit as st

import helpers.sidebar
from helpers import util
from services import prompts
import asyncio
import re

st.set_page_config(
    page_title="Generate Code",
    page_icon="📄",
    layout="wide"
)

# Add comments to explain the purpose of the code sections

# Show sidebar
helpers.sidebar.show()
# Flag to track if new code was extracted
new_code_extracted = False


#############################################################################

st.write("Welcome to the code generator!")
st.write("This tool is designed to help you generate code for your software projects.")



# Initialize session state for messages if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_code" not in st.session_state:
    st.session_state.current_code = ""

# Initialize a unique key for the text area in the session state
if "text_area_key" not in st.session_state:
    st.session_state.text_area_key = 0
# Initialize a variable to track if the page has been reset
if "just_reset" not in st.session_state:
    st.session_state.just_reset = False

if "action" not in st.session_state:
    st.session_state.action = "Review"
# Code input area
code = st.text_area("Enter your code here",
                    value=st.session_state.current_code,
                    key=f"code_text_area_{st.session_state.text_area_key}",
                    height=300)
action_key = None
# Button to reset the page
reset_button = st.button("Reset the page")
if reset_button:
    st.session_state.current_code = ""
    st.session_state.messages = []
    st.session_state.text_area_key += 1  # Increment the key to make it unique
    st.session_state.action = "Review"
    st.experimental_rerun()


# This will default to "Review" after a reset, or persist the user's last selection otherwise
action = st.selectbox("Choose an action", ["Review", "Debug", "Modify"], index=["Review", "Debug", "Modify"].index(st.session_state.action))

# Update the action in session state
st.session_state.action = action
error_message = ""
modify_instruction = ""
# Additional input for Debug or Modify action
additional_input = ""

if action in ["Debug"]:
    error_message = st.text_input("Error message (optional)")
if action in ["Modify"]:
    if st.session_state.current_code == "":
        modify_instruction = st.text_input("Modify instructions (required)")
    else:
        modify_instruction = st.text_input("Follow up instructions (required)")

# Button to submit request
if st.button("Submit"):
    if (action == "Review"):
        # Append the user's action and code to the session state
        st.session_state.messages.append({
            "role": "user",
            "content": prompts.review_prompt(code)
        })
        asyncio.run(util.review_code(st.session_state.messages, prompts.review_prompt(code)))

    if (action == "Debug"):
        # Append the user's action and code to the session state
        st.session_state.messages.append({
            "role": "user",
            "content": prompts.debug_prompt(code, error_message)
        })
        asyncio.run(util.debug_code(st.session_state.messages, prompts.debug_prompt(code, error_message)))

    if (action == "Modify"):
        # Append the user's action and code to the session state
        st.session_state.messages.append({
            "role": "user",
            "content": prompts.modify_code_prompt(code, modify_instruction)
        })
        asyncio.run(util.modify_code(st.session_state.messages, prompts.modify_code_prompt(code, modify_instruction)))



code_extracted_flag = False
# Display and extract LLM's responses
for message in st.session_state.messages:
    if message["role"] == "assistant":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            extracted_code = re.findall(r"```(.*?)```", message["content"], re.DOTALL)
            if extracted_code and action == "Modify":
                code_extracted_flag = True
                st.session_state.current_code = extracted_code[0]
                follow_up_button = st.button("Update the code and follow up")
                st.session_state.messages = []  # Clear messages to avoid repetition
                if follow_up_button:
                    st.experimental_rerun()


