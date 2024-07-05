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
import datetime

def json_serializable(obj):
    """ Convert non-serializable objects to serializable format """
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, datetime.datetime):
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

    documents = collection.find() 

    data = []

    # Iterate through documents
    for document in documents:
        trip_details = document["tripDetails"]
        aitrip_id = document["_id"]
        for day_key, day_details in trip_details.items():
            if day_key.startswith("Day"):
                day_number = day_key.replace("Day", "")
                for detail in day_details:
                    data.append({
                        '_id': detail.get('_id'),
                        'place_name': detail.get('placeName'),
                        'longitude': detail.get('longitude'),
                        'latitude': detail.get('latitude'),
                        'activity': detail.get('activity'),
                        'category': detail.get('category'),
                        'day_number': day_number,
                        'aitrip_id': aitrip_id
                    })

    # Create a Pandas DataFrame
    df = pd.DataFrame(data)

    df.columns = df.columns.str.lower()
    
    return df
