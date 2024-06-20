from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.data_preparation.shared.secrets import get_secret_value
from mage_ai.io.mongodb import MongoDB
from os import path
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
import pandas as pd
import pymongo
import json
from bson import ObjectId
from pandas import json_normalize
import numpy as np
import datetime
import csv

def json_serializable(obj):
    """ Convert non-serializable objects to serializable format """
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, datetime.datetime):  # Properly reference datetime class
        return obj.isoformat()
    if isinstance(obj, list):
        return [json_serializable(i) for i in obj]
    if isinstance(obj, dict):
        return {k: json_serializable(v) for k, v in obj.items()}
    raise TypeError(f"Type {type(obj)} not serializable")


@data_loader
def load_from_mongodb(*args, **kwargs):
    connection_string = get_secret_value('mongo_uri')
    client = pymongo.MongoClient(connection_string)

    db = client["gradProject"]

    collection = db['aitrips']

    # Fetch all documents
    documents = collection.find()  # No filters applied to get all documents

    # Initialize lists to store data across all documents
    all_places_ids = []
    all_aitrip_ids = []  
    all_day_numbers = []
    all_longitudes = []
    all_latitudes = []
    all_activities = []
    all_categories = []

    # Iterate through documents
    for document in documents:
        trip_details = document["tripDetails"]
        aitrip_id = document["_id"]  # Get the _id of the aitrip document
        for day_key, day_details in trip_details.items():
            if day_key.startswith("Day"):
                day_number = day_key.replace("Day", "")
                for details in day_details:
                    all_aitrip_ids.append(aitrip_id) 
                    all_day_numbers.append(day_number)
                    all_places_ids.append(details.get("_id"))
                    all_longitudes.append(details.get("longitude"))
                    all_latitudes.append(details.get("latitude"))
                    all_activities.append(details.get("activity"))
                    all_categories.append(details.get("category"))

    # Create a Pandas DataFrame
    data = {
        '_id': all_places_ids,
        "aitrip_id": all_aitrip_ids,  # Include the foreign key column
        "day_id": all_day_numbers,
        "Longitude": all_longitudes,
        "Latitude": all_latitudes,
        "Activity": all_activities,
        "Category": all_categories,
    }
    df = pd.DataFrame(data)
    
    return df

    