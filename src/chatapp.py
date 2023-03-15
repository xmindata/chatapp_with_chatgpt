import openai
import os
import sys
import json
import time
from dotenv import load_dotenv


# load the API key from the environment
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

try:
  # Try out the API
  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", # this is "ChatGPT" $0.002 per 1k tokens
    messages=[{"role": "user", "content": "What is the capital of The Netherlands?"}]
  )
  print (completion)
except openai.error.RateLimitError as e:
  print(e)
