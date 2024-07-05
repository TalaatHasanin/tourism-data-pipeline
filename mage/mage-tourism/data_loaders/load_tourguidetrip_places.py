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

    collection = db['tripdays']

    # Fetch all documents
    documents = collection.find()  # No filters applied to get all documents

    data = []


    # Iterate through documents
    for document in documents:
        places = document["dayPlaces"]
        day_id = document["_id"]  # Get the _id of the custom document
        for place in places:
            data.append({
                '_id': place.get('_id'),
                'place_name': place.get('placeName'),
                'place_type': place.get('placeType'),
                'latitude': place.get('latitude'),
                'longitude': place.get('longitude'),
                'activity': place.get('activity'),
                'day_id': day_id
            })

    df = pd.DataFrame(data)
    
    return df

    