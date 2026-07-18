import streamlit as st
from chatbot import get_response, cache_stats

st.title("The AI Workshop Customer Support")
st.write("Welcome! Ask me anything about our courses and bootcamps.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Type your question here..."):
    st.session_state.messages.append({"role": "user", "content": 
    prompt})
    with st.chat_message("user"):
        st.write(prompt)

    result = get_response(prompt)

    if result:
        with st.chat_message("assistant"):
            st.write(result["response_text"])
            if result["needs_human"]:
                st.warning("This has been flagged for human support.")
        st.session_state.messages.append({
            "role": "assistant",
            "content": result["response_text"]
        })