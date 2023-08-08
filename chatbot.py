import os
import openai
import sys
from dotenv import load_dotenv
import time
from yaspin import yaspin
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

# -------------------- Configuration --------------------

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
LOG_FILE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "conversation.log")

# -------------------- Helper Functions --------------------

def type_out(message):
    for letter in message:
        if letter == '\n':  # Handle newlines
            print()
        else:
            print(Fore.GREEN + letter, end='', flush=True)  # Using colorama for green text
        time.sleep(0.005)
    print()

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
    
    # Check for token length and reset conversation if it's too long
    total_tokens = sum([len(item['content']) for item in messages])
    if total_tokens > 3000:
        conversation = [{"role": "assistant", "content": "Let's continue our conversation."}]
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        messages.extend(conversation)
    
    with yaspin(text="Sending message...", spinner="dots") as spinner:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            assistant_message = response['choices'][0]['message']['content']
            spinner.ok("✅")
        except Exception as e:
            spinner.fail("❌")
            raise e

    type_out(f"AI: {assistant_message}")
    
    conversation.append({"role": "AI", "content": assistant_message})
    write_to_log(conversation)
    return assistant_message

# -------------------- Main Function --------------------

def main():
    """Main function to handle the user's message and print the assistant's response."""
    conversation = load_conversation()
    user_message = " ".join(sys.argv[1:])
    send_message(conversation, user_message)

# -------------------- Script Execution --------------------

if __name__ == "__main__":
    main()
