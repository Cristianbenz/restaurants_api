from csv import DictReader
restaurants_list = list()


def parse_info(get_conn):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM restaurants")
    result = cur.fetchall()
    cur.close()
    conn.close()
    if len(result) < 1:
        with open('restaurantes.csv', encoding='utf8') as info:
            reader = DictReader(info)
            for row in reader:
                restaurants_list.append({
                    "id": row["id"],
                    "rating": row['rating'],
                    "name": row['name'],
                    "site": row["site"],
                    "email": row["email"],
                    "phone": row["phone"],
                    "street": row["street"],
                    "city": row['city'],
                    "state": row["state"],
                    "lat": row["lat"],
                    "lng": row["lng"]
                })
            upload_restaurants(get_conn)


def upload_restaurants(get_conn):
    conn = get_conn()
    cur = conn.cursor()
    for restaurant in restaurants_list:
        cur.execute('INSERT INTO restaurants (id, rating, name, site, email, phone, street, city, state, lat, lng) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *',
                    (restaurant["id"], restaurant["rating"], restaurant["name"], restaurant["site"], restaurant["email"], restaurant["phone"], restaurant["street"], restaurant["city"], restaurant["state"], restaurant["lat"], restaurant["lng"]))
    conn.commit()

    cur.close()
    conn.close()
