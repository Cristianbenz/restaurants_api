from app import app
from os import environ
from load_restaurants import parse_info
from db import get_connection

if __name__ == '__main__':
    parse_info(get_connection)
    app.run(port=environ.get('PORT'), debug=True)