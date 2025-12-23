import streamlit as st

from components.chat import chat_interface


def main():
    st.title("Graduate project chat")

    chat_interface(use_stream=True)


if __name__ == "__main__":
    main()