from dotenv import load_dotenv
import os

load_dotenv()
db_url = os.getenv("DATABASE_URL")
import psycopg

conn = psycopg.connect(db_url)
print("Connected successfully!")
with conn.cursor() as cur:
       cur.execute("""CREATE TABLE IF NOT EXISTS tasks (
    id serial primary key,
    title text,
    done boolean
)""")
conn.commit()

with conn.cursor() as cur:
    cur.execute("SELECT COUNT (*) FROM tasks")
    count = cur.fetchone()[0]
    if count == 0:
        cur.execute("INSERT INTO tasks (title, done) VALUES(%s, %s)", ('build', True))
        cur.execute("INSERT INTO tasks (title, done) VALUES(%s, %s)", ('swim', False))
        cur.execute("INSERT INTO tasks (title, done) VALUES(%s, %s)", ('eat', True))
conn.commit()


