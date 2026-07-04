# Azure AI Foundry Agents

This folder contains a collection of Azure AI Foundry Agent samples created while completing the **Microsoft AI-103** learning path.

Each lab introduces a new capability of Azure AI Foundry Agents. Together they demonstrate the evolution from basic conversational agents to enterprise-grade AI solutions using Retrieval-Augmented Generation (RAG), Azure AI Foundry IQ, Function Calling and the Model Context Protocol (MCP).

---

# Learning Objectives

The labs demonstrate the following Azure AI concepts:

- Azure AI Foundry Agent Service
- Azure AI Projects SDK
- Azure OpenAI Responses API
- Conversations API
- Agent References
- Azure Identity Authentication
- Knowledge Files
- Code Interpreter
- Function Calling
- Azure AI Foundry IQ
- Knowledge Sources
- Knowledge Bases
- Retrieval Augmented Generation (RAG)
- Azure Blob Storage
- Azure AI Search
- Remote MCP Servers

---

# Lab Overview

## Lab001 – Azure AI Foundry Agent with Knowledge Files

Introduces Azure AI Foundry Agents using uploaded knowledge files.

Implemented concepts:

- Knowledge Files
- Conversations API
- Responses API
- Agent Instructions

**Source**

```text
Lab001_agents_with_functions.py
```

---

## Lab002 – Azure AI Agent with Custom Function Tools

Demonstrates how an Azure AI Agent can execute deterministic business logic by invoking custom Python functions.

Implemented concepts:

- Function Calling
- Function Tools
- Tool Registration
- Business Logic Integration

Example functions:

- next_visible_event()
- calculate_observation_cost()
- generate_observation_report()

**Source**

```text
Lab002_agent.py
```

---

## Lab003 – Azure AI Agent with a Remote MCP Server

Introduces the **Model Context Protocol (MCP)**.

Instead of calling local Python functions, the Agent connects to the Microsoft Learn MCP Server and dynamically discovers available tools.

Implemented concepts:

- Model Context Protocol (MCP)
- Remote MCP Server
- Tool Discovery
- MCP Approval Requests

**Source**

```text
Lab003_mcp_remote.py
```

---

## Lab004 – Azure AI Foundry IQ Knowledge Base (RAG)

Demonstrates how to build a Retrieval-Augmented Generation (RAG) solution using Azure AI Foundry IQ.

The Azure AI Agent retrieves information from PDF documents stored in Azure Blob Storage through an Azure AI Search index.

Knowledge sources include:

- Contoso Product Catalog
- Camping Accessories
- Backpack Guide

Implemented concepts:

- Azure AI Foundry IQ
- Knowledge Sources
- Knowledge Bases
- Azure Blob Storage
- Azure AI Search
- Retrieval-Augmented Generation (RAG)
- Agent References
- Conversations API
- Responses API

**Source**

```text
Lab004_agent_client_contoso.py
```

---

# Repository Structure

```text
05-agents/
│
├── Lab001_agents_with_functions.py
├── Lab002_agent.py
├── Lab003_mcp_remote.py
├── Lab004_agent_client_contoso.py
├── README.md
│
├── data/
│   └── contosoproducts/
│       ├── contoso-backpacks-guide.pdf
│       ├── contoso-camping-accessories.pdf
│       └── contoso-tents-catalog.pdf
│
├── shared/
│   ├── config.py
│   ├── console.py
│   └── openai_client.py
│
└── mcpagent/
    ├── client.py
    ├── server.py
    └── README.md
```

---

# Solution Evolution

```text
Lab001
Knowledge Files
        │
        ▼
Lab002
Function Calling
        │
        ▼
Lab003
Remote MCP Server
        │
        ▼
Lab004
Azure AI Foundry IQ
Knowledge Base (RAG)
```

---

# Architecture

```text
Azure AI Foundry Project
          │
          ▼
Azure AI Agent
          │
          ├──────────────┐
          │              │
          ▼              ▼
Function Tools      Knowledge Base
                          │
                          ▼
                   Azure AI Search
                          │
                          ▼
                  Azure Blob Storage
                          │
                          ▼
                     PDF Documents
```

---

# Azure Resources

The samples require the following Azure resources:

- Azure AI Foundry Project
- Azure OpenAI Deployment
- Azure AI Search
- Azure Blob Storage
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

# Configuration

All samples use a shared configuration module.

Environment variables are loaded from the project `.env` file via:

```python
shared.config
```

Example:

```env
FOUNDRY_PROJECT_ENDPOINT=https://<project>.services.ai.azure.com/api/projects/<project>

FOUNDRY_AGENT_NAME=my-agent

FOUNDRY_MODEL_DEPLOYMENT=gpt-4.1-mini
```

Some labs define additional configuration variables for dedicated Azure AI Foundry projects.

Example:

```env
FOUNDRY_PROJECT_ENDPOINT_CONTOSO=...

FOUNDRY_AGENT_NAME_CONTOSO=...
```

---

# Required Python Packages

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

# Key Takeaways

These labs demonstrate the evolution of Azure AI Foundry Agents from simple conversational assistants to enterprise AI applications.

Topics include:

- Knowledge Files
- Function Calling
- Azure AI Foundry IQ
- Retrieval-Augmented Generation (RAG)
- Azure AI Search
- Azure Blob Storage
- Remote MCP Servers
- Enterprise Knowledge Integration

Together these examples form a practical reference implementation for building enterprise AI solutions with Azure AI Foundry.

---

# References

Microsoft Learn

Develop AI Agents with Azure AI Foundry

