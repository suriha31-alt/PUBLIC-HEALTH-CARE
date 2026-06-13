from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["healthcare_db"]
collection = db["hospital_data"]