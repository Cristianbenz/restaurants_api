from flask import Flask
from dotenv import load_dotenv
import markdown
load_dotenv()

app = Flask(__name__)

@app.get('/')
def index():
    with open("README.md") as readme_file:
        readme = markdown.markdown(
            readme_file.read(), extensions=["fenced_code"]
        )

    return readme

from controllers import *