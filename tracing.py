import os
from getpass import getpass
os.environ["OPENAI_API_KEY"] = getpass("OpenAI API key")
# Import open-telemetry dependencies
from arize.otel import register

# Setup OTel via our convenience function

tracer_provider = register(
    space_id = "U3BhY2U6Mjg0MTQ6b01EMw==", # in app space settings page
    api_key = "ak-ce753816-98a6-4807-b334-cbf21bc6d40c-e1EG1IjqzwFNd0NFfxLviTuG5ATnd-LN", # in app space settings page
    project_name = "capstone-rag-demo", # name this to whatever you would like
)

# Import the automatic instrumentor from OpenInference
from openinference.instrumentation.openai import OpenAIInstrumentor

# Finish automatic instrumentation
OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)

import openai

client = openai.OpenAI()
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Write a haiku."}],
    max_tokens=20,
)
print(response.choices[0].message.content)