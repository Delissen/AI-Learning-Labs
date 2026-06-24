# Exercise:
# https://microsoftlearning.github.io/mslearn-ai-studio/Instructions/Exercises/04a-use-own-data.html
#
# Demonstrates:
# - Creating a Vector Store
# - Uploading and indexing PDF documents
# - Using the File Search tool
# - Combining File Search with Web Search
# - Maintaining conversational context using previous_response_id

import os
from dotenv import load_dotenv
import glob
from pathlib import Path

from openai import OpenAI
from shared.config import (
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_KEY
)

# Example questions:
# - What's happening in San Francisco next month?
# - What hotels does Margie's Travel offer there?




def main():

    

    # Clear the console for a cleaner interactive experience.
    os.system('cls' if os.name == 'nt' else 'clear')

    try:

        instructions="""
                You are a travel assistant that provides information
                on travel services available from Margie's Travel.

                Answer questions about services offered by Margie's Travel
                using the provided travel brochures.

                Search the web for general information about destinations
                or current travel advice.
                """
                
        instructions2="""
                You are a travel assistant for Margie's Travel.

                Always answer questions using information found in the uploaded travel brochures.

                When hotel information is available in the brochures:
                - Include hotel names.
                - Include hotel descriptions.
                - Include available amenities.
                - Include location information.

                If the requested information cannot be found in the brochures, clearly state:
                'This information is not available in the Margie's Travel brochures.'

                Do not make assumptions or invent hotel information.
                """

        instructions3="""
                You are a travel assistant for Margie's Travel.

                Answer exclusively using information retrieved from the uploaded brochures.

                Never use prior knowledge.
                Never generate information that is not explicitly present in the brochures.

                If information is missing, say:
                'I could not find this information in the travel brochures.'
                """

        # Load Azure OpenAI configuration from the .env file.
        load_dotenv()

        model_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

        print("Model deployment:", model_deployment)

        # Create an Azure OpenAI client.
        openai_client = OpenAI(
            base_url=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_API_KEY
        )

        # Locate all PDF travel brochures that will be indexed.
        ROOT_DIR = Path(__file__).parent.parent
        DATA_FILES = ROOT_DIR / "data" / "brochures" / "*.pdf"

        # Create a Vector Store.
        # Uploaded documents are automatically chunked, embedded,
        # and indexed for semantic search.
        print("Creating vector store and uploading files...")

        vector_store = openai_client.vector_stores.create(
            name="travel-brochures"
        )

        file_streams = [
            open(f, "rb")
            for f in glob.glob(str(DATA_FILES))
        ]

        if not file_streams:
            print("No PDF files found in the brochures folder!")
            return

        # Upload and process all brochure documents.
        file_batch = openai_client.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id,
            files=file_streams
        )

        for f in file_streams:
            f.close()

        print(
            f"Vector store created with "
            f"{file_batch.file_counts.completed} files."
        )

        # Maintain conversation history between requests.
        last_response_id = None

        # Interactive question-and-answer loop.
        while True:

            input_text = input(
                '\nEnter a question (or type "quit" to exit): '
            )

            if input_text.lower() == "quit":
                break

            if len(input_text) == 0:
                print("Please enter a question.")
                continue

            # The model can use:
            # 1. File Search for information contained in the brochures
            # 2. Web Search for current destination information
            response = openai_client.responses.create(
                model=model_deployment,
                instructions=instructions3,
                input=input_text,
                previous_response_id=last_response_id,
                tools=[
                    {
                        "type": "file_search",
                        "vector_store_ids": [vector_store.id]
                    },
                    {
                        "type": "web_search"
                    }
                ]
            )

            print(response.output_text)

            # Store the response ID to preserve conversation context.
            last_response_id = response.id

    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()