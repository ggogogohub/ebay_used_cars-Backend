# Description: Global variables and constants
from pymongo import MongoClient

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017")
db = client.ebay_used_cars

# Secret Key
SECRET_KEY = 'mysecret'

