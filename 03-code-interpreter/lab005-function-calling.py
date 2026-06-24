import time
from openai import OpenAI
from shared.config import (
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_KEY)

# Local function that can be called by the model.
# In a real-world scenario this could retrieve weather data,
# query a database, call an API, or execute business logic.
def get_time():
    return f"The time is {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"


def main():

    # Create Azure OpenAI client
    client = OpenAI(
        base_url=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY
    )

    # Register available functions.
    # The model can decide when one of these tools should be used.
    function_tools = [
        {
            "type": "function",
            "name": "get_time",
            "description": "Get the current time"
        }
    ]

    # Start the conversation with a system/developer instruction.
    messages = [
        {
            "role": "developer",
            "content": "You are an AI assistant that provides information."
        }
    ]

    # Continue accepting user prompts until 'quit' is entered.
    while True:

        prompt = input("\nEnter a prompt (or type 'quit' to exit)\n")

        if prompt.lower() == "quit":
            break

        # Add the user message to the conversation history.
        messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        # Send the conversation to the model.
        # The model may either answer directly or request a function call.
        response = client.responses.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            input=messages,
            tools=function_tools
        )

        # Store the model response in the conversation history.
        messages += response.output

        # Check whether the model requested a tool call.
        # Model evaluates the prompt - It determines whether a function call is needed.
        for item in response.output:

            if item.type == "function_call" and item.name == "get_time":

                # Execute the local Python function.
                current_time = get_time()

                # Return the function result back to the model.
                messages.append(
                    {
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": current_time
                    }
                )

                # Ask the model to generate a final response
                # using the function result.
                response = client.responses.create(
                    model=AZURE_OPENAI_DEPLOYMENT,
                    instructions="Answer only with the tool output.",
                    input=messages,
                    tools=function_tools
                )

        # Display the final answer.
        print(response.output_text)


# Application entry point
if __name__ == '__main__':
    main()
