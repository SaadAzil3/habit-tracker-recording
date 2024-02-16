import os
from flask import Flask
from routes import pages
from pymongo import MongoClient
from dotenv import load_dotenv
from functools import partial

load_dotenv()

def create_app(environ, start_response):
    app = Flask(__name__)
    client = MongoClient(os.environ.get("MONGODB_URI"))
    app.db = client.get_default_database()

    app.register_blueprint(pages)
    
    # You can add additional setup code here if needed
    
    return app(environ, start_response)

# If you're running this using Gunicorn, you can create a partial application
application = partial(create_app)
