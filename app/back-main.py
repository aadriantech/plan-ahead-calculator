# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask
from routes import init_routes

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

# Initialize routes
init_routes(app)

port_number = 5000

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=port_number)