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
    data = list(db['tourguides'].find())
    df = pd.DataFrame(data)

    # Convert data to JSON serializable format
    serializable_data = json.loads(json.dumps(data, default=json_serializable))
    
    # Convert the cleaned data to DataFrame
    df = pd.DataFrame(serializable_data)

    df = df.drop(columns=['__v', 'password', 'customId', 'confirmed', 
    'forgetPassword', 'token', 'profilePicture', 'socketID', 'devicePushToken',
    'languages', 'ministyliscence', 'syndicateLiscence', 'createdTrips', 
    'contact_info', 'CV', 'firsNameSlug', 'lastNameSlug', 'verified'])

    df.rename(columns={'firstName': 'first_name'}, inplace=True)
    df.rename(columns={'lastName': 'last_name'}, inplace=True)
    df.rename(columns={'updatedAt': 'updated_at'}, inplace=True)
    df.rename(columns={'phoneNumber': 'phone_number'}, inplace=True)
    df.rename(columns={'createdAt': 'created_at'}, inplace=True)
    df.rename(columns={'birthDate': 'birth_date'}, inplace=True)

    return df