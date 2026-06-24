from openai import OpenAI
from shared.config import (
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_KEY
)
from pathlib import Path

# Determine the location of the knowledge base file relative to this script.
# This makes the project portable across different machines and environments.
ROOT_DIR = Path(__file__).parent.parent
DATA_FILE = ROOT_DIR / "data" / "retro-dos-race-games.md"

print(f"Data file path: {DATA_FILE}")

# Create an Azure OpenAI client using the shared project configuration.
client = OpenAI(
    base_url=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY
)

# Create a temporary vector store and upload the knowledge base document.
# The file will be indexed automatically and made available for semantic search.
vector_store = client.vector_stores.create(
    name="dosracegames-docs"
)

with open(DATA_FILE, "rb") as file:
    client.vector_stores.files.upload_and_poll(
        vector_store_id=vector_store.id,
        file=file
    )

# Query the knowledge base using the File Search tool.
# The model will retrieve relevant document fragments before generating a response.
response = client.responses.create(
    model=AZURE_OPENAI_DEPLOYMENT,
    instructions=(
        "You are an AI assistant that provides information "
        "from a MS-DOS racing games knowledge base."
    ),
    input="What are the best cars and drivers for each MS-DOS racing game in the knowledge base?",
    tools=[
        {
            "type": "file_search",
            "vector_store_ids": [vector_store.id]
        }
    ],
    include=["file_search_call.results"]
)

# Display the generated answer.
print(response.output_text)