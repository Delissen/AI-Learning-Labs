# Local MCP Agent

This folder contains a complete implementation of a **local Model Context Protocol (MCP)** solution.

The implementation demonstrates how an **Azure AI Foundry Agent** can communicate with a locally hosted MCP Server to execute business functionality on demand.

Unlike the previous lab, which connected to the public **Microsoft Learn MCP Server**, this implementation hosts its own MCP Server and exposes custom business tools.

---

# What is MCP?

The **Model Context Protocol (MCP)** is an open protocol that enables AI Agents to discover and invoke external tools dynamically.

Instead of hardcoding Python functions or API integrations into an AI Agent, MCP provides a standardized interface that allows tools to be published by an MCP Server and consumed by any compatible AI Agent.

Benefits include:

- Standardized tool discovery
- Separation of business logic from the AI Agent
- Easier maintenance
- Better scalability
- Reusable integrations

---

# Project Structure

```text
mcpagent/
│
├── client.py
├── server.py
├── __init__.py
└── README.md
```

---

# Components

## server.py

Implements the local MCP Server.

The server exposes business functionality as MCP Tools.

Current tools include:

- get_inventory_levels()
- get_weekly_sales()

Each tool can be discovered automatically by any MCP-compatible client.

---

## client.py

Acts as the bridge between Azure AI Foundry and the local MCP Server.

Responsibilities include:

- Starting the local MCP Server
- Establishing an MCP Client Session
- Discovering available MCP Tools
- Converting MCP Tools into Azure AI Function Tools
- Processing Function Calls
- Returning tool output back to the AI Agent

The Azure AI Agent is unaware that these functions are executed locally. From the model's perspective they behave like native tools.

---

# Architecture

```text
                 User
                   │
                   ▼
          Azure AI Foundry Agent
                   │
                   ▼
             Function Calling
                   │
                   ▼
               MCP Client
                   │
       Model Context Protocol
                   │
                   ▼
              Local MCP Server
         ┌─────────┴─────────┐
         ▼                   ▼
get_inventory_levels()   get_weekly_sales()
```

---

# Communication Flow

The following sequence takes place during a conversation:

```text
User Prompt
      │
      ▼
Azure AI Agent
      │
      ▼
Agent determines that external data is required
      │
      ▼
Function Call
      │
      ▼
MCP Client
      │
      ▼
Local MCP Server
      │
      ▼
Business Function
      │
      ▼
JSON Result
      │
      ▼
MCP Client
      │
      ▼
Azure AI Agent
      │
      ▼
Natural Language Response
```

---

# MCP Workflow

The interaction between the Azure AI Agent and the local MCP Server consists of several steps:

1. The MCP Client starts the local MCP Server.
2. The client establishes an MCP Session.
3. The client requests a list of available tools.
4. The server publishes its tool definitions.
5. The client converts each MCP Tool into an Azure AI Function Tool.
6. The Azure AI Agent receives these Function Tools.
7. During the conversation, the LLM decides when a tool should be invoked.
8. The MCP Client executes the selected tool.
9. The result is returned to the Azure AI Agent.
10. The Azure AI Agent generates the final response for the user.

---

# Business Scenario

This sample uses a fictional cosmetics retailer.

The MCP Server exposes two inventory-related tools:

### Inventory Levels

Returns the current stock levels for all products.

Example:

```text
Moisturizer : 6
Conditioner : 3
Dry Shampoo : 45
```

### Weekly Sales

Returns the number of units sold during the previous week.

Example:

```text
Moisturizer : 22
Conditioner : 1
Dry Shampoo : 17
```

The AI Agent combines these datasets to determine:

- Products that should be restocked
- Products that may require promotional discounts
- Inventory trends
- Stock recommendations

---

# Key Learning Objectives

This implementation demonstrates:

- Local MCP Server development
- FastMCP
- MCP Client Sessions
- Tool Discovery
- Dynamic Function Creation
- Azure AI Foundry Agents
- Function Calling
- OpenAI Responses API

---

# Technologies

- Python 3.14
- FastMCP
- Model Context Protocol (MCP)
- Azure AI Foundry
- Azure AI Projects SDK
- Azure Identity
- OpenAI Responses API

---

# References

Microsoft Learn

**Develop AI Agents with Azure AI Foundry**

Exercise 03 – MCP Integration

https://microsoftlearning.github.io/mslearn-ai-agents/Instructions/Exercises/03-mcp-integration.html
