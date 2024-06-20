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

    collection = db['customtrips']

    # Fetch all documents
    documents = collection.find()  # No filters applied to get all documents

    # Initialize lists to store data across all documents
    all_customtrip_ids = []  # New list to store the foreign key
    all_days_ids = []
    all_day_names = []


    # Iterate through documents
    for document in documents:
        trip_details = document["tripDetails"]
        customtrip_id = document["_id"]  # Get the _id of the custom document
        for details in trip_details:
            all_days_ids.append(details.get('_id'))
            all_day_names.append(details.get('dayName'))
            all_customtrip_ids.append(customtrip_id)

    # Create a Pandas DataFrame
    data = {
        '_id': all_days_ids,
        'day_name': all_day_names,
        'customtrip_id': all_customtrip_ids,
    }
    df = pd.DataFrame(data)
    # print(df.dtypes)
    
    return df

    