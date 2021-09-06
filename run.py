import csv

from photo_radar import models
from photo_radar.fetchers import canada


def save_as_csv():
    with open("photo_radar.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "id",
                "street",
                "city",
                "provience",
                "country",
                "lat",
                "lon",
                "is_red_light_enabled",
                "is_speed_enabled",
            ]
        )
        for camera in models.Camera.select():
            writer.writerow(
                [
                    camera.id,
                    camera.street,
                    camera.city,
                    camera.provience,
                    camera.country,
                    camera.lat,
                    camera.lon,
                    camera.is_red_light_enabled,
                    camera.is_speed_enabled,
                ]
            )


if __name__ == "__main__":
    models.create_tables()
    canada.bc.run()
    save_as_csv()
