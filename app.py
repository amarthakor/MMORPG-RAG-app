from game_search import get_similar_games
from openai import OpenAI
import os
from dotenv import load_dotenv
from arize.otel import register
tracer_provider = register(
    space_id = "U3BhY2U6Mjg0MTQ6b01EMw==", # in app space settings page
    api_key = "ak-ce753816-98a6-4807-b334-cbf21bc6d40c-e1EG1IjqzwFNd0NFfxLviTuG5ATnd-LN", # in app space settings page
    project_name = "capstone-rag-demo", # name this to whatever you would like
)

# Import the automatic instrumentor from OpenInference
from openinference.instrumentation.openai import OpenAIInstrumentor

# Finish automatic instrumentation
OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def search_games(query):
    if not query.strip():
        return "Please enter a search query"
    
    results = get_similar_games(query, top_k=5)

    if not results:
        return "No results were found for your query"
    
    try:
        results_text = ''
        for g in results:
            results_text += f"- {g['title']} ({g['genre']}, {g['platform']}, {g['release_date']}): {g['description']}\n"

        prompt = f""" 
        A user searched for {query}

        Here are the most relevant games found:

        {results_text}

        Provide a natural and conversational response that includes the following:
        1. If the user asks about a specific game, try to answer their question.
        2. Offer 3-5 suggestions if they ask for recommendations
        3. Ask them for their thoughts.

        Keep the response friendly and helpful, 3-4 sentences long.
        """

        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that is knowledgeable about MMORPGs"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=250,
            temperature=0.7
        )

        llm_summary = response.choices[0].message.content.strip()

        return llm_summary
    
    except Exception as e:
        print(f"There was an error with the LLM: {e}")
        output = f"Found {len(results)} results for: '{query}'\n\n"

        return output

if __name__ == "__main__":
    print("Welcome to your Game Assistant! Type 'quit' or 'exit' to stop.\n")
    
    while True:
        query = input("Enter your game query: ").strip()
        if query.lower() in ("quit", "exit"):
            print("Goodbye! 👋")
            break

        response = search_games(query)
        print("\n" + response + "\n")