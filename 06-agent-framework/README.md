# Lab 001 - Microsoft Agent Framework

> **Module:** 06-agent-framework

This lab demonstrates how to build an AI agent by using the **Microsoft Agent Framework** together with **Azure AI Foundry**.

The agent reads expense data from a text file and uses **Automatic Function Calling** to invoke a custom tool that simulates submitting an expense claim by email.

Unlike the previous Azure AI Agent labs, this exercise uses the **Microsoft Agent Framework**, Microsoft's latest SDK for building enterprise AI agents.

---

## Learning Objectives

After completing this lab you will understand how to:

- Create a Microsoft Foundry Agent
- Connect to an Azure AI Foundry project
- Authenticate using `AzureCliCredential`
- Configure agent instructions (system prompt)
- Register custom tools
- Use Automatic Function Calling
- Execute conversations with an AI agent
- Build enterprise AI applications with the Microsoft Agent Framework

---

## Technologies Used

- Python
- Microsoft Agent Framework
- Azure AI Foundry
- Azure OpenAI
- Azure Identity
- Pydantic
- dotenv

---

## Project Structure

```text
06-agent-framework
│
├── Lab001_agent_framework.py
├── data.txt
└── README.md
```

---

## Prerequisites

Before running this lab, ensure the following prerequisites are met:

- Azure AI Foundry project
- Azure OpenAI model deployment
- Azure CLI installed
- Logged in with:

```bash
az login
```

- Correct configuration in:

```text
.env
```

- Required packages installed:

```bash
pip install -r requirements.txt
```

---

## Architecture

```text
                   User
                     │
                     ▼
        Microsoft Agent Framework
                     │
                     ▼
          FoundryChatClient
                     │
                     ▼
       Azure AI Foundry Project
                     │
                     ▼
             Azure OpenAI Model
                     │
                     ▼
      Automatic Function Calling
                     │
                     ▼
             submit_claim()
                     │
                     ▼
              Agent Response
```

The Microsoft Agent Framework automatically decides whether the registered tool should be executed based on the user's request.

---

## How It Works

The application performs the following steps:

1. Reads expense data from **data.txt**
2. Prompts the user for a request
3. Connects to Azure AI Foundry
4. Creates a Microsoft Foundry Agent
5. Registers a custom tool (`submit_claim`)
6. Sends the conversation to the LLM
7. The LLM determines whether the tool should be called
8. The tool is executed automatically
9. The final response is returned to the user

---

## Sample Questions

Try one of the following prompts:

- Submit an expense claim.
- Create an expense report.
- Process these expenses.
- Please submit this expense claim.
- Send these expenses to accounting.
- Email my expense claim.

---

## Automatic Function Calling

One of the key concepts demonstrated in this lab is **Automatic Function Calling**.

Instead of explicitly calling Python functions, the AI model determines whether a tool is required.

```text
User Prompt
      │
      ▼
Large Language Model
      │
      ▼
Does a Tool Need to be Executed?
      │
      ├───────────────┐
      │               │
     No              Yes
      │               │
      ▼               ▼
Generate       Execute submit_claim()
Response             │
      │               ▼
      └──────► Tool Result
                     │
                     ▼
             Final AI Response
```

This greatly simplifies application development because the developer only registers the available tools. The Microsoft Agent Framework handles the orchestration automatically.

---

## Custom Tool

The lab exposes a single custom tool:

```python
submit_claim()
```

The tool is registered using the `@tool` decorator.

The AI receives metadata describing:

- Function name
- Purpose
- Input parameters
- Return value

Using this information, the framework automatically determines:

- when to call the tool
- which parameters to pass
- how to incorporate the result into the final response

---

## Authentication

Authentication is handled using:

```python
AzureCliCredential()
```

This credential reuses the Azure CLI login performed with:

```bash
az login
```

No API keys are required during development.

---

## Expected Output

Example:

```text
Here are the expenses contained in the file...

> Submit an expense claim

===================================================
Expense Claim Tool
===================================================

To      : expenses@contoso.com
Subject : Expense Claim

Flight Amsterdam - London
Hotel
Taxi

===================================================
Agent Response
===================================================

Your expense claim has been submitted successfully.
```

---

## Microsoft Learn

This lab is based on the official Microsoft Learn exercise:

https://microsoftlearning.github.io/mslearn-ai-agents/Instructions/Exercises/07-agent-framework.html

---

## Key Concepts

- Microsoft Agent Framework
- Azure AI Foundry
- FoundryChatClient
- Agent
- Agent Instructions
- AzureCliCredential
- Automatic Function Calling
- Custom Tools
- Tool Registration
- Tool Metadata
- Enterprise AI Agents

---

## Key Takeaways

This lab demonstrates how the Microsoft Agent Framework simplifies enterprise AI development by:

- Providing a high-level SDK for AI agents
- Managing conversations and agent execution
- Supporting Automatic Function Calling
- Integrating seamlessly with Azure AI Foundry
- Registering custom Python functions as AI tools
- Reducing the amount of orchestration code developers need to write

---

## Related Labs

This lab builds upon concepts introduced in previous modules:

| Module | Topic |
|---------|-------|
| 01 | Chat Completions |
| 02 | Prompt Engineering |
| 03 | Code Interpreter |
| 04 | Retrieval Augmented Generation (RAG) |
| 05 | Azure AI Agents |
| **06** | **Microsoft Agent Framework** |

---

## Repository

This lab is part of the **AI-Learning-Labs** project, a personal learning repository created while completing the **Microsoft AI-103** learning path.

Each module focuses on a different Azure AI capability and includes fully documented source code, configuration examples, and practical demonstrations.