# ============================================================================
# Lab003 - MCP Integration (Remote MCP Server)
# ============================================================================
#
# Description
# -----------
# Demonstrates how an Azure AI Agent uses the Model Context Protocol (MCP)
# to dynamically discover and invoke tools exposed by a remote MCP server.
#
# Demonstrates how an Azure AI Agent connects to a remote MCP server
# (Microsoft Learn MCP Server) and dynamically invokes MCP tools.
#
# Link: https://microsoftlearning.github.io/mslearn-ai-agents/Instructions/Exercises/03-mcp-integration.html
#
# Scenario
# --------
# The agent connects to the Microsoft Learn MCP Server to retrieve
# official Microsoft documentation and code samples.
#
# Learning Objectives
# -------------------
# - Create an Azure AI Agent
# - Connect to a remote MCP server
# - Handle MCP approval requests
# - Execute multiple MCP tool calls
# - Return the final grounded response
#
# ============================================================================

#
# Flow:
#   User Prompt
#       ↓
#   Azure AI Agent
#       ↓
#   MCP Approval
#       ↓
#   Microsoft Learn MCP Server
#       ↓
#   Tool Execution
#       ↓
#   Final Response
# ============================================================================

import os
from dotenv import load_dotenv

# Azure AI Foundry
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, MCPTool

# OpenAI Response API
from openai.types.responses.response_input_param import (
    McpApprovalResponse,
    ResponseInputParam,
)

# Shared configuration
from shared.config import (
    FOUNDRY_MODEL_DEPLOYMENT,
    FOUNDRY_PROJECT_ENDPOINT,
)

# ---------------------------------------------------------------------------
# Load configuration
# ---------------------------------------------------------------------------

load_dotenv()

project_endpoint = FOUNDRY_PROJECT_ENDPOINT
model_deployment = FOUNDRY_MODEL_DEPLOYMENT


# ---------------------------------------------------------------------------
# Connect to Azure AI Foundry
# ---------------------------------------------------------------------------

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(
        endpoint=project_endpoint,
        credential=credential,
    ) as project_client,
    project_client.get_openai_client() as openai_client,
):

    # -----------------------------------------------------------------------
    # Register the remote Microsoft Learn MCP Server.
    #
    # This server exposes several tools such as:
    # - microsoft_docs_search
    # - microsoft_docs_fetch
    # - microsoft_code_sample_search
    #
    # Setting require_approval="always" means the agent must ask permission
    # before every MCP tool invocation.
    # -----------------------------------------------------------------------

    mcp_tool = MCPTool(
        server_label="api-specs",
        server_url="https://learn.microsoft.com/api/mcp",
        require_approval="always",
    )

    # -----------------------------------------------------------------------
    # Create a Prompt Agent and attach the MCP server.
    # From this point the agent can dynamically discover and use the MCP tools.
    # -----------------------------------------------------------------------

    agent = project_client.agents.create_version(
        agent_name="MyAgent",
        definition=PromptAgentDefinition(
            model=model_deployment,
            instructions=(
                "You are a helpful assistant that can use MCP tools "
                "to answer questions about Microsoft products."
            ),
            tools=[mcp_tool],
        ),
    )

    print(f"Agent created: {agent.name}")

    # -----------------------------------------------------------------------
    # Start a new conversation.
    # The conversation stores the history of all prompts and responses.
    # -----------------------------------------------------------------------

    conversation = openai_client.conversations.create()

    # -----------------------------------------------------------------------
    # Ask the first question.
    #
    # The model now decides whether it can answer itself or whether it needs
    # one of the MCP tools.
    # -----------------------------------------------------------------------

    response = openai_client.responses.create(
        conversation=conversation.id,
        input="Give me the Azure CLI commands to create an Azure Container App with a managed identity.",
        extra_body={
            "agent_reference": {
                "name": agent.name,
                "type": "agent_reference",
            }
        },
    )

    # -----------------------------------------------------------------------
    # Process all approval requests returned by the model.
    #
    # Because require_approval="always" is enabled, the model cannot execute
    # an MCP tool without explicit approval.
    # -----------------------------------------------------------------------

    input_list: ResponseInputParam = []

    for item in response.output:

        if item.type == "mcp_approval_request":

            input_list.append(
                McpApprovalResponse(
                    type="mcp_approval_response",
                    approve=True,
                    approval_request_id=item.id,
                )
            )

    # -----------------------------------------------------------------------
    # Continue the conversation.
    #
    # Some MCP servers require multiple tool calls.
    #
    # Example:
    #
    # Search documentation
    #        ↓
    # Fetch complete article
    #        ↓
    # Generate final answer
    #
    # Therefore we keep approving requests until no more approvals are needed.
    # -----------------------------------------------------------------------

    while True:

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

        # Prepare a new approval list for the next iteration.
        input_list = []

        # Check whether the model wants to execute another MCP tool.
        for item in response.output:

            if item.type == "mcp_approval_request":

                input_list.append(
                    McpApprovalResponse(
                        type="mcp_approval_response",
                        approve=True,
                        approval_request_id=item.id,
                    )
                )

        # When no approval requests remain, the model has finished.
        if not input_list:
            break

    # -----------------------------------------------------------------------
    # Display the final answer generated by the agent.
    # -----------------------------------------------------------------------

    print("\nAgent response:")
    print(response.output_text)

    # -----------------------------------------------------------------------
    # Remove the temporary agent.
    # This keeps the Azure AI Foundry project clean.
    # -----------------------------------------------------------------------

    project_client.agents.delete_version(
        agent_name=agent.name,
        agent_version=agent.version,
    )

    print("\nAgent deleted.")