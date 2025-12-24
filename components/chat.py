import streamlit as st

from backend.llm_client import call_llm

SYSTEM_PROMPT = """You are a helpful event management assistant that answers questions about company events.

Your responsibilities:
- Answer questions about upcoming company events, attendee counts, and scheduling
- Provide information from the events database when available
- Be polite, concise, and professional

Your limitations:
- Only answer questions related to company events
- Politely decline requests unrelated to events
- Do not perform unauthorized database operations (only SELECT queries are allowed)

If a user asks something outside your scope, politely explain that you can only help with company events information."""


def display_queries(queries):
    """Display executed SQL queries in a collapsible section."""
    if not queries:
        return

    with st.expander(f"🔍 View SQL Queries ({len(queries)} executed)", expanded=False):
        for idx, query_info in enumerate(queries, 1):
            st.markdown(f"**Query {idx}:**")

            # Show explanation if available
            if query_info.get("explanation") and query_info["explanation"] != "N/A":
                st.info(f"📝 {query_info['explanation']}")

            # Show the SQL query with syntax highlighting
            st.code(query_info.get("query", "N/A"), language="sql")

            # Show execution result
            if query_info.get("success"):
                st.success(f"✅ Success: {query_info.get('row_count', 0)} rows returned")
            elif query_info.get("error"):
                st.error(f"❌ Error: {query_info['error']}")

            if idx < len(queries):
                st.divider()

def chat_interface():
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system",
                                      "content": SYSTEM_PROMPT}]

        # Initialize queries history
    if "queries_history" not in st.session_state:
        st.session_state.queries_history = []

    # Display chat history (skip system message)
    assistant_msg_idx = 0
    for message in st.session_state.messages:
        if message["role"] == "system":
            continue

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            # Show queries for assistant messages
            if message["role"] == "assistant":
                if assistant_msg_idx < len(st.session_state.queries_history):
                    queries = st.session_state.queries_history[assistant_msg_idx]
                    if queries:
                        display_queries(queries)
                assistant_msg_idx += 1

    prompt = st.chat_input("Ask me about company events...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                with st.spinner("Thinking..."):
                    response, executed_queries = call_llm(st.session_state.messages)
                st.markdown(response)
                # Display executed queries
                if executed_queries:
                    display_queries(executed_queries)

                st.session_state.messages.append({"role": "assistant", "content": response})

                # Store queries for this message
                st.session_state.queries_history.append(executed_queries)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                # Remove the user message if there was an error
                if st.session_state.messages[-1]["role"] == "user":
                    st.session_state.messages.pop()

