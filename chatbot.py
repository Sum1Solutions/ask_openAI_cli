import os
import openai
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set the log file path
LOG_FILE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "conversation.log")

def sanitize_input(input_string):
    """Sanitize the input string by removing certain special characters."""
    
    # Define characters to remove
    chars_to_remove = ['?', "'"]
    
    # Remove defined characters from the input string
    sanitized_string = ''.join([char for char in input_string if char not in chars_to_remove])
    
    return sanitized_string

def load_conversation():
    """Load conversation history from the log file."""
    
    # Check if the log file exists
    if os.path.exists(LOG_FILE_PATH):
        # If the log file exists, read it and construct the conversation history
        with open(LOG_FILE_PATH, "r") as f:
            conversation_lines = f.read().splitlines()
            return [{"role": "user" if line.split(": ")[0] == "User" else "assistant", 
                     "content": ": ".join(line.split(": ")[1:])} 
                    for line in conversation_lines]
    else:
        # If the log file does not exist, start a new conversation
        return [{"role": "assistant", "content": "Hello! How can I assist you today?"}]

def write_to_log(conversation):
    """Write the conversation history to the log file."""
    
    with open(LOG_FILE_PATH, "w") as f:
        f.write("\n".join([f"{item['role']}: {item['content']}" for item in conversation]))

def send_message(conversation, message):
    """Send a message to the OpenAI API and receive the assistant's response."""
    
    # Add the user's message to the conversation history
    conversation.append({"role": "user", "content": message})
    
    # Construct the messages to be sent to the API
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    messages.extend(conversation)
    
    # Send the messages to the API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Change this to another model if you prefer
        messages=messages
    )
    
    # Extract the assistant's response
    assistant_message = response['choices'][0]['message']['content']
    
    # Add the assistant's response to the conversation history
    conversation.append({"role": "AI", "content": assistant_message})
    
    # Write the updated conversation history to the log file
    write_to_log(conversation)
    
    # Return the assistant's response
    return assistant_message

def main():
    """Main function to handle the user's message and print the assistant's response."""
    
    # Load the conversation history
    conversation = load_conversation()
    
    # Get the user's message from the command-line arguments
    user_message = " ".join(sys.argv[1:])
    
    # Sanitize the user's message
    sanitized_user_message = sanitize_input(user_message)
    
    # Send the sanitized user's message to the chatbot and get the response
    response = send_message(conversation, sanitized_user_message)
    
    # Print the response
    print(response)

# Run the main function if the script is run directly
if __name__ == "__main__":
    main()
