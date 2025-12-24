import streamlit as st

from components.chat import chat_interface


def main():
    st.title("Event Management Assistant")
    st.markdown("Ask me anything about company events!")

    chat_interface()

if __name__ == "__main__":
    main()