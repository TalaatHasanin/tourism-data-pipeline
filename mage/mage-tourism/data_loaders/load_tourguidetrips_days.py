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
import itertools

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

    # Fetch all documents
    tripdays = db['tripdays'].find()

    tourguidetrips = db['tourguidetrips'].find()

    # Initialize lists to store data across all documents
    all_tourguidetrips_ids = [] 
    all_days_ids = []


    for document in tourguidetrips:
        tourguidetrip_id = document['_id']
        trip_details = document['tripDetails']
        for detail in trip_details:
            all_days_ids.append(detail)
            all_tourguidetrips_ids.append(tourguidetrip_id)
        

    # Create a Pandas DataFrame
    data = {
        '_id': all_days_ids,
        'tourguidetrip_id': all_tourguidetrips_ids,
    }
    df = pd.DataFrame(data)

    df2 = pd.DataFrame(tripdays)
    df2 = df2.drop(columns=['dayPlaces', '__v'])

    # Merge the dataframes on _id
    enriched_df = pd.merge(df, df2, on='_id', how='left')
    
    return enriched_df

    