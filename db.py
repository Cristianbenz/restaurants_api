from psycopg2 import connect
from os import environ

user = environ.get('DB_USERNAME')
password = environ.get('DB_PASSWORD')
host = environ.get('DB_HOST')
port = environ.get('DB_PORT')
database = environ.get('DB_NAME')

def get_connection():
    conn = connect(user=user, password=password,
                   host=host, port=port, database=database)
    return conn