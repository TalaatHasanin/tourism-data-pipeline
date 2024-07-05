create storage integration easy_tour_bucket
    type = external_stage
    storage_provider = gcs
    enabled = true
    storage_allowed_locations = ( 'gcs://easy_tour_bucket')