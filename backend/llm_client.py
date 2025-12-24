from openai import AzureOpenAI

from backend.tools import get_tools
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

def call_llm(messages: list[dict]):
    llm_client = get_llm_client()
    response = llm_client.chat.completions.create(
        model=DEPLOYMENT_MODEL,
        messages=messages,
        tools=get_tools(),
        tool_choice="auto"
    )
    return response.choices[0].message.content


def call_llm_stream(messages: list[dict]):
    llm_client = get_llm_client()
    return llm_client.chat.completions.create(
        model=DEPLOYMENT_MODEL,
        messages=messages,
        stream=True,
        tools=get_tools(),
        tool_choice="auto"
    )