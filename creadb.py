import psycopg2
from config import *

conn = psycopg2.connect(database=database, user=user, password=password)
conn.autocommit = True


def create_db():
    with conn.cursor() as cur:
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS vkinder_candidates(
                        id SERIAL PRIMARY KEY,
                        ids_f INTEGER UNIQUE,
                        user_id INTEGER);
                        """)
        # cur.closed()


def add_candidate(user_id, ids_f):
    with conn.cursor() as cur:
        cur.execute(
            f"""INSERT INTO vkinder_candidates (user_id, founded_id)
                VALUES (%s, %s)""", (user_id, ids_f)
        )
    # cur.closed()


def data_check():
    with conn.cursor() as cur:
        cur.execute(
            f"""SELECT founded_id FROM vkinder_candidates;"""
        )
        vkinder_candidates = cur.fetchall()
    # cur.closed()
        return vkinder_candidates


def drop_users():
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE IF EXIST vkinder_candidates CASCADE;""")
    # cur.closed()


if __name__ == "__main__":
    create_db()
