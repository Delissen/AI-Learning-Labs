"""
AI-103 Lab 02 - Code Interpreter

Doel:
- Gebruik maken van de Code Interpreter tool
- Python code laten uitvoeren door het model
- Tool Calling demonstreren
"""

from shared.openai_client import client
from shared.config import AZURE_OPENAI_DEPLOYMENT

print("Using deployment:", AZURE_OPENAI_DEPLOYMENT)

try:

    response = client.responses.create(
        model=AZURE_OPENAI_DEPLOYMENT,

        instructions=
        """
        You are a helpful AI assistant.

        Use the Code Interpreter tool whenever calculations are required.
        """,

        input="What is the square root of 1024?",

        tools=[
            {
                "type": "code_interpreter",
                "container": {
                    "type": "auto"
                }
            }
        ]
    )

    print("\n=== Code Interpreter Response ===")
    print(response.output_text)

except Exception as ex:

    import traceback

    print("\n=== Exception ===")
    print(type(ex).__name__)
    print(ex)

    traceback.print_exc()
