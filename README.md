# OpenAI Chatbot CLI

This project allows you to communicate with an OpenAI-powered chatbot via the command line.

## Setup

1. Clone the repository to your local machine.

2. Install the required dependencies: `openai` and `python-dotenv`. This can be done using pip:

    ```
    pip install openai python-dotenv
    ```

3. Add your OpenAI API key to a .env file in the project's root directory, like so:

    ```
    OPENAI_API_KEY=<Your-API-Key>
    ```

4. Add execution permission to the shell script:

    ```
    chmod +x ask.sh
    ```

5. Optionally, you can add an alias for the shell script to your shell configuration file (e.g., .bashrc, .zshrc) to easily call the chatbot from anywhere:

    ```
    alias ask='/path/to/ask.sh'
    ```

    Don't forget to source your shell configuration file or restart your terminal after adding the alias.

## Usage

After setting up the project, you can interact with the chatbot by typing `ask` followed by your question or command enclosed in double quotes. For example:

- ask "What's the weather like?"

The chatbot will respond in the terminal.

### Special Commands

In addition to chatting, this script provides special commands:

- `ask -c "your question"`: This will print the current conversation history and proceed with your new question.
- `ask -x "your question"`: This will delete the conversation history and proceed with your new question.

## Notes

This chatbot uses the OpenAI API and the gpt-3.5-turbo model. The conversation history is saved in a file named `conversation.log` in the project's root directory.

OpenAI did the heavy lifting: 

https://chat.openai.com/share/b95a8c63-509b-4b45-bdf0-f696516b0ef7
