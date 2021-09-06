import requests

from photo_radar import config


def get_coordinate_by_address(address):
    response = requests.get(
        config.GOOGLE_MAP_GEOCODING_API_ENDPOINT,
        params={"address": address, "key": config.GOOGLE_CLOUD_PLATFORM_API_KEY},
    )
    return response.json()
