from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from pandas import DataFrame
from os import path
import pandas as pd

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_google_cloud_storage(data, data_2, data_3, **kwargs) -> None:
    """
    Template for exporting data to a Google Cloud Storage bucket.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#googlecloudstorage
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'
    gcs = GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile))

    bucket_name = 'easy_tour_bucket'

    data_dict = {
        'tourguidetrips': data,
        'tourguidetrip_places': data_3,
        'tourguidetrip_days': data_2
    }

    for key, value in data_dict.items():

        object_key = f'{key}.parquet'

        gcs.export(
            pd.DataFrame.from_dict(value),
            bucket_name,
            object_key,
        )
