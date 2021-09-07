import itertools
import re

from requests_html import HTMLSession, AsyncHTMLSession

from photo_radar import models, utils

COUNTRY = "CA"
PROVIENCE = "BC"
PROVIENCE_HUMANIZED = "British Columbia"
BC_URL = "https://www2.gov.bc.ca/gov/content/transportation/driving-and-cycling/roadsafetybc/intersection-safety-cameras/where-the-cameras-are"

asession = AsyncHTMLSession()


def parse_location_per_city(city):
    location_list = city["result"].html.find("tbody tr")

    locations = []
    for row in location_list:
        colums = row.find("td")
        google_map_url = row.find("a", first=True).attrs["href"]
        matches = re.search(r"@(.*)\/", google_map_url)
        location = {
            "street": colums[0].text,
            "city": city["city"],
            "is_red_light_enabled": True if colums[1].text == "✓" else False,
            "is_speed_enabled": True if colums[2].text == "✓" else False,
            "lat": None,
            "lon": None,
        }
        if matches:
            [lat, lng, _] = matches[1].split(",")
            location["lat"] = float(lat)
            location["lon"] = float(lng)
        locations.append(location)
    return locations


async def _async_fetch_locations_per_city(url, city):
    r = await asession.get(url)
    return parse_location_per_city({"result": r, "city": city})


def _patch_camera_location_metadata(camera):
    camera["country"] = COUNTRY
    camera["provience"] = PROVIENCE
    return camera


def run():
    session = HTMLSession()
    response = session.get(BC_URL)

    cameras_nav_list = response.html.find("li.open.current ul li a")
    cameras_by_city_list = [
        {"city": each.text, "url": f'https://www2.gov.bc.ca{each.attrs["href"]}'}
        for each in cameras_nav_list
    ]
    # extract list of cameras from each city camera page
    results = asession.run(
        *[
            lambda url=each["url"], city=each["city"]: _async_fetch_locations_per_city(
                url, city
            )
            for each in cameras_by_city_list
        ]
    )
    # flatten per city nested list into a flat list
    results = list(itertools.chain.from_iterable(results))
    results = list(map(_patch_camera_location_metadata, results))

    # persist to database
    models.Camera.insert_many(results).on_conflict(
        preserve=[models.Camera.is_red_light_enabled, models.Camera.is_speed_enabled],
        conflict_target=[
            models.Camera.street,
            models.Camera.city,
            models.Camera.provience,
            models.Camera.country,
        ],
    ).execute()

    # geocode intersection address to coordinate, the encoded coordinates from ICBC-provided google map url is not accurate
    cameras = models.Camera.select()
    for each in cameras:
        result = utils.get_coordinate_by_address(each.street)
        coord = result["results"][0]["geometry"]["location"]
        each.lon = coord["lng"]
        each.lat = coord["lat"]
        each.save()


if __name__ == "__main__":
    models.create_tables()
    run()
