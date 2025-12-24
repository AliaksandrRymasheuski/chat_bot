import streamlit as st

from components.chat import chat_interface


def main():
    st.title("Event Management Assistant")
    st.markdown("Ask me anything about company events!")

    with st.sidebar:
        st.header("Settings")

        # Streaming toggle
        use_streaming = st.toggle("Enable Streaming", value=True,
                                  help="Stream responses word by word")

    chat_interface(use_stream=use_streaming)


if __name__ == "__main__":
    main()