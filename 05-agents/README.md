# Azure AI Agents

This folder contains the Azure AI Agent labs created while completing the **Microsoft AI-103** learning path.

The labs gradually build upon each other and demonstrate how Azure AI Foundry Agents can be extended with additional capabilities such as Function Calling and the Model Context Protocol (MCP).

---

# Learning Objectives

The labs cover the following AI-103 concepts:

- Azure AI Foundry Agent Service
- Prompt Agent Definitions
- Azure AI Projects SDK
- Azure OpenAI Responses API
- Conversations API
- Function Calling
- Function Tools
- Model Context Protocol (MCP)
- Remote MCP Servers
- Local MCP Servers
- Azure Identity Authentication

---

# Lab Overview

## Lab001 - Agents with Knowledge Files and Code Interpreter

Demonstrates how to build an Azure AI Foundry Agent that uses:

- Knowledge Files
- Code Interpreter
- Conversations API
- Responses API

The Python application communicates with the Azure AI Agent and automatically processes generated files and charts.

**Source**

```
Lab001_agents_with_functions.py
```

---

## Lab002 - Azure AI Agent with Custom Function Tools

Introduces **Function Calling**.

Instead of relying only on built-in Agent capabilities, the Large Language Model can invoke custom Python functions to perform deterministic business logic.

Implemented Function Tools:

- next_visible_event()
- calculate_observation_cost()
- generate_observation_report()

**Source**

```
Lab002_agent.py
```

---

## Lab003 - Azure AI Agent with a Remote MCP Server

Introduces the **Model Context Protocol (MCP)**.

Instead of calling local Python functions, the Azure AI Agent connects to the **Microsoft Learn MCP Server**.

The agent dynamically discovers available tools and requests approval before executing them.

Implemented concepts:

- MCPTool
- Tool Discovery
- MCP Approval Requests
- Remote MCP Server
- Microsoft Learn MCP Server

**Source**

```
Lab003_mcp_remote.py
```

---

## Lab004 - Azure AI Agent with a Local MCP Server

The next step is hosting your own MCP Server.

The local implementation consists of two components:

```
mcpagent/
├── client.py
└── server.py
```

The MCP Client connects Azure AI Foundry with a locally running MCP Server.

The MCP Server exposes inventory-related business functions as AI tools.

This demonstrates how enterprise applications can expose internal functionality through the Model Context Protocol.

---

# Solution Evolution

```text
Lab001
Knowledge Files
Code Interpreter
        │
        ▼
Lab002
Function Calling
        │
        ▼
Lab003
Remote MCP Server
(Microsoft Learn)
        │
        ▼
Lab004
Local MCP Server
(Custom Business Logic)
```

---

# Repository Structure

```text
05-agents/
│
├── Lab001_agents_with_functions.py
├── Lab002_agent.py
├── Lab003_mcp_remote.py
├── README.md
│
mcpagent/
│   ├── client.py
│   ├── server.py
│   └── README.md
│
shared/
│
data/
```

---

# Azure Resources

These labs require:

- Azure AI Foundry Project
- Azure OpenAI Deployment
- Azure AI Projects SDK
- Azure Subscription

Authentication is performed using:

```python
DefaultAzureCredential()
```

Supported authentication methods:

- Azure CLI
- Visual Studio
- Visual Studio Code
- Managed Identity

---

# Required Python Packages

Install all required packages using:

```bash
pip install -r requirements.txt
```

---

# Configuration

The labs use a shared configuration module.

Environment variables are loaded from the project `.env` file through:

```python
shared.config
```

Example:

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project>.services.ai.azure.com/api/projects/<project>

FOUNDRY_MODEL_DEPLOYMENT=gpt-4.1

FOUNDRY_AGENT_NAME=my-agent
```

---

# Key Takeaways

These labs demonstrate the natural evolution of Azure AI Agents:

- Using built-in Agent capabilities
- Extending Agents with Python Function Tools
- Connecting to Remote MCP Servers
- Hosting your own Local MCP Server
- Integrating AI Agents with external business logic

Together these examples form a practical reference implementation for building enterprise AI solutions with Azure AI Foundry and the Model Context Protocol.

---

# References

Microsoft Learn

Develop AI Agents with Azure AI Foundry

- Exercise 01 – Agents with Knowledge Files
- Exercise 02 – Agent Custom Tools
- Exercise 03 – MCP Integration

https://microsoftlearning.github.io/mslearn-ai-agents/