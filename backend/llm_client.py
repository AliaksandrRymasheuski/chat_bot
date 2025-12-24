import json
from openai import AzureOpenAI
from typing import List, Dict, Any
from backend.tools import get_tools, execute_function_call
from config.settings import AZURE_OPENAI_API_KEY, AZURE_OPENAI_API_VERSION, AZURE_OPENAI_ENDPOINT

client = None
DEPLOYMENT_MODEL = "gpt-4o"

def get_llm_client():
    global client
    if client is None:
        client = AzureOpenAI(
            api_key        = AZURE_OPENAI_API_KEY,
            api_version    = AZURE_OPENAI_API_VERSION,
            azure_endpoint = AZURE_OPENAI_ENDPOINT,
        )
    return client

def call_llm(messages: List[Dict[str, Any]], max_iterations: int = 5):
    """
    Send messages and handle function calling automatically.
    Works with external conversation history (like Streamlit session state).

    Args:
        messages: List of message dictionaries with 'role' and 'content'
        max_iterations: Maximum number of function call iterations

    Returns:
        The assistant's final response as a string
    """
    llm_client = get_llm_client()

    # Create a working copy of messages for function calling
    working_messages = messages.copy()
    iteration = 0

    while iteration < max_iterations:
        iteration += 1

        response = llm_client.chat.completions.create(
            model=DEPLOYMENT_MODEL,
            messages=working_messages,
            tools=get_tools(),
            tool_choice="auto"
        )

        assistant_message = response.choices[0].message

        if assistant_message.tool_calls:
            # Add assistant message with tool calls to working messages
            working_messages.append({
                "role": "assistant",
                "content": assistant_message.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    } for tc in assistant_message.tool_calls
                ]
            })

            # Execute each function call
            for tool_call in assistant_message.tool_calls:
                function_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                # Execute the function
                function_response = execute_function_call(function_name, arguments)

                # Add function response to working messages
                working_messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": function_response
                })

            # Continue loop to get final response
            continue
        else:
            # No function call, return the response
            return assistant_message.content or ""

    return "Maximum iterations reached. Please try rephrasing your question."



def call_llm_stream(messages: list[dict]):
    llm_client = get_llm_client()
    return llm_client.chat.completions.create(
        model=DEPLOYMENT_MODEL,
        messages=messages,
        stream=True,
        tools=get_tools(),
        tool_choice="auto"
    )