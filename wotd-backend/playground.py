import os
import psycopg2

ENV_PASSWORD = 'POSTGRES_PASSWORD'
ENV_USER = 'POSTGRES_USER'
ENV_DB_NAME = 'POSTGRES_DB'

if (ENV_PASSWORD not in os.environ) \
        or (ENV_USER not in os.environ) \
        or (ENV_DB_NAME not in os.environ):
    # if ENV_PASSWORD or ENV_USER or ENV_DB_NAME not in os.environ:
    print('invalid environment - shutting down')
    exit(1)

conn = psycopg2.connect(database=os.environ[ENV_DB_NAME],
                        host="localhost",
                        user=os.environ[ENV_USER],
                        password=os.environ[ENV_PASSWORD],
                        port="5432")

cursor = conn.cursor()
cursor.execute("SELECT * FROM students;")
print(cursor.fetchall())
