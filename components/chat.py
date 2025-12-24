import streamlit as st

from backend.llm_client import call_llm, call_llm_stream


def chat_interface(use_stream: bool = False):
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system",
                                      "content": "You are a helpful event management assistant."
                                                 "You should be able to answer user's questions about upcoming company events,"
                                                 "attendee counts and scheduling."
                                                 "You should not answer user's questions not not related to company events."
                                                 "Be polite and concise."
                                                 "If user asks to perform actions that are not allowed - explicitly say that it's not allowed."}]

    for message in st.session_state.messages:
        if message["role"] == "system":
            continue
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("How can I help you?")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                if use_stream:
                    assistant_replied = call_llm_stream(st.session_state.messages)
                    response = st.write_stream(assistant_replied)
                else:
                    response = call_llm(st.session_state.messages)
                    st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

