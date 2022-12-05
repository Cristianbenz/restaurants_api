from psycopg2 import connect
from os import environ
from load_restaurants import parse_info

user = environ.get('DB_USERNAME')
password = environ.get('DB_PASSWORD')
host = environ.get('DB_HOST')
port = environ.get('DB_PORT')
database = environ.get('DB_NAME')

def get_connection():
    conn = connect(user=user, password=password,
                   host=host, port=port, database=database)
    return conn

parse_info(get_connection)