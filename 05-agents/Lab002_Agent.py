"""
------------------------------------------------------------------------------
Lab002 - Azure AI Foundry Agent with Custom Function Tools

Course:
    Microsoft AI-103 - Develop AI Solutions on Microsoft Azure

Description:
    This lab demonstrates how to build an Azure AI Foundry Agent that can
    invoke custom Python functions (Function Tools) to retrieve information,
    perform calculations and generate reports.

Learning objectives:
    - Create an Azure AI Foundry Agent
    - Register Function Tools
    - Handle Function Calling
    - Process Responses API output
    - Maintain multi-turn conversations

Functions implemented:
    - next_visible_event()
    - calculate_observation_cost()
    - generate_observation_report()

Author:
    Maarten Delissen

------------------------------------------------------------------------------
"""
# Test prompt:

# Find me the next event I can see from South America and give me the cost for 5 hours of premium telescope time at normal priority.


import json
import os

from dotenv import load_dotenv

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FunctionTool
from azure.ai.projects.models import PromptAgentDefinition
from azure.identity import DefaultAzureCredential

from openai.types.responses.response_input_param import (
    FunctionCallOutput,
    ResponseInputParam,
)

from shared.config import (
    FOUNDRY_AGENT_NAME,
    FOUNDRY_MODEL_DEPLOYMENT,
    FOUNDRY_PROJECT_ENDPOINT,
)

from shared.Lab002_agent_custom_tools import (
    calculate_observation_cost,
    generate_observation_report,
    next_visible_event,
)

# =============================================================================
# Configuration
# =============================================================================

def validate_configuration() -> None:
    """
    Validate the required Azure AI Foundry configuration.
    """

    if not FOUNDRY_PROJECT_ENDPOINT:
        raise ValueError("FOUNDRY_PROJECT_ENDPOINT is missing.")

    if not FOUNDRY_MODEL_DEPLOYMENT:
        raise ValueError("FOUNDRY_MODEL_DEPLOYMENT is missing.")

    if not FOUNDRY_AGENT_NAME:
        raise ValueError("FOUNDRY_AGENT_NAME is missing.")

def create_project_client() -> AIProjectClient:
    """
    Create a connection to the Azure AI Foundry project.
    """

    credential = DefaultAzureCredential()

    return AIProjectClient(
        endpoint=FOUNDRY_PROJECT_ENDPOINT,
        credential=credential
    )

def create_openai_client(project_client):
    """
    Create an OpenAI client from the Azure AI Foundry project.
    """

    return project_client.get_openai_client()

# =============================================================================
# Console Helpers
# =============================================================================

def create_event_tool() -> FunctionTool:
    """
    Create the Function Tool that returns the next visible
    astronomical event for a given location.
    """

    return FunctionTool(
        name="next_visible_event",
        description="Get the next visible event in a given location.",
        parameters={
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": (
                        "Continent to find the next visible event "
                        "(e.g. north_america, south_america, australia)."
                    ),
                },
            },
            "required": ["location"],
            "additionalProperties": False,
        },
        strict=True,
    )

def create_cost_tool() -> FunctionTool:
    """
    Create the Function Tool that calculates
    telescope observation costs.
    """

    return FunctionTool(
        name="calculate_observation_cost",
        description=(
            "Calculate the cost of an observation based on the "
            "telescope tier, number of hours and priority."
        ),
        parameters={
            "type": "object",
            "properties": {
                "telescope_tier": {
                    "type": "string",
                    "description": (
                        "Telescope tier "
                        "(standard, advanced or premium)."
                    ),
                },
                "hours": {
                    "type": "number",
                    "description": "Number of observation hours.",
                },
                "priority": {
                    "type": "string",
                    "description": (
                        "Observation priority "
                        "(low, normal or high)."
                    ),
                },
            },
            "required": [
                "telescope_tier",
                "hours",
                "priority",
            ],
            "additionalProperties": False,
        },
        strict=True,
    )

def create_report_tool() -> FunctionTool:
    """
    Create the Function Tool that generates
    an observation report.
    """

    return FunctionTool(
        name="generate_observation_report",
        description="Generate an astronomical observation report.",
        parameters={
            "type": "object",
            "properties": {
                "event_name": {
                    "type": "string",
                    "description": "Astronomical event name.",
                },
                "location": {
                    "type": "string",
                    "description": "Observer location.",
                },
                "telescope_tier": {
                    "type": "string",
                    "description": "Telescope tier.",
                },
                "hours": {
                    "type": "number",
                    "description": "Observation duration.",
                },
                "priority": {
                    "type": "string",
                    "description": "Observation priority.",
                },
                "observer_name": {
                    "type": "string",
                    "description": "Observer name.",
                },
            },
            "required": [
                "event_name",
                "location",
                "telescope_tier",
                "hours",
                "priority",
                "observer_name",
            ],
            "additionalProperties": False,
        },
        strict=True,
    )


def main() -> None:
    """
    Application entry point.
    """

    # -------------------------------------------------------------------------
    # Initialisatie
    # -------------------------------------------------------------------------

    os.system("cls" if os.name == "nt" else "clear")

    load_dotenv()

    validate_configuration()

    print("Connecting to Azure AI Foundry...")

    credential = DefaultAzureCredential()

    project_client = AIProjectClient(
        endpoint=FOUNDRY_PROJECT_ENDPOINT,
        credential=credential,
    )

    openai_client = create_openai_client(project_client)

    # -------------------------------------------------------------------------
    # Maak de Function Tools
    # -------------------------------------------------------------------------

    event_tool = create_event_tool()

    cost_tool = create_cost_tool()

    report_tool = create_report_tool()

    # -------------------------------------------------------------------------
    # Maak de Agent
    # -------------------------------------------------------------------------

    print(f"Creating agent '{FOUNDRY_AGENT_NAME}'...")

    agent = project_client.agents.create_version(
        agent_name=FOUNDRY_AGENT_NAME,
        definition=PromptAgentDefinition(
            model=FOUNDRY_MODEL_DEPLOYMENT,
            instructions="""
            You are an astronomy observations assistant.

            Help users find astronomical events, calculate telescope costs
            and generate observation reports.

            Always use the available function tools whenever appropriate.
            """,
            tools=[
                event_tool,
                cost_tool,
                report_tool,
            ],
        ),
    )

    print("Agent created successfully.")

    # -------------------------------------------------------------------------
    # Start Conversation
    # -------------------------------------------------------------------------

    conversation = openai_client.conversations.create()

    print(f"Conversation created ({conversation.id})")

    input_list: ResponseInputParam = []

    print()
    print("=" * 60)
    print("Azure AI Foundry Astronomy Agent")
    print("=" * 60)
    print("Type 'quit' to exit.")
    print()

    # -------------------------------------------------------------------------
    # Chat Loop
    # -------------------------------------------------------------------------

    try:

        while True:

            user_input = input("USER: ").strip()

            if user_input.lower() == "quit":
                break

            if not user_input:
                continue

            openai_client.conversations.items.create(
                conversation_id=conversation.id,
                items=[
                    {
                        "type": "message",
                        "role": "user",
                        "content": user_input,
                    }
                ],
            )

            print("\nThinking...\n")

            response = openai_client.responses.create(
                conversation=conversation.id,
                extra_body={
                    "agent_reference": {
                        "name": agent.name,
                        "type": "agent_reference",
                    }
                },
                input=input_list,
            )

            if response.status == "failed":
                print(response.error)
                continue

            input_list.clear()

            for item in response.output:

                if item.type != "function_call":
                    continue

                result = None

                arguments = json.loads(item.arguments)

                if item.name == "next_visible_event":
                    result = next_visible_event(**arguments)

                elif item.name == "calculate_observation_cost":
                    result = calculate_observation_cost(**arguments)

                elif item.name == "generate_observation_report":
                    result = generate_observation_report(**arguments)

                input_list.append(
                    FunctionCallOutput(
                        type="function_call_output",
                        call_id=item.call_id,
                        output=result,
                    )
                )

            if input_list:

                response = openai_client.responses.create(
                    previous_response_id=response.id,
                    input=input_list,
                    extra_body={
                        "agent_reference": {
                            "name": agent.name,
                            "type": "agent_reference",
                        }
                    },
                )

            print(f"\nAGENT:\n{response.output_text}\n")

    finally:

        print("\nCleaning up...")

        project_client.agents.delete_version(
            agent_name=agent.name,
            agent_version=agent.version,
        )

        openai_client.close()
        project_client.close()
        credential.close()

        print("Done.")

if __name__ == '__main__': 
    main()
