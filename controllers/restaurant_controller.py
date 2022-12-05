from flask import request
from app import app
from models.restaurant_model import Restaurant

restaurant = Restaurant()

@app.get('/api/restaurants')
def get_restaurants_controller():
    return restaurant.get_restaurants_model()


@app.post('/api/restaurant')
def create_restaurant_controller():
    return restaurant.create_restaurants_model()


@app.put('/api/restaurant/<restaurant_id>')
def modify_restaurant_controller(restaurant_id):
    return restaurant.modify_restaurant_model(restaurant_id)

@app.patch('/api/restaurant/<restaurant_id>')
def partially_modify_restaurant_controller(restaurant_id):
    return restaurant.partially_modify_restaurant_model(restaurant_id)


@app.get('/api/restaurants/statistics')
def statistics_by_location_controller():
    return restaurant.statistics_bt_location_model(request.args)