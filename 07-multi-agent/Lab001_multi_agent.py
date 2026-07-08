"""
===============================================================================
Lab 001 - Multi-Agent Orchestration with Microsoft Agent Framework
===============================================================================

Description
-----------
This sample demonstrates how to build a simple Multi-Agent solution by using the
Microsoft Agent Framework together with Azure AI Foundry.

Instead of using a single AI agent, this lab creates three specialized agents
that work together in a sequential workflow:

    1. Summarizer Agent
       Summarizes the customer feedback.

    2. Classifier Agent
       Classifies the feedback.

    3. Action Agent
       Recommends the next action.

The SequentialBuilder orchestrates the conversation between these agents. The
output from one agent becomes the input for the next agent.

Microsoft Learn Exercise
------------------------
https://microsoftlearning.github.io/mslearn-ai-agents/Instructions/Exercises/08-agent-framework-multi-agents.html

Sample Questions
----------------
Replace the feedback text with your own examples, for example:

1.
The application crashes every time I upload a photo.

2.
The dashboard looks great. Thank you for the latest improvements!

3.
Please add Microsoft Teams integration.

4.
The software is extremely slow after the latest update.

5.
The colors are confusing and the interface is difficult to use.

Learning Objectives
-------------------
- Create multiple AI agents
- Specialize agents with different responsibilities
- Build a Sequential Orchestration workflow
- Execute a Multi-Agent conversation
- Understand how agents collaborate
"""

import os
import asyncio
from pathlib import Path
from typing import cast

# -----------------------------------------------------------------------------
# Microsoft Agent Framework
# -----------------------------------------------------------------------------

# Message object used when reading the workflow output.
from agent_framework import Message

# Client used to connect to Azure AI Foundry.
from agent_framework.foundry import FoundryChatClient

# Sequential orchestration builder.
from agent_framework.orchestrations import SequentialBuilder

# Azure authentication
from azure.identity import AzureCliCredential

# Shared configuration (.env)
from shared.config import (
    FOUNDRY_PROJECT_ENDPOINT_MULTI,
    FOUNDRY_MODEL_DEPLOYMENT_MULTI,
    FOUNDRY_AGENT_NAME_MULTI,
)


async def main():

    # -------------------------------------------------------------------------
    # Agent Instructions
    # -------------------------------------------------------------------------
    # Each AI agent receives its own System Prompt.
    #
    # This is one of the strengths of a Multi-Agent architecture:
    #
    # - every agent has one responsibility
    # - prompts remain small
    # - agents become reusable
    # -------------------------------------------------------------------------

    summarizer_instructions = """
    Summarize the customer's feedback in one short sentence.
    Keep it neutral and concise.

    Example output:
    App crashes during photo upload.
    User praises dark mode feature.
    """

    classifier_instructions = """
    Classify the feedback as one of the following:

    - Positive
    - Negative
    - Feature request
    """

    action_instructions = """
    Based on the summary and classification, suggest the next action in one
    short sentence.

    Example output:

    Escalate as a high-priority bug for the mobile team.
    Log as positive feedback to share with design and marketing.
    Log as enhancement request for product backlog.
    """

    # -------------------------------------------------------------------------
    # Create the Azure AI Foundry Client
    # -------------------------------------------------------------------------
    #
    # AzureCliCredential reuses the Azure CLI login:
    #
    #     az login
    #
    # The FoundryChatClient connects to the Azure AI Foundry project and uses
    # the configured Azure OpenAI deployment.
    # -------------------------------------------------------------------------

    credential = AzureCliCredential()

    chat_client = FoundryChatClient(
        credential=credential,
        project_endpoint=FOUNDRY_PROJECT_ENDPOINT_MULTI,
        model=FOUNDRY_MODEL_DEPLOYMENT_MULTI,
    )

    # -------------------------------------------------------------------------
    # Create the AI Agents
    # -------------------------------------------------------------------------
    #
    # Each agent has:
    #
    # - a name
    # - its own System Prompt
    #
    # The agents are lightweight runtime agents. They are created when the
    # application starts and don't need to exist beforehand inside Azure AI
    # Foundry.
    # -------------------------------------------------------------------------

    summarizer_agent = chat_client.as_agent(
        name="summarizer",
        instructions=summarizer_instructions,
    )

    classifier_agent = chat_client.as_agent(
        name="classifier",
        instructions=classifier_instructions,
    )

    action_agent = chat_client.as_agent(
        name="action",
        instructions=action_instructions,
    )

    # -------------------------------------------------------------------------
    # Customer Feedback
    # -------------------------------------------------------------------------
    #
    # Replace this text with your own examples to experiment with the workflow.
    # -------------------------------------------------------------------------

    feedback = """
    I think the dashboard is very ugly. The colors are too bright and the
    layout is confusing. I hate working with it. Please make it more
    user-friendly and visually appealing.
    """

    # -------------------------------------------------------------------------
    # Build the Sequential Workflow
    # -------------------------------------------------------------------------
    #
    # Workflow:
    #
    # Customer Feedback
    #         │
    #         ▼
    #   Summarizer Agent
    #         │
    #         ▼
    #   Classifier Agent
    #         │
    #         ▼
    #     Action Agent
    #
    # output_from="all"
    #
    # Returns the output from every agent instead of only the final result.
    # -------------------------------------------------------------------------

    workflow = SequentialBuilder(
        participants=[
            summarizer_agent,
            classifier_agent,
            action_agent,
        ],
        output_from="all",
    ).build()

    # -------------------------------------------------------------------------
    # Execute the Workflow
    # -------------------------------------------------------------------------

    result = await workflow.run(
        f"Customer feedback:\n\n{feedback}"
    )

    outputs = result.get_outputs()

    # -------------------------------------------------------------------------
    # Display Results
    # -------------------------------------------------------------------------
    #
    # Every participating agent produces a response.
    #
    # The workflow returns these responses as Message objects.
    # -------------------------------------------------------------------------

    i = 1

    for response in outputs:

        for msg in cast(list[Message], response.messages):

            name = msg.author_name or (
                "assistant"
                if msg.role == "assistant"
                else "user"
            )

            print("-" * 60)
            print(f"{i:02d} [{name}]")
            print(msg.text)

            i += 1


# -----------------------------------------------------------------------------
# Application Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())