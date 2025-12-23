import os
from openai import AzureOpenAI
from dotenv import load_dotenv

client = None
DEPLOYMENT_MODEL = "gpt-4o"

def get_llm_client():
    load_dotenv()
    global client
    if client is None:
        client = AzureOpenAI(
            api_key        = os.environ["AZURE_OPENAI_API_KEY"],
            api_version    = os.environ["AZURE_OPENAI_API_VERSION"],
            azure_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"],
        )
    return client

def call_llm(messages: list[dict]):
    llm_client = get_llm_client()
    response = llm_client.chat.completions.create(
        model=DEPLOYMENT_MODEL,
        messages=messages
    )
    return response.choices[0].message.content


def call_llm_stream(messages: list[dict]):
    llm_client = get_llm_client()
    return llm_client.chat.completions.create(
        model=DEPLOYMENT_MODEL,
        messages=messages,
        stream=True
    )