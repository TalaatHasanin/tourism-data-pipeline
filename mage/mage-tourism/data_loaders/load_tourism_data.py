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


@data_loader
def load_from_mongodb(*args, **kwargs):
    # config_path = path.join(get_repo_path(), 'io_config.yaml')
    # config_profile = 'default'

    # query = {}

    # return MongoDB.with_config(ConfigFileLoader(config_path, config_profile)).load(
    #     query=query,
    #     collection='collection_name',
    # )
    connection_string = get_secret_value('mongo_uri')
    client = pymongo.MongoClient(connection_string)
 
    # Database Name
    db = client["gradProject"]

    # Collection Name
    col = db["aitrips"]

    x = col.find_one()

    print(x)



# @test
# def test_output(output, *args) -> None:
#     """
#     Template code for testing the output of the block.
#     """
#     assert output is not None, 'The output is undefined'
