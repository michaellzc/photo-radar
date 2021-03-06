# Photo Radar

> Please drive safely.

Photo radar location data in Canada.

## Why does this project exist?

Under the Intersection Safety Camera (ISC) program, there are nearly 200 red light or speed cameras located in British Columbia. [ICBC] and [Ministry of Transportation][] have made them publicly available via a custom Google Map, you may find them from [here](https://www.icbc.com/road-safety/community/Pages/intersection-safety-camera-program.aspx) and [here](https://www2.gov.bc.ca/gov/content/transportation/driving-and-cycling/roadsafetybc/intersection-safety-cameras/where-the-cameras-are).

However, they do not provide the data in a format that is problematically accessible with minimal effort.

The goal of this project is to maintain a source of photo radar data across Canada and make them publically available with developers-friendly formats (sqlite, csv, etc).

## Supported communities

- British Columbia, CA - [source](https://www2.gov.bc.ca/gov/content/transportation/driving-and-cycling/roadsafetybc/intersection-safety-cameras/where-the-cameras-are)

## Usage

The location data in sqlite or csv can be downloaded from the [releases page](https://github.com/michaellzc/photo-radar/releases).

## Development

### Prereq

- Python 3.x (the latest)
- Pipenv
- Google API Key with Geocoding API enabled - [learn more](https://developers.google.com/maps/documentation/geocoding/get-api-key)

### Setup

```bash
pipenv install --dev
```

### Run

Start the virtual environment

```bash
pipenv shell
```

```bash
python run.py
```

[icbc]: https://www.icbc.com/
[ministry of transportation]: https://www2.gov.bc.ca/gov/content/transportation

### Add data for a new provience

Implement a new `fetcher` module similar to [photo_radar.fetcher.canada.bc](photo_radar/fetchers/canada/bc.py). The internal doesn't really matter, and it's a one-off script anyway. We just need to make sure the camera data can be persisted using the [camera](photo_radar/models.py) model.
