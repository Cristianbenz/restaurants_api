from flask import Flask, jsonify
from psycopg2 import connect, extras
from dotenv import load_dotenv
from os import environ

load_dotenv()

app = Flask(__name__)
user = environ.get('DB_USERNAME')
password = environ.get('DB_PASSWORD')
host = environ.get('DB_HOST')
port = environ.get('DB_PORT')
database = environ.get('DB_NAME')

def get_conection():
    conn = connect(user=user, password=password, host=host, port=port, database=database)
    return conn

@app.get('/api/restaurants')
def get_restaurants():
    conn = get_conection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute('SELECT * FROM restaurants')
    result = cur.fetchall()

    cur.close()
    conn.close()

    if len(result) == 0:
        return jsonify({"message": "Not exist any restaurant yet"}), 404
    
    return jsonify(result)

if __name__ == "__main__":
    app.run(port=environ.get('PORT'), debug=True)