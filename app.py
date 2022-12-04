from flask import Flask, jsonify, request
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

def get_connection():
    conn = connect(user=user, password=password, host=host, port=port, database=database)
    return conn

@app.get('/api/restaurants')
def get_restaurants():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute('SELECT * FROM restaurants')
    result = cur.fetchall()

    cur.close()
    conn.close()

    if len(result) == 0:
        return jsonify({"message": "Not exist any restaurant yet"}), 404
    
    return jsonify(result)

@app.post('/api/restaurant')
def create_restaurant():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    data = request.get_json()
    rating = data["rating"]
    id = data["id"]
    name = data["name"]
    site = data["site"]
    email = data["email"]
    phone = data['phone']
    street = data["street"]
    city = data["city"]
    state = data["state"]
    lat = data["lat"]
    lng = data["lng"]

    cur.execute(
        "INSERT INTO restaurants (id, rating, name, site, email, phone, street, city, state, lat, lng) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *",
        (id, rating, name, site, email, phone, street, city, state, lat, lng))
    conn.commit()
    new_restaurant = cur.fetchone()

    cur.close()
    conn.close()

    if new_restaurant is None:
        return jsonify({"message":"Restaurant not found"}), 404

    return jsonify(new_restaurant)

if __name__ == "__main__":
    app.run(port=environ.get('PORT'), debug=True)