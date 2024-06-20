from mage_ai.settings.repo import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_big_query(data, data_2, data_3, **kwargs) -> None:
    """
    Template for exporting data to a BigQuery warehouse.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#bigquery
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'
    bq = BigQuery.with_config(ConfigFileLoader(config_path, config_profile))

    data_dict = {
        'customtrips': data_2,
        'customtrips_places': data_3,
        'customtrips_days': data
    }

    for key, value in data_dict.items():
        table_id = f'easytour-422214.easy_tour_dataset.{key}'
        
        bq.export(
            value,
            table_id,
            if_exists='replace'
        )