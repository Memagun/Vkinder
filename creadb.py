import psycopg2


def create_db():
    conn = psycopg2.connect(database="", user="", password="")
    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE IF NOT EXIST vkinder_candidates(
                    id SERIAL PRIMARY KEY,
                    first_name varchar(50) NOT NULL,
                    last_name varchar(50) NOT NULL""")
    conn.close()


def add_candidate(candidate, cursor):
    cursor.execute("""
    INSERT into vkinder_candidates (id, first_name, last_name, domain)
    values(%s, %s, %s)
    returning id""", (candidate["id"], candidate["first_name"], candidate["last_name"]))
    candidate_id = cursor.fetchone()[0]
    return candidate_id





if __name__ == "__main__":
    create_db()
    add_candidate() #add user

