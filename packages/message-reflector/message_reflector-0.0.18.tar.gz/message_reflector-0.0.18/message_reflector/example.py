import streamlit as st
from message_reflector import message_reflector
import time
import uuid
st.title("Message Reflector")

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = f"Hello {time.time()}"

if "latest_pending_prompt" not in st.session_state:
    st.session_state.latest_pending_prompt = None

st.write("session_state")
st.write(st.session_state)

if st.button("Set Prompt"):
    st.session_state.pending_prompt = f"Hello {time.time()}"


def stream_out(prompt):
    for i in range(1):
        yield f"{prompt}@{i}"
        time.sleep(1)

def generate_response(prompt):
    with st.chat_message("user"):
        st.write(prompt)
    st.write_stream(stream_out(prompt))

if pending_prompt := message_reflector(st.session_state.pending_prompt, delay_ms=1000, key="reflected_message"):
    if pending_prompt != st.session_state.latest_pending_prompt:
        st.session_state.latest_pending_prompt = pending_prompt
        generate_response(pending_prompt)
    else:
        st.warning(f"reflector not changed: {pending_prompt}")
else:
    st.warning("reflector is none")


if prompt := st.chat_input("Enter a message"):
    generate_response(prompt)
    




if st.button("Refresh"):
    st.rerun()
