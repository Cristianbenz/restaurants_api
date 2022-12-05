from flask import jsonify, request
from psycopg2 import extras
from db import get_connection
import statistics

class Restaurant():
    def __init__(self):
        self.conn = get_connection
    
    def get_restaurants_model(self):
        conn = self.conn()
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

    def create_restaurants_model(self):
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

        conn = self.conn()
        cur = conn.cursor(cursor_factory=extras.RealDictCursor)
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

    def modify_restaurant_model(self, restaurant_id):
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
        conn = self.conn()
        cur = conn.cursor(cursor_factory=extras.RealDictCursor)
        cur.execute(
            "UPDATE restaurants SET rating= %s, name= %s, site= %s, email= %s, phone= %s, street= %s, city= %s, state= %s, lat= %s, lng= %s WHERE id=%s RETURNING *",
            (rating, name, site, email, phone, street, city, state, lat, lng, restaurant_id))

        conn.commit()
        modified_restaurant = cur.fetchone()
        cur.close()
        conn.close()

        return jsonify(modified_restaurant)

    def partially_modify_restaurant_model(self, restaurant_id):
        conn = self.conn()
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

    def statistics_bt_location_model(self, queries):
        latitude = queries.get("latitude")
        longitude = queries.get("longitude")
        radius = queries.get("radius")
        conn = self.conn()
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

