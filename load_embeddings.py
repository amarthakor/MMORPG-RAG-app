import os
import csv
from openai import OpenAI
import psycopg2
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_game_data():
    """Load game data from file"""
    with open('Free-to-play-games.txt', 'r') as file:
        return list(csv.reader(file))
    

def generate_embeddings():
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="postgres",
        database="game_data"
    )
    cursor = conn.cursor()

    try:
        game_data = load_game_data()

        for game in game_data:
            title, thumbnail, description, open_url, genre, platform, publisher, developer, release_date, game_url = game

        
            content = f"{title}. {description}. Genre: {genre}. Platform: {platform}"
            embedding = client.embeddings.create(
                model="text-embedding-3-small",
                input=content
            ).data[0].embedding

            cursor.execute(
                """INSERT INTO game_info
                    (title, thumbnail, description, open_url, genre, platform, publisher, developer, release_date, game_url, embedding)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (title, thumbnail, description, open_url, genre, platform, publisher, developer, release_date, game_url, embedding)
            )

        conn.commit()
        print("All embeddings stored successfully!")

    except Exception as e:
        conn.rollback()
        print("Error occured while generating embeddings:", e)

    finally:
        cursor.close()
        conn.close()
    
if __name__ == "__main__":
    generate_embeddings()