from shared.openai_client import client
from shared.config import AZURE_OPENAI_DEPLOYMENT

# live gegegens ophalen via web search tool. In dit voorbeeld:
# Microsoft Build aankondigingen, crypto prijzen en vluchtprijzen naar Curacao.

# Learn module: https://learn.microsoft.com/en-us/training/modules/use-generative-ai-tools/04-web-search?pivots=text

print("\n=== Microsoft Build Live data===")

# Get response using the web_search tool
response = client.responses.create(
    model=AZURE_OPENAI_DEPLOYMENT,
    instructions="You are an AI assistant. Use web search when current information is required.",
    input="What are three major announcements from Microsoft Build this week?",
    tools=[{"type": "web_search"}]
)

print(response.output_text)

print("\n=== Crypto prices ===")
response = client.responses.create(
    model=AZURE_OPENAI_DEPLOYMENT,
    instructions="You are an AI assistant. Use web search when current information is required.",
    input="What is the Price of Bitcoin and the price of Pepe at the moment?",
    tools=[{"type": "web_search"}]
)

print(response.output_text)


print("\n=== VLucht Curacao ===")
response = client.responses.create(
    model=AZURE_OPENAI_DEPLOYMENT,
    instructions="You are an AI assistant. Use web search when current information is required.",
    input="I want to fly from Brussels Zaventem or Dusseldorf to Curacou 17 juli 2027 to 2 august 2027 with one family (4 persons). What does it cost?",
    tools=[{"type": "web_search"}]
)

print(response.output_text)