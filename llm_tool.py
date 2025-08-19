#A tool that takes a technical question, and responds with an explanation. 

# imports
import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
from openai import OpenAI

# constants

MODEL_GPT = "gpt-4o-mini"
MODEL_LLAMA = "llama3.2"
OLLAMA_API = "http://localhost:11434/api/generate"

# set up environment
api_key = "sk-proj-xxxxxxxxxxxxxxxxxxxxxxxx"   # 👈 put your real key here

# Validate API key
if not api_key:
    print("No API key was found - please head over to the troubleshooting notebook in this folder to identify & fix!")
elif not api_key.startswith("sk-proj-"):
    print("An API key was found, but it doesn't start sk-proj-; please check you're using the right key - see troubleshooting notebook")
elif api_key.strip() != api_key:
    print("An API key was found, but it looks like it might have space or tab characters at the start or end - please remove them - see troubleshooting notebook")
else:
    print("API key found and looks good so far!")

openai.api_key = api_key

openai = OpenAI()

# here is the question; type over this to ask something new
question = """
In LLM engineering, what is the difference between prompt engineering and fine-tuning?
When would you choose one over the other?
"""

# Get gpt-4o-mini to answer, with streaming
print("=== Answer from OpenAI GPT-4o-mini ===")
stream = openai.chat.completions.create(
    model=MODEL_GPT,
    messages=[{"role": "user", "content": question}],
    stream=True
)

for chunk in stream:
    delta = chunk.choices[0].delta
    if delta and delta.content:   # safer than using .get()
        print(delta.content, end="", flush=True)

print("\n")

# Get Llama 3.2 to answer
print("=== Answer from Ollama Llama 3.2 ===")
response = requests.post(
    OLLAMA_API,
    json={"model": MODEL_LLAMA, "prompt": question, "stream": False},
    stream=False
)
print(response.json().get("response", "No response"))
