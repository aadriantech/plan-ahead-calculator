# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask
from dotenv import load_dotenv
from routes import init_routes
import os

# Load environment variables from .env file
load_dotenv()

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

# Set configuration variables from environment variables
app.config['APPLICATION_PATH'] = os.getenv('APPLICATION_PATH', '/var/www/')

# Initialize routes
init_routes(app)

if __name__ == "__main__":
    app.run(debug=True)