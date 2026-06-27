# Lab001 - Agents with Functions

## Overview

This lab demonstrates how to connect a Python application to an Azure AI Foundry Agent using the Azure AI Projects SDK.

The agent is configured in Azure AI Foundry and can use:

* Knowledge Files
* Code Interpreter
* Conversations API
* Responses API
* File Generation
* Chart Generation

The Python application acts as a client that sends user messages to the agent and processes the responses.

---

## Learning Objectives

This lab covers the following AI-103 concepts:

* Azure AI Foundry Agent Service
* Agent Instructions
* Knowledge Files
* Code Interpreter
* Conversations
* Responses API
* Agent References
* Azure Identity Authentication
* File Citations
* Generated Files

---

## Solution Architecture

```text
User
 │
 ▼
Python Client
 │
 ▼
Azure AI Foundry Agent
 │
 ├── Instructions
 ├── Knowledge Files
 ├── Code Interpreter
 └── GPT Model
```

The Python application is responsible for:

* Connecting to Azure AI Foundry
* Starting conversations
* Sending user prompts
* Displaying agent responses
* Downloading generated files
* Saving generated charts

The Agent is responsible for:

* Retrieving knowledge
* Executing Python code
* Analyzing uploaded files
* Generating responses

---

## Prerequisites

### Azure Resources

The following Azure resources are required:

* Azure AI Foundry Project
* Azure AI Foundry Agent
* Azure OpenAI Deployment
* Azure Subscription

### Local Software

* Python 3.11+
* Visual Studio 2022/2026 or VS Code
* Azure CLI
* Azure Login

---

## Required Python Packages

Install the required packages:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install openai
pip install python-dotenv
pip install azure-ai-projects
pip install azure-identity
```

---

## Configuration

Create a `.env` file in the project root.

Example:

```env
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-openai-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_DEPLOYMENT=gpt-4.1

# Azure AI Search
AZURE_AI_SEARCH_ENDPOINT=https://your-search-service.search.windows.net
AZURE_AI_SEARCH_KEY=your-search-key

# Azure AI Foundry
FOUNDRY_PROJECT_ENDPOINT=https://your-project.services.ai.azure.com/api/projects/your-project
FOUNDRY_AGENT_NAME=it-support-agent
```

---

## Agent Configuration

The lab expects an Azure AI Foundry Agent to exist.

Example:

### Agent Name

```text
it-support-agent
```

### Instructions

```text
You are an IT Support Agent for Contoso Corporation.

You help employees with technical issues and IT policy questions.
```

### Knowledge Files

Upload:

```text
IT_Policy.txt
```

Purpose:

* Company policies
* Password requirements
* IT procedures

### Code Interpreter Files

Upload:

```text
system_performance.csv
```

Purpose:

* Data analysis
* Charts
* Trend analysis

---

## Example Questions

### Knowledge File

```text
What is the password policy?
```

### Data Analysis

```text
Analyze the system performance data.
```

### Chart Generation

```text
Create a chart showing CPU usage over time.
```

---

## Generated Output

The application automatically stores generated content in:

```text
agent_outputs/
```

Examples:

```text
agent_outputs/
├── chart_1.png
├── chart_2.png
└── report.csv
```

---

## Authentication

The application uses:

```python
DefaultAzureCredential()
```

Supported authentication methods:

* Azure CLI Login
* Visual Studio Login
* Visual Studio Code Login
* Managed Identity

Login example:

```bash
az login
```

---

## Known Issues

### Rate Limit Exceeded

Example:

```text
429 - rate_limit_exceeded
```

Cause:

* Azure OpenAI deployment quota exceeded.

Resolution:

* Wait a few minutes.
* Increase deployment quota.
* Switch to another deployment.

---

## Repository Structure

```text
05-agents/
│
├── lab001-agents-with-functions.py
├── README.md
│
shared/
├── config.py
│
data/
├── lab001-agents-with-functions/
│   ├── IT_Policy.txt
│   └── system_performance.csv
│
agent_outputs/
```

---

## Key Takeaways

This lab demonstrates how an Azure AI Foundry Agent can:

* Retrieve information from Knowledge Files
* Execute Python code using Code Interpreter
* Generate charts and files
* Maintain conversation context
* Be accessed programmatically through Python

This is one of the foundational patterns for building AI-powered business applications with Azure AI Foundry.

More information can be found in the official documentation: https://microsoftlearning.github.io/mslearn-ai-agents/Instructions/Exercises/01-build-agent-portal-and-vscode.html