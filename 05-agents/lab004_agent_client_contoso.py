"""
===========================================================================
Lab 004 - Azure AI Foundry IQ Agent Client
===========================================================================

Description
-----------
This sample demonstrates how to communicate with an Azure AI Foundry Agent
that is connected to a Foundry IQ Knowledge Base.

The agent uses Retrieval Augmented Generation (RAG) to answer questions
based on PDF documents stored in Azure Blob Storage.
In the project the sample documents are stored in Data\contosoproducts\

Knowledge Base
--------------
- Contoso Outdoor Product Catalog
- Camping Accessories
- Backpack Guide

Based on
--------
https://microsoftlearning.github.io/mslearn-ai-agents/Instructions/Exercises/04-integrate-agent-with-foundry-iq.html

Author
------
Maarten Delissen
https://github.com/Delissen

Example questions
-----------------
- What types of tents does Contoso offer?
- Tell me about which backpacks are available in XL.
- What camping accessories are available?
- Which backpack is suitable for a weekend hiking trip?
===========================================================================
"""
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from shared.config import (
    FOUNDRY_PROJECT_ENDPOINT_CONTOSO,
    FOUNDRY_AGENT_NAME_CONTOSO,
)

# Load environment variables
load_dotenv()
project_endpoint = FOUNDRY_PROJECT_ENDPOINT_CONTOSO
agent_name = FOUNDRY_AGENT_NAME_CONTOSO

# Validate configuration
if not project_endpoint or not agent_name:
    raise ValueError("FOUNDRY_PROJECT_ENDPOINT_CONTOSO and FOUNDRY_AGENT_NAME_CONTOSO must be set in .env file")

print(f"Project endpoint : {project_endpoint}")
print(f"Agent            : {agent_name}")

# 1. Create DefaultAzureCredential
# 2. Create AIProjectClient with endpoint
# 3. Get the OpenAI client
# 4. Get the agent by name
# 5. Create a new conversation


# Connect to the project and agent
credential = DefaultAzureCredential(
     exclude_environment_credential=True,
     exclude_managed_identity_credential=True
)
project_client = AIProjectClient(
     credential=credential,
     endpoint=project_endpoint
)

# Get the OpenAI client
openai_client = project_client.get_openai_client()

# Get the agent
agent = project_client.agents.get(agent_name=agent_name)
print(f"Connected to agent: {agent.name} (id: {agent.id})\n")

# Create a new conversation
conversation = openai_client.conversations.create(items=[])
print(f"Created conversation (id: {conversation.id})\n")

# Conversation history for context (client-side tracking)
conversation_history = []


def send_message_to_agent(user_message):
    """
    Send a message to the agent and handle the response using the conversations API.
    """
    try:
        print("\nAgent: ", end="", flush=True)
        
        # 1. Add the user message to the conversation using conversations.items.create()
        # 2. Create a response using responses.create() with agent reference
        # 3. Extract and display the response text
        # 4. Check for and display any citations
        # Your code will go here

        # Add user message to the conversation
        openai_client.conversations.items.create(
             conversation_id=conversation.id,
             items=[{"type": "message", "role": "user", "content": user_message}],
         )
    
        # Store in conversation history (client-side)
        conversation_history.append({
             "role": "user",
             "content": user_message
         })
    
        # Create a response using the agent
        response = openai_client.responses.create(
             conversation=conversation.id,
             extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
             input=""
         )

        # Check if the response output contains an MCP approval request
        approval_request = None
        if hasattr(response, 'output') and response.output:
             for item in response.output:
                 if hasattr(item, 'type') and item.type == 'mcp_approval_request':
                     approval_request = item
                     break
    
        # Handle approval request if present
        if approval_request:
             print(f"[Approval required for: {approval_request.name}]\n")
             print(f"Server: {approval_request.server_label}")
        
             # Parse and display the arguments (optional, for transparency)
             import json
             try:
                 args = json.loads(approval_request.arguments)
                 print(f"Arguments: {json.dumps(args, indent=2)}\n")
             except:
                 print(f"Arguments: {approval_request.arguments}\n")
        
             # Prompt user for approval
             approval_input = input("Approve this action? (yes/no): ").strip().lower()
        
             if approval_input in ['yes', 'y']:
                 print("Approving action...\n")
            
                 # Create approval response item
                 approval_response = {
                     "type": "mcp_approval_response",
                     "approval_request_id": approval_request.id,
                     "approve": True
                 }
             else:
                 print("Action denied.\n")
            
                 # Create denial response item
                 approval_response = {
                     "type": "mcp_approval_response",
                     "approval_request_id": approval_request.id,
                     "approve": False
                 }
        
             # Add the approval response to the conversation
             openai_client.conversations.items.create(
                 conversation_id=conversation.id,
                 items=[approval_response]
             )
        
             # Get the actual response after approval/denial
             response = openai_client.responses.create(
                 conversation=conversation.id,
                 extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
                 input=""
             )
        
        # Extract the response text
        if response and response.output_text:
            response_text = response.output_text
            
            print(f"{response_text}\n")
            
            # Check for citations if available
            if hasattr(response, 'citations') and response.citations:
                print("\nSources:")
                for citation in response.citations:
                    print(f"  - {citation.content if hasattr(citation, 'content') else 'Knowledge Base'}")
            
            # Store in conversation history (client-side)
            conversation_history.append({
                "role": "assistant",
                "content": response_text
            })
            
            return response_text
        else:
            print("No response received.\n")
            return None
    except Exception as e:
        print(f"\n\nError: {str(e)}\n")
        return None


def display_conversation_history():
    """
    Display the full conversation history.
    """
    print("\n" + "="*60)
    print("CONVERSATION HISTORY")
    print("="*60 + "\n")
    
    for turn in conversation_history:
        role = turn["role"].upper()
        content = turn["content"]
        print(f"{role}: {content}\n")
    
    print("="*60 + "\n")


def main():
    """
    Main interaction loop.
    """
    print("Contoso Product Expert Agent")
    print("Ask questions about our outdoor and camping products.")
    print("Type 'history' to see conversation history, or 'quit' to exit.\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() == 'quit':
                print("\nEnding conversation...")
                break
                
            if user_input.lower() == 'history':
                display_conversation_history()
                continue
            
            # Send message and get response
            send_message_to_agent(user_input)
            
        except KeyboardInterrupt:
            print("\n\nInterrupted by user.")
            break
        except Exception as e:
            print(f"\nUnexpected error: {str(e)}\n")
    
    print("\nConversation ended.")


if __name__ == "__main__":
    main()
