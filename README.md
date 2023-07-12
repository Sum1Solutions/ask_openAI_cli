1. Clone the repository:


```
git clone https://github.com/Sum1Solutions/ask_openAI_cli.git
```

2. Create a virtual environment and activate it:

```
python3 -m venv myenv
source myenv/bin/activate
```

3. Install the required packages:

```
pip install -r requirements.txt
```

4. Create a .env file and add your OpenAI API key:

```
OPENAI_API_KEY=your-api-key
```

5. Run the app:

```
python app.py "Replace HERE with the message you want to send to the LLM, in quotes"
```


6. Get the response:

The app will print the model's response to your message.

Note: The conversation history is stored in a log file called conversation.log in the same directory as the app. If the log file exists, the app will load the conversation history from the file. Otherwise, it will start a new conversation.

You can deactivate the virtual environment when you're done:

```
deactivate
```