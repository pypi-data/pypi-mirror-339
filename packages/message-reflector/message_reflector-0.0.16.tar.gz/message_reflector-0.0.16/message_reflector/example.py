import streamlit as st
from message_reflector import message_reflector
import time
import uuid
st.title("Message Reflector")

if "prompt" not in st.session_state:
    st.session_state.prompt = f"Hello {time.time()}"

st.write(f"prompt: {st.session_state.prompt}")

r = message_reflector(st.session_state.prompt, delay_ms=5000, key="reflected_message")

st.write(f"reflected r: {r}")

st.write("session_state")
st.write(st.session_state)

if st.button("Set Prompt"):
    st.session_state.prompt = f"Hello {time.time()}"


if st.button("Refresh"):
    pass



