# Lab 001 – Agent-to-Agent (A2A) Communication

> **Module:** 08-a2a-agent

This lab explores the **Agent-to-Agent (A2A) Protocol**, an open standard that enables independent AI agents to discover, communicate, and collaborate with each other across different runtimes and frameworks.

Unlike previous labs that use the Microsoft Agent Framework directly, this exercise focuses on remote agents that expose capabilities through the A2A protocol.

---

## Learning Objectives

After completing this lab you will understand how to:

- Understand the Agent-to-Agent (A2A) protocol
- Create multiple remote AI agents
- Expose Agent Cards for agent discovery
- Route requests between specialized agents
- Host AI agents using FastAPI / Starlette
- Communicate with Azure AI Foundry models
- Build distributed multi-agent architectures

---

## Technologies Used

- Python
- Azure AI Foundry
- Microsoft Agent Framework
- A2A SDK
- Starlette
- FastAPI
- Uvicorn
- Azure OpenAI
- dotenv

---

## Project Structure

```
08_a2a_agent
│
├── title_agent
│   ├── agent.py
│   ├── agent_executor.py
│   └── server.py
│
├── outline_agent
│   ├── agent.py
│   ├── agent_executor.py
│   └── server.py
│
├── routing_agent
│   ├── agent.py
│   └── server.py
│
├── client.py
├── run_all.py
├── .env
├── .env.template
└── requirements.txt
```

---

## How it works

The solution consists of three specialized AI agents:

### Title Agent
Generates an engaging title for an article.

### Outline Agent
Creates a structured outline for the requested topic.

### Routing Agent
Discovers the available remote agents through their Agent Cards and routes incoming user requests to the appropriate specialized agent.

The client communicates only with the Routing Agent.

```
Client
   │
   ▼
Routing Agent
   │
   ├────────────► Title Agent
   │
   └────────────► Outline Agent
```

---

## Configuration

The lab requires the following environment variables:

```text
PROJECT_ENDPOINT
MODEL_DEPLOYMENT_NAME

SERVER_URL

TITLE_AGENT_PORT
OUTLINE_AGENT_PORT
ROUTING_AGENT_PORT
```

---

## Current Status

⚠️ **Implementation note**

This project is based on the official Microsoft Learn exercise:

https://microsoftlearning.github.io/mslearn-ai-agents/Instructions/Exercises/09-multi-remote-agents-with-a2a.html

During implementation, multiple compatibility issues were encountered between the current versions of the following packages:

- A2A SDK
- Microsoft Agent Framework
- Starlette
- Uvicorn

The Microsoft Learn sample appears to target earlier SDK versions, while current package releases introduce breaking changes.

The project structure, configuration and agent implementations were successfully integrated into this repository, but the complete end-to-end execution could not be reproduced using the latest publicly available SDK versions.

---

## Lessons Learned

Despite the compatibility issues, this lab provided valuable insight into:

- Agent-to-Agent communication
- Agent discovery using Agent Cards
- Distributed AI architectures
- Routing requests between specialized AI agents
- Hosting AI agents as independent services
- Challenges of rapidly evolving AI SDKs

---

## References

- Microsoft Learn – Discover Agents with A2A
- A2A Protocol
- Azure AI Foundry
- Microsoft Agent Framework

---

## Repository

Part of the **AI-Learning-Labs** repository created while completing the Microsoft AI-103 learning path.

Note: This lab is included for learning and reference purposes. The implementation documents the architecture and integration approach, although the latest SDK versions currently prevent the original Microsoft Learn sample from running without additional modifications.