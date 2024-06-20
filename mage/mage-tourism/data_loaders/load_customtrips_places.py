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
    all_customtrip_ids = [] 
    all_days_ids = []
    all_places_ids = []
    place_names = []
    latitudes = []
    longitudes = []
    categories = []
    governments = []
    activities = []
    images = []
    prices = []


    # Iterate through documents
    for document in documents:
        trip_details = document["tripDetails"]
        customtrip_id = document["_id"] 
        for details in trip_details:
            day_id = details['_id']
            places = details['dayPlaces']
            for place in places:
                place_names.append(place.get('placeName'))
                latitudes.append(place.get('latitude'))
                longitudes.append(place.get('longitude'))
                categories.append(place.get('category'))
                governments.append(place.get('government'))
                activities.append(place.get('activity'))
                images.append(place.get('image'))
                prices.append(place.get('priceRange'))
                all_days_ids.append(day_id)
                all_customtrip_ids.append(customtrip_id)
                all_places_ids.append(place.get('_id'))
    # print(len(all_places_ids))
    # print(len(place_names))
    # print(len(all_customtrip_ids))
    # print(len(all_days_ids))
    # print(len(latitudes))
    # print(len(longitudes))
    # print(len(categories))
    # print(len(governments))
    # print(len(activities))
    # print(len(images))
    # print(len(prices))
    # Create a Pandas DataFrame
    data = {
        '_id': all_places_ids,
        'place_name': place_names,
        'latitude': latitudes,
        'longitude': longitudes,
        'category': categories,
        'government': governments,
        'activity': activities,
        'image': images,
        'price_range': prices,
        'day_id': all_days_ids,
        'customtrip_id': all_customtrip_ids,
    }
    df = pd.DataFrame(data)
    # print(df.dtypes)
    
    return df
