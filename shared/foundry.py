"""
shared/foundry.py

Shared helper functions for Azure AI Foundry.

These helper methods are reused throughout the AI-103 Learning Labs.
"""

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential


# =============================================================================
# Configuration
# =============================================================================

def validate_configuration(
    endpoint: str,
    model: str | None = None,
    agent_name: str | None = None,
) -> None:
    """
    Validate the required Azure AI Foundry configuration.
    """

    if not endpoint:
        raise ValueError("FOUNDRY_PROJECT_ENDPOINT is missing.")

    if model is not None and not model:
        raise ValueError("FOUNDRY_MODEL_DEPLOYMENT is missing.")

    if agent_name is not None and not agent_name:
        raise ValueError("FOUNDRY_AGENT_NAME is missing.")


# =============================================================================
# Authentication
# =============================================================================

def create_credential() -> DefaultAzureCredential:
    """
    Create a Default Azure Credential.

    Authentication is automatically resolved using one of the
    supported Azure authentication methods, such as:

    - Visual Studio
    - Azure CLI
    - Visual Studio Code
    - Managed Identity
    """

    return DefaultAzureCredential()


# =============================================================================
# Azure AI Foundry
# =============================================================================

def create_project_client(
    endpoint: str,
    credential: DefaultAzureCredential,
) -> AIProjectClient:
    """
    Create an Azure AI Foundry project client.
    """

    return AIProjectClient(
        endpoint=endpoint,
        credential=credential,
    )


def create_openai_client(project_client: AIProjectClient):
    """
    Create an Azure OpenAI client from the Foundry project.
    """

    return project_client.get_openai_client()


def create_conversation(openai_client):
    """
    Create a new conversation.
    """

    return openai_client.conversations.create()


# =============================================================================
# Agent Management
# =============================================================================

def delete_agent(
    project_client: AIProjectClient,
    agent,
) -> None:
    """
    Delete an Agent Version after the lab has completed.

    Microsoft Learn creates temporary agents for many labs.
    Cleaning them up prevents unnecessary clutter inside
    the Foundry project.
    """

    project_client.agents.delete_version(
        agent_name=agent.name,
        agent_version=agent.version,
    )


# =============================================================================
# Cleanup
# =============================================================================

def cleanup(
    credential: DefaultAzureCredential | None,
    project_client: AIProjectClient | None,
    openai_client,
) -> None:
    """
    Close all Azure resources.
    """

    try:
        if openai_client is not None:
            openai_client.close()
    except Exception:
        pass

    try:
        if project_client is not None:
            project_client.close()
    except Exception:
        pass

    try:
        if credential is not None:
            credential.close()
    except Exception:
        pass
