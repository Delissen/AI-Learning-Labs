from shared.openai_client import client
from shared.config import AZURE_OPENAI_DEPLOYMENT

response = client.responses.create(
    model=AZURE_OPENAI_DEPLOYMENT,
    input="Zeg hallo tegen Maarten."
)

print(response.output_text)
