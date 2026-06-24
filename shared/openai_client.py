from openai import OpenAI
from shared.config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_KEY
)

client = OpenAI(
    base_url=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY
)
