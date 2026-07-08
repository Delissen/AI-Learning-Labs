"""
===============================================================================
Lab 006 - Microsoft Agent Framework
===============================================================================

Description
-----------
This lab demonstrates how to build an AI Agent by using the Microsoft Agent
Framework together with Azure AI Foundry.

The agent receives expense data from a text file and uses Automatic Function
Calling to invoke a custom tool that submits an expense claim.

Concepts demonstrated
---------------------
- Microsoft Agent Framework
- Azure AI Foundry
- FoundryChatClient
- Agent
- Agent Instructions (System Prompt)
- Automatic Function Calling
- Custom Tools
- AzureCliCredential authentication

Microsoft Learn Lab
-------------------
https://microsoftlearning.github.io/mslearn-ai-agents/Instructions/Exercises/07-agent-framework.html

Sample questions
----------------
Submit an expense claim.

Create an expense report.

Please submit these expenses.

Can you create my expense claim?

===============================================================================
"""

import os
import asyncio
from pathlib import Path
from typing import Annotated

from dotenv import load_dotenv
from azure.identity import AzureCliCredential
from pydantic import Field

# Microsoft Agent Framework
from agent_framework import Agent, tool
from agent_framework.foundry import FoundryChatClient

# Shared configuration
from shared.config import (
    FOUNDRY_AGENT_NAME,
    FOUNDRY_MODEL_DEPLOYMENT,
    FOUNDRY_PROJECT_ENDPOINT,
)

# Load environment variables (.env)
load_dotenv()


async def main():
    """
    Entry point of the application.

    This function:

    1. Clears the console.
    2. Loads the sample expense data.
    3. Asks the user what should be done.
    4. Sends everything to the AI Agent.
    """

    os.system("cls" if os.name == "nt" else "clear")

    # Read the sample expense file that will be supplied to the agent.
    script_dir = Path(__file__).parent
    file_path = script_dir / "data.txt"

    with file_path.open("r", encoding="utf-8") as file:
        expenses_data = file.read()

    # Ask the user what to do with the provided expenses.
    user_prompt = input(
        f"""
Here are the expenses contained in the file:

{expenses_data}

What would you like me to do with them?

> """
    )

    await process_expenses_data(user_prompt, expenses_data)


async def process_expenses_data(prompt: str, expenses_data: str):
    """
    Creates and executes a Microsoft Foundry Agent.

    Steps:

    1. Connect to Azure AI Foundry.
    2. Create an Agent.
    3. Register the custom Tool.
    4. Send the user prompt.
    5. Receive and display the response.

    Automatic Function Calling will determine whether the
    submit_claim() tool should be executed.
    """

    # ------------------------------------------------------------------
    # Create a client that connects to the Azure AI Foundry project.
    #
    # AzureCliCredential uses the Azure CLI login that was performed
    # earlier with:
    #
    #     az login
    #
    # ------------------------------------------------------------------

    client = FoundryChatClient(
        project_endpoint=FOUNDRY_PROJECT_ENDPOINT,
        model=FOUNDRY_MODEL_DEPLOYMENT,
        credential=AzureCliCredential(),
    )

    # ------------------------------------------------------------------
    # Create the AI Agent.
    #
    # Instructions define the permanent behaviour of the agent.
    #
    # Tools extend the capabilities of the LLM by allowing it to execute
    # Python functions automatically through Function Calling.
    # ------------------------------------------------------------------

    async with Agent(
        client=client,
        name=FOUNDRY_AGENT_NAME,
        instructions="""
You are an AI assistant responsible for processing expense claims.

When the user requests an expense claim:

1. Analyse the supplied expense data.
2. Create an itemised expense report.
3. Call the submit_claim tool.
4. Send the email to expenses@arcadiuz.com.
5. Use 'Expense Claim' as the subject.
6. Confirm to the user that the claim has been submitted.

Do not ask the user for additional information.
Only use the information that is already available.
""",
        tools=[submit_claim],
    ) as agent:

        try:

            # Create the conversation.
            prompt_messages = [f"{prompt}\n\nExpense data:\n{expenses_data}"]

            # Invoke the agent.
            response = await agent.run(prompt_messages)

            print("\n===================================================")
            print("Agent Response")
            print("===================================================\n")
            print(response)

        except Exception as ex:
            print("\nError")
            print("-----")
            print(ex)


# =============================================================================
# Custom Tool
# =============================================================================

@tool(approval_mode="never_require")
def submit_claim(
    to: Annotated[
        str,
        Field(description="Recipient of the expense claim email."),
    ],
    subject: Annotated[
        str,
        Field(description="Email subject."),
    ],
    body: Annotated[
        str,
        Field(description="Email body containing the expense report."),
    ],
):
    """
    Simulates sending an expense claim.

    This function is exposed to the AI model through the @tool decorator.

    The LLM determines automatically when this function should be called.
    The developer never calls this function directly.

    Parameters
    ----------
    to
        Recipient email address.

    subject
        Email subject.

    body
        Expense claim body.
    """

    print("\n===================================================")
    print("Expense Claim Tool")
    print("===================================================")

    print(f"\nTo      : {to}")
    print(f"Subject : {subject}")
    print(f"\n{body}\n")

    return "Expense claim email successfully prepared and sent."


if __name__ == "__main__":
    asyncio.run(main())