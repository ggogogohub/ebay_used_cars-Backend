# Description: This file is the entry point of the application. It creates the Flask app and registers the blueprints.
from flask import Flask
from pymongo import MongoClient
from blueprints.reviews.reviews import reviews_bp
from blueprints.auth.auth import auth_bp
from blueprints.listings.listings import listings_bp
from blueprints.admin.admin import admin_bp

# Create the Flask app
app = Flask(__name__)

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["ebay_used_cars"]

# Register Blueprints
app.register_blueprint(reviews_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(listings_bp)
app.register_blueprint(admin_bp)

# Run the application
if __name__ == '__main__':
    app.run(debug=True, port=5001)
