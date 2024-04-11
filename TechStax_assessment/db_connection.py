from flask_pymongo import pymongo
from datetime import datetime
from bson.objectid import ObjectId
from datetime import datetime

client=pymongo.MongoClient("mongodb://localhost:27017/")
db=client["github"]
collection=db["events"]

def store_event(eventdetails):
  collection.insert_one(eventdetails)
