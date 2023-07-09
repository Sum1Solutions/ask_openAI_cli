#!/bin/zsh

# Activate the virtual environment
source /Users/jb/coding/ask_openAI_cli/env/bin/activate

# Execute the Python script within the virtual environment
python /Users/jb/coding/ask_openAI_cli/chatbot.py "$*"

# Deactivate the virtual environment (but lose all context of prior conversation)
# deactivate
