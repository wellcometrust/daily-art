# Daily Wellcome Art

An API to deliver a daily dosis of art from the Wellcome Collection.

### Quickstart
Easiest way to start the api and the daily cron-'type' job is via:
```
docker-compose up
```

Documentation is served on [localhost:8000/docs]. For a summary, see table below:


| Endpoint   |  Parameters | Return |
|---|---|--------|
| /random_image   | width: `integer` (default=300. An optional integer for the image size) | A html template with a random art work and description. |
| /random_image/json   | width: `integer` (default=300. An optional integer for the image size) | A json with artwork information |

Some script to download and clean the data are available in the subfolder `/data`
