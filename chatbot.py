import os
import openai
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API client
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define conversation history
conversation = []

# Load conversation history from the log file
log_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "conversation.log")
if os.path.exists(log_file):
    with open(log_file, "r") as f:
        conversation_lines = f.read().splitlines()
        conversation = [{"role": "user" if line.split(": ")[0] == "User" else "assistant", 
                         "content": ": ".join(line.split(": ")[1:])} 
                        for line in conversation_lines]
else:
    conversation = [{"role": "assistant", "content": "Hello! How can I assist you today?"}]


def send_message(message):
    # Add the user's message to the conversation
    conversation.append({"role": "user", "content": message})

    # Start messages with the system message
    messages = [{"role": "system", "content": "You are a helpful assistant."}]

    # Add the rest of the conversation to messages
    messages.extend(conversation)

    # Send the messages to the API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # You may change this to text-davinci-003 if you prefer
        messages=messages
    )

    # Get the assistant's response
    assistant_message = response['choices'][0]['message']['content']

    # Add the assistant's message to the conversation
    conversation.append({"role": "AI", "content": assistant_message})

    # Save the updated conversation history to the log file
    with open(log_file, "w") as f:
        f.write("\n".join([f"{item['role']}: {item['content']}" for item in conversation]))

    # Return the assistant's message
    return assistant_message

# Get user's message from command-line argument
user_message = " ".join(sys.argv[1:])

# Send the user's message to the chatbot and print the response
response = send_message(user_message)
print(response)
