import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="postgres",
    database="game_data"
)

cur = conn.cursor()

try:
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS game_info (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            thumbnail TEXT NOT NULL,
            description TEXT NOT NULL,
            open_url TEXT NOT NULL,
            genre TEXT NOT NULL,
            platform TEXT NOT NULL,
            publisher TEXT NOT NULL,
            developer TEXT NOT NULL,
            release_date DATE NOT NULL,
            game_url TEXT NOT NULL,
            embedding vector(1536)
        );
    """)
    conn.commit()
    print("Database setup complete!")
except Exception as e:
    print("Error during setup:", e)
finally:
    cur.close()
    conn.close()