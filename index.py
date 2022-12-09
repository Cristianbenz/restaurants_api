from app import app
from os import environ

if __name__ == '__main__':
    app.run(port=environ.get('PORT'), debug=False)
