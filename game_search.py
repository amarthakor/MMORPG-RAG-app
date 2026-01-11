import os
import psycopg2
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        user="postgres",
        password='gonoles123',
        database="game_data"
    )

def get_similar_games(query, top_k=5):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=[query]
    )

    query_embedding = response.data[0].embedding

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT title, description, genre, platform, publisher, developer,
                    release_date, embedding <=> %s::vector as distance
            FROM game_info
            ORDER BY distance
            LIMIT %s
        """, (query_embedding, top_k))

        results = []
        for row in cursor.fetchall():
            results.append({
                'title': row[0],
                'description': row[1],
                'genre': row[2],
                'platform': row[3],
                'publisher': row[4],
                'developer': row[5],
                'release_date': row[6],
                'similarity': 1 - row[7]
            })

        return results
    except Exception as e:
        print(f"Error searching database: {e}")
        return []
    
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print('Testing functionality...')
    test_query = "What action games were released by Blizzard in 2022?"
    print(f"\nSearching for: {test_query}")

    results = get_similar_games(test_query, top_k=5)

    if results:
        print(f"\nFound {len(results)} results: ")
        for g in results:
            print(g['title'], g['similarity'])
    else:
        print('No results found')