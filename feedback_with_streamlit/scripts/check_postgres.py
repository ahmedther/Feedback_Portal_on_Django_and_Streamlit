import os
import psycopg2
import time


while True:
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )
        print("PostgreSQL server is available")
        conn.close()
        break  # Break the loop if connection successful
    except psycopg2.OperationalError:
        print("PostgreSQL server is not available. Retrying in 1 second...")
        time.sleep(1)
