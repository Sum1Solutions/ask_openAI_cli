import os
import openai
import sys
from dotenv import load_dotenv
import time
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# -------------------- Configuration --------------------

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set the log file path
LOG_FILE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "conversation.log")

# -------------------- Helper Functions --------------------

def type_out(message):
    for letter in message:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(0.005)
    print()

def sanitize_input(input_string):
    """Sanitize the input string by removing certain special characters."""
    chars_to_remove = ['?', "'"]
    sanitized_string = ''.join([char for char in input_string if char not in chars_to_remove])
    return sanitized_string

def print_response(response):
    """Print the response history in a readable format using 'rich' library."""
    console = Console()

    # # Indented response
    # console.print("\nIndented response:", style="bold underline")
    # console.print(console.indent(response, level=2))

    # Bold color response
    console.print(f"\nChat GPT-3.5 Turbo Output", style="bold underline")
    rprint(f"[cyan]{response}[/cyan]")

    # # Panel response
    # console.print("\nPanel response:", style="bold underline")
    # panel = Panel(Text(response, justify="center"))
    # console.print(panel)

# -------------------- Conversation Handling --------------------

def load_conversation():
    """Load conversation history from the log file."""
    if os.path.exists(LOG_FILE_PATH):
        with open(LOG_FILE_PATH, "r") as f:
            conversation_lines = f.read().splitlines()
            return [{"role": "user" if line.split(": ")[0] == "User" else "assistant", 
                     "content": ": ".join(line.split(": ")[1:])} 
                    for line in conversation_lines]
    else:
        return [{"role": "assistant", "content": "Hello! How can I assist you today?"}]

def write_to_log(conversation):
    """Write the conversation history to the log file."""
    with open(LOG_FILE_PATH, "w") as f:
        f.write("\n".join([f"{item['role']}: {item['content']}" for item in conversation]))

def send_message(conversation, message):
    """Send a message to the OpenAI API and receive the assistant's response."""
    conversation.append({"role": "user", "content": message})
    
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    messages.extend(conversation)
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    
    assistant_message = response['choices'][0]['message']['content']
    
    conversation.append({"role": "AI", "content": assistant_message})
    
    write_to_log(conversation)
    
    print_response(assistant_message)  # Print response in multiple ways
    
    return assistant_message

# -------------------- Main Function --------------------

def main():
    """Main function to handle the user's message and print the assistant's response."""
    conversation = load_conversation()
    user_message = " ".join(sys.argv[1:])
    sanitized_user_message = sanitize_input(user_message)
    send_message(conversation, sanitized_user_message)

# -------------------- Script Execution --------------------

if __name__ == "__main__":
    main()
