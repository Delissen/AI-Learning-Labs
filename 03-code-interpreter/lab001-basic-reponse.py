"""
AI-103 Lab 01 - Basic Response

Doel:
- Verbinding maken met Azure OpenAI
- Een eenvoudige prompt uitvoeren
- Testen van deployment, endpoint en API key
"""

from shared.openai_client import client
from shared.config import AZURE_OPENAI_DEPLOYMENT

print("Using deployment:", AZURE_OPENAI_DEPLOYMENT)

response = client.responses.create(
    model=AZURE_OPENAI_DEPLOYMENT,
    input="Say hello to Maarten in Dutch."
)

print("\n=== Response ===")
print(response.output_text)
