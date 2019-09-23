# Daily Wellcome Art

An API to deliver daily art from the Wellcome Collection.

### Quickstart
To run standalone:

```
virtualenv -p python3 env/
. env/bin/activate
pip install -r requirements.txt
uvicorn daily-art.main:app # --reload for development mode
```

To run via docker:
```
docker build -t wt-da ./
docker run -p 8000:8000 wt-da
```

Interactive Swagger UI documentation is served on [http://localhost:8000/docs](). For a summary, see table below:


| Endpoint   |  Parameters | Return |
|---|---|--------|
| /random_image   | width: `integer` (default=300. An optional integer for the image size) | A html template with a random art work and description. |
| /random_image/json   | width: `integer` (default=300. An optional integer for the image size) | A json with artwork information |

Some script to download and clean the data are available in the subfolder `/data`
