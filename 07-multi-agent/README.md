# Lab 001 - Multi-Agent Orchestration

> **Module:** 07-multi-agent

This lab demonstrates how to build a **Multi-Agent AI solution** by using the **Microsoft Agent Framework** together with **Azure AI Foundry**.

Instead of relying on a single AI agent, this solution creates multiple specialized agents that collaborate in a **Sequential Orchestration** workflow. Each agent has a single responsibility, making the overall solution easier to understand, maintain, and extend.

The sample processes customer feedback by summarizing the text, classifying it, and recommending the next business action.

---

## Learning Objectives

After completing this lab you will understand how to:

- Build a Multi-Agent solution
- Create specialized AI agents
- Configure agent-specific system prompts
- Connect to Azure AI Foundry
- Authenticate using `AzureCliCredential`
- Use the Microsoft Agent Framework
- Build a Sequential Orchestration workflow
- Execute multiple agents in sequence
- Understand agent collaboration and orchestration

---

## Technologies Used

- Python
- Microsoft Agent Framework
- Azure AI Foundry
- Azure OpenAI
- Azure Identity
- Async Programming (`asyncio`)

---

## Project Structure

```text
07-multi-agent
│
├── Lab001_multi_agent.py
└── README.md
```

---

## Prerequisites

Before running this lab ensure you have:

- Azure AI Foundry project
- Azure OpenAI deployment
- Azure CLI installed
- Logged in using:

```bash
az login
```

- Correct configuration inside:

```text
.env
```

Example:

```ini
FOUNDRY_PROJECT_ENDPOINT_MULTI=...
FOUNDRY_MODEL_DEPLOYMENT_MULTI=gpt-4.1-mini
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## Solution Architecture

```text
                  Customer Feedback
                           │
                           ▼
                  Sequential Workflow
                           │
      ┌────────────────────┼────────────────────┐
      ▼                    ▼                    ▼
 Summarizer Agent    Classifier Agent     Action Agent
      │                    │                    │
      └────────────────────┴────────────────────┘
                           │
                           ▼
                     Final Output
```

Each agent performs one specialized task before passing its output to the next participant.

---

## Agent Responsibilities

### Summarizer Agent

Purpose:

- Read customer feedback
- Produce a concise summary
- Remove unnecessary details

Example output:

```text
User requests a dark mode for the dashboard.
```

---

### Classifier Agent

Purpose:

Classify the feedback as one of:

- Positive
- Negative
- Feature Request

Example:

```text
Feature Request
```

---

### Action Agent

Purpose:

Recommend the next business action.

Example:

```text
Log as enhancement request for product backlog.
```

---

## Sequential Orchestration

This lab demonstrates **Sequential Orchestration**.

Each agent waits until the previous agent has completed its work.

```text
Customer Feedback

↓

Summarizer

↓

Classifier

↓

Action

↓

Result
```

This orchestration pattern is ideal when each step depends on the output of the previous step.

---

## How It Works

The application performs the following steps:

1. Connects to Azure AI Foundry
2. Creates three specialized AI agents
3. Builds a Sequential Workflow
4. Sends customer feedback into the workflow
5. Executes each agent in sequence
6. Collects every agent's response
7. Displays the intermediate and final results

---

## Sample Feedback

Example 1

```text
The dashboard works well, but I would really appreciate a dark mode for working at night.
```

Expected output:

```text
Summary:
User requests a dark mode.

Classification:
Feature Request

Action:
Log as enhancement request for product backlog.
```

---

Example 2

```text
The application crashes every time I upload a photo.
```

Expected output:

```text
Summary:
Application crashes during photo upload.

Classification:
Negative

Action:
Escalate as a high-priority bug.
```

---

Example 3

```text
The latest release is fantastic! Everything feels much faster.
```

Expected output:

```text
Summary:
User is satisfied with the latest release.

Classification:
Positive

Action:
Share positive feedback with the product team.
```

---

## Why Multi-Agent?

Instead of one large AI agent performing every task, each agent focuses on a single responsibility.

Advantages include:

- Smaller prompts
- Better maintainability
- Improved scalability
- Easier testing
- Reusable agents
- Better enterprise architecture

---

## Multi-Agent vs Single-Agent

| Single Agent | Multi-Agent |
|---------------|------------|
| One large prompt | Multiple specialized prompts |
| One responsibility overload | One responsibility per agent |
| Harder to maintain | Easier to maintain |
| Less reusable | Highly reusable |
| Limited scalability | Highly scalable |

---

## Sequential vs Parallel Orchestration

This lab demonstrates **Sequential Orchestration**.

```text
Summarizer

↓

Classifier

↓

Action
```

In more advanced scenarios, multiple agents can execute simultaneously using **Parallel Orchestration**.

---

## Authentication

Authentication uses:

```python
AzureCliCredential()
```

The credential automatically reuses your Azure CLI login.

```bash
az login
```

No API keys are required during development.

---

## Expected Output

```text
------------------------------------------------------------
01 [summarizer]

User requests a dark mode for the dashboard.

------------------------------------------------------------
02 [classifier]

Feature Request

------------------------------------------------------------
03 [action]

Log as enhancement request for product backlog.
```

---

## Microsoft Learn

Official exercise:

https://microsoftlearning.github.io/mslearn-ai-agents/Instructions/Exercises/08-agent-framework-multi-agents.html

---

## Key Concepts

- Microsoft Agent Framework
- Azure AI Foundry
- Multi-Agent Solutions
- Sequential Orchestration
- Specialized Agents
- Agent Instructions
- AzureCliCredential
- Azure OpenAI
- Workflow Orchestration

---

## Key Takeaways

This lab demonstrates how the Microsoft Agent Framework enables multiple specialized AI agents to collaborate in a structured workflow.

Instead of creating one large prompt, responsibilities are divided across several focused agents. This approach improves maintainability, scalability, and clarity while making enterprise AI solutions easier to design and extend.

Sequential orchestration ensures that each agent builds upon the work of the previous agent, creating a simple but powerful collaboration model.

---

## Related Labs

| Module | Topic |
|---------|-------|
| 01 | Chat Completions |
| 02 | Prompt Engineering |
| 03 | Code Interpreter |
| 04 | Retrieval-Augmented Generation (RAG) |
| 05 | Azure AI Agents |
| 06 | Microsoft Agent Framework |
| **07** | **Multi-Agent Orchestration** |

---

## Repository

This lab is part of the **AI-Learning-Labs** project, a personal learning repository created while completing the **Microsoft AI-103** learning path.

Each module focuses on a specific Azure AI capability and includes fully documented source code, configuration examples, and practical demonstrations.