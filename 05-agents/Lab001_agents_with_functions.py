"""
Lab001 - Agents with Functions

AI-103 Learning Lab

Lab description: https://microsoftlearning.github.io/mslearn-ai-agents/Instructions/Exercises/01-build-agent-portal-and-vscode.html

Dit script maakt verbinding met een Azure AI Foundry Agent
en start een interactieve chat-sessie.

De agent kan:
- Knowledge Files gebruiken
- Code Interpreter uitvoeren
- Grafieken genereren
- Bestanden teruggeven aan de gebruiker

Benodigde configuratie:
- FOUNDRY_PROJECT_ENDPOINT
- FOUNDRY_AGENT_NAME

Authenticatie:
- Azure Login via DefaultAzureCredential

Sample Questions:
-  What's the policy for password resets?
-  Analyze the system performance data and identify any periods where CPU usage exceeded 80%
-  What are the average, minimum, and maximum values for disk usage in the performance data?
-  Find any correlation between high CPU usage and memory usage in the performance data

"""

import base64
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

from shared.config import (
    FOUNDRY_AGENT_NAME,
    FOUNDRY_PROJECT_ENDPOINT,
)

# Directory waarin bestanden die door de Agent worden gegenereerd
# lokaal worden opgeslagen.
OUTPUT_DIR = Path("agent_outputs")


# ============================================================
# Configuration
# ============================================================

def validate_configuration() -> None:
    """
    Controleer of alle verplichte configuratie aanwezig is.
    """

    if not FOUNDRY_PROJECT_ENDPOINT:
        raise ValueError("FOUNDRY_PROJECT_ENDPOINT ontbreekt")

    if not FOUNDRY_AGENT_NAME:
        raise ValueError("FOUNDRY_AGENT_NAME ontbreekt")


def create_project_client() -> AIProjectClient:
    """
    Maak verbinding met Azure AI Foundry.

    DefaultAzureCredential gebruikt de actieve Azure login
    (Visual Studio, Azure CLI of Azure Account Extension).
    """

    credential = DefaultAzureCredential()

    return AIProjectClient(
        credential=credential,
        endpoint=FOUNDRY_PROJECT_ENDPOINT
    )


# ============================================================
# File Handling
# ============================================================

def get_output_path(filename: str) -> Path:
    """
    Maak een uniek bestandspad aan zodat bestaande bestanden
    niet worden overschreven.
    """

    OUTPUT_DIR.mkdir(exist_ok=True)

    file_name = Path(filename).name
    stem = Path(file_name).stem or "output"
    suffix = Path(file_name).suffix

    output_path = OUTPUT_DIR / file_name

    counter = 1

    while output_path.exists():
        output_path = OUTPUT_DIR / f"{stem}_{counter}{suffix}"
        counter += 1

    return output_path


def save_bytes(file_bytes: bytes, filename: str) -> Path:
    """
    Sla binaire data lokaal op.
    """

    output_path = get_output_path(filename)

    with open(output_path, "wb") as file_handle:
        file_handle.write(file_bytes)

    return output_path


def save_image(image_data: str, filename: str) -> Path:
    """
    Decodeer Base64 afbeelding en sla deze lokaal op.
    """

    return save_bytes(
        base64.b64decode(image_data),
        filename
    )


def download_container_file(
    openai_client,
    annotation,
    downloaded_files: dict
) -> Path:
    """
    Download een bestand uit de Agent sandbox.

    Voorkomt dubbele downloads door gebruik te maken van caching.
    """

    cache_key = (
        annotation.container_id,
        annotation.file_id
    )

    if cache_key in downloaded_files:
        return downloaded_files[cache_key]

    file_content = openai_client.containers.files.content.retrieve(
        file_id=annotation.file_id,
        container_id=annotation.container_id
    )

    output_path = save_bytes(
        file_content.read(),
        annotation.filename or f"{annotation.file_id}.bin"
    )

    downloaded_files[cache_key] = output_path

    return output_path


# ============================================================
# Response Processing
# ============================================================

def format_output_text(
    content_item,
    openai_client,
    downloaded_files: dict
):
    """
    Vervang sandbox file references door lokale bestandspaden.
    """

    text = content_item.text or ""

    replacements = []
    referenced_files = set()

    for annotation in content_item.annotations or []:

        if getattr(annotation, "type", "") != "container_file_citation":
            continue

        output_path = download_container_file(
            openai_client,
            annotation,
            downloaded_files
        )

        replacement_text = (
            f"{annotation.filename} "
            f"(saved to {output_path})"
        )

        referenced_files.add(output_path)

        start_index = getattr(annotation, "start_index", None)
        end_index = getattr(annotation, "end_index", None)

        if start_index is not None and end_index is not None:
            replacements.append(
                (
                    start_index,
                    end_index,
                    replacement_text
                )
            )
            continue

        annotated_text = getattr(annotation, "text", "")

        if annotated_text:
            text = text.replace(
                annotated_text,
                replacement_text
            )

    for start_index, end_index, replacement_text in sorted(
        replacements,
        reverse=True
    ):
        text = (
            f"{text[:start_index]}"
            f"{replacement_text}"
            f"{text[end_index:]}"
        )

    return text, referenced_files


def get_agent_response(
    openai_client,
    conversation_id: str,
    agent_name: str
):
    """
    Vraag een antwoord op bij de Azure AI Foundry Agent.
    """

    return openai_client.responses.create(
        conversation=conversation_id,
        extra_body={
            "agent_reference": {
                "name": agent_name,
                "type": "agent_reference"
            }
        },
        input=""
    )


# ============================================================
# UI
# ============================================================

def show_banner() -> None:
    """
    Toon applicatiebanner.
    """

    print("\n" + "=" * 60)
    print("Azure AI Foundry Agent")
    print("=" * 60)
    print("Type 'exit' om af te sluiten.")
    print()


# ============================================================
# Main
# ============================================================

def main() -> None:

    load_dotenv()

    validate_configuration()

    print("Connecting to Microsoft Foundry project...")

    project_client = create_project_client()

    openai_client = project_client.get_openai_client()

    print(f"Loading agent: {FOUNDRY_AGENT_NAME}")

    agent = project_client.agents.get(
        agent_name=FOUNDRY_AGENT_NAME
    )

    print(
        f"Connected to agent: "
        f"{agent.name} "
        f"(id: {agent.id})"
    )

    conversation = openai_client.conversations.create(
        items=[]
    )

    print(
        f"Conversation created "
        f"(id: {conversation.id})"
    )

    show_banner()

    while True:

        user_input = input("You: ").strip()

        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break

        if not user_input:
            continue

        openai_client.conversations.items.create(
            conversation_id=conversation.id,
            items=[
                {
                    "type": "message",
                    "role": "user",
                    "content": user_input
                }
            ]
        )

        print("\n[Agent is thinking...]\n")

        try:

            response = get_agent_response(
                openai_client,
                conversation.id,
                agent.name
            )

        except Exception as ex:

            print("\nAgent error:")
            print(ex)
            print()

            continue

        handled_output = False
        downloaded_files = {}
        referenced_files = set()
        image_count = 0

        if hasattr(response, "output") and response.output:

            for item in response.output:

                item_type = getattr(item, "type", "")

                if item_type == "message" and getattr(item, "content", None):

                    for content_item in item.content:

                        if getattr(content_item, "type", "") != "output_text":
                            continue

                        formatted_text, message_files = format_output_text(
                            content_item,
                            openai_client,
                            downloaded_files
                        )

                        referenced_files.update(message_files)

                        if formatted_text:
                            print(f"\nAgent: {formatted_text}\n")
                            handled_output = True

                elif hasattr(item, "text") and item.text:

                    print(f"\nAgent: {item.text}\n")
                    handled_output = True

                elif item_type == "image":

                    image_count += 1

                    filename = f"chart_{image_count}.png"

                    if (
                        hasattr(item, "image")
                        and hasattr(item.image, "data")
                    ):
                        file_path = save_image(
                            item.image.data,
                            filename
                        )

                        print(
                            f"\n[Agent generated a chart - "
                            f"saved to: {file_path}]"
                        )

                    else:
                        print("\n[Agent generated an image]")

                    handled_output = True

            for file_path in downloaded_files.values():

                if file_path not in referenced_files:

                    print(
                        f"\n[Agent generated a file - "
                        f"saved to: {file_path}]"
                    )

                    handled_output = True

        if (
            not handled_output
            and hasattr(response, "output_text")
            and response.output_text
        ):
            print(f"\nAgent: {response.output_text}\n")


if __name__ == "__main__":
    main()