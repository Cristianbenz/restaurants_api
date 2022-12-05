# restaurants_api
API made with python, postgreSQL and the extension postGIS in wich you can get information about restaurants that already exist in the database, add a new restaurant to the database, modify them and get statistic information about restaurants in a especific zone.

## SETUP
Step 1: clone this repository.

Step 2: create venv.

Step 3: run pip install -r requirements.txt

## ROUTES

### GET /api/restaurants
Brings a list of all existing restaurants.

### POST /api/restaurant
Create a new restaurant with the following schema

{
    "id": "string",
    "rating": "integer(0 <= x <= 4)",
    "name": "string",
    "site": "string",
    "email": "string",
    "phone": "string",
    "street": "string",
    "city": "string",
    "state": "string",
    "lat": "float",
    "lng": "float"
}


### PUT /api/restaurant/<restaurant_id>
Searches and updates the restaurant that has the given id through params.

### PATCH /api/restaurant/<restaurant_id>
Searches and partially updates the restaurant that has the given id through params.

### GET /api/restaurants//statistics?latitude=x&longitude=y&radius=z
It provides information on the count, average rating and standard deviation of the rating of the restaurants located in the given area.

## Dependencies
- Flask.
- Psycopg2.
- Python enviroment.

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/23086126-2b00b225-2fe5-40d0-92b4-a4dd09870438?action=collection%2Ffork&collection-url=entityId%3D23086126-2b00b225-2fe5-40d0-92b4-a4dd09870438%26entityType%3Dcollection%26workspaceId%3D1d9080cd-207d-4792-a278-e966b4a13ef4)
