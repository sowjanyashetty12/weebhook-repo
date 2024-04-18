from flask_pymongo import pymongo

import logging

# Initialize the logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# client = pymongo.MongoClient('172.28.192.1', 27017)
# client = pymongo.MongoClient(('mongodb://localhost:27017'))
client = pymongo.MongoClient('mongodb://mongo:27017')
db = client["github"]
collection = db["events"]


def store_event(eventdetails):
    try:
        # Insert the event details into the collection
        collection.insert_one(eventdetails)
        logger.info("Event stored successfully")
    except Exception as e:
        # Log any exceptions that occur during the insertion process
        logger.error(f"Error storing event: {e}")
