if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, data_2, *args, **kwargs):
    aitrip_places = data
    aitrips = data_2

    aitrips.columns = aitrips.columns.str.lower()
    aitrip_places.columns = aitrip_places.columns.str.lower()
    
    aitrip_places['_id'] = aitrip_places['_id'].astype('str')
    aitrip_places['aitrip_id'] = aitrip_places['aitrip_id'].astype('str')
    aitrip_places['day_id'] = aitrip_places['day_id'].astype('int')
    aitrip_places['activity'] = aitrip_places['activity'].astype('str')
    aitrip_places['category'] = aitrip_places['category'].astype('str')

    aitrips['_id'] = aitrips['_id'].astype('str')
    aitrips['tourist_id'] = aitrips['tourist_id'].astype('str')
    aitrips['status'] = aitrips['status'].astype('str')
    aitrips['title'] = aitrips['title'].astype('str')
    aitrips['from'] = aitrips['from'].astype('str')
    aitrips['to'] = aitrips['to'].astype('str')

    return {
        'aitrips': aitrips,
        'aitrip_places': aitrip_places
    }