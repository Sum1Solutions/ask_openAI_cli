#!/bin/zsh

# Set log file path
LOG_FILE_PATH="/Users/jb/coding/ask_openAI_cli/conversation.log"

# Check for flags
if [[ $1 == "-c" ]] || [[ $1 == "-x" ]]
then
    flag=$1
    shift

    case "${flag}"
    in
    -c) cat $LOG_FILE_PATH;;  # If -c, print the log file
    -x) rm $LOG_FILE_PATH;;  # If -x, delete the log file
    esac
fi

# Activate the virtual environment
source /Users/jb/coding/ask_openAI_cli/env/bin/activate

# Execute the Python script within the virtual environment
python3 /Users/jb/coding/ask_openAI_cli/chatbot.py "$*"

# Deactivate the virtual environment (but lose all context of prior conversation)
# deactivate
