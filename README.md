# 🕶️ TopGPT 🕶️
 a satirical GPT-powered chatbot using Andrew Tate's tweets in a vector database
 
## Overview
This is a satirical QA bot built with a gpt + langchain backend, which uses a vector database of all of Andrew Tate's tweets to imitate him when answering questions. Prompts will have dynamic contexts that will return the most relevant of Andrew's existing tweets to a user's input, which are then used to generate a response.

## How to run
You will need a local copy of this repo, as well as Python (this app was built on 3.10, but I think 3.8+ will do), and an OpenAI API Key (and some money, if your free trial has run out).

In terms of funky packages, there's:
- streamlit
- langchain
- tiktoken
- openai
- snscrape
- chromadb

(apologies - I didn't build this in a venv and pipreqs refuses to work)

I'm sure there is a way for this to be run remotely, or perhaps I could publish this "dashboard" on streamlit, but I am a silly little boy.
