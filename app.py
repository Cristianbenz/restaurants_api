from flask import Flask, jsonify, request
from psycopg2 import connect, extras
from dotenv import load_dotenv
from os import environ
from load_restaurants import parse_info
import statistics

load_dotenv()

app = Flask(__name__)
user = environ.get('DB_USERNAME')
password = environ.get('DB_PASSWORD')
host = environ.get('DB_HOST')
port = environ.get('DB_PORT')
database = environ.get('DB_NAME')


def get_connection():
    conn = connect(user=user, password=password,
                   host=host, port=port, database=database)
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

    return jsonify({
        "total": len(result),
        "results": result
    })


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
        return jsonify({"message": "Restaurant not found"}), 404

    return jsonify(new_restaurant)


@app.put('/api/restaurant/<restaurant_id>')
def modify_restaurant(restaurant_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    data = request.get_json()
    rating = data["rating"]
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
        "UPDATE restaurants SET rating= %s, name= %s, site= %s, email= %s, phone= %s, street= %s, city= %s, state= %s, lat= %s, lng= %s WHERE id=%s RETURNING *",
        (rating, name, site, email, phone, street, city, state, lat, lng, restaurant_id))

    conn.commit()
    modified_restaurant = cur.fetchone()
    cur.close()
    conn.close()

    return jsonify(modified_restaurant)

@app.patch('/api/restaurant/<restaurant_id>')
def partial_modify_restaurant(restaurant_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    
    data = request.get_json()
    qry = "UPDATE restaurants SET "

    for key in data:
        qry += f"{key}={data[key]},"

    qry = qry[:-1] + f" WHERE id='{restaurant_id}' RETURNING *"

    cur.execute(qry)

    conn.commit()
    modified_restaurant = cur.fetchone()
    cur.close()
    conn.close()

    return jsonify(modified_restaurant)


@app.get('/api/restaurants/statistics')
def get_by_location():
    queries = request.args
    latitude = queries["latitude"]
    longitude = queries["longitude"]
    radius = queries["radius"]

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute(
        f"SELECT rating, name FROM restaurants r WHERE (ST_DWithin('POINT({latitude} {longitude})'::geography, ('POINT('|| r.lat || ' ' || r.lng ||')')::geography, {radius}))")
    result = cur.fetchall()
    cur.close()
    conn.close()

    if len(result) < 1:
        return jsonify({"message": "Not exist any restaurant into the gave zone"}), 404
    
    rating = [restaurant["rating"] for restaurant in result]
    count = len(result)
    avg = statistics.mean(rating)
    std = 0

    if len(rating) > 2:
        std = statistics.stdev(rating)
    
    return jsonify({
        "count": count,
        "avg": avg,
        "std": std
    })


if __name__ == "__main__":
    parse_info(get_connection)
    app.run(port=environ.get('PORT'), debug=True)
