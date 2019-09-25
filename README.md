# Daily Wellcome Art

An API to deliver daily art from the Wellcome Collection. It pulls data from the collection api (`http://api.wellcomecollection.org/`) and exposes via an endpoint to get a random work, and an endpoint to post to a custom slack hook.

### Quickstart
To run standalone:

```
make
uvicorn daily-art.main:app # --reload for development mode
```

To run via docker-compose and publish the message periodically via a slack incoming hook (if you don't mind about posting to slack, just ignore the first line):
```
export $SLACK_HOOK=<address_to_slack_incoming_hook>
docker-compose up
```


Interactive Swagger UI documentation is served on [http://localhost:8000/docs](). For a summary, see table below:


| Endpoint   |  Parameters | Return |
|---|---|--------|
| /random-art   | width: `integer` (default=300. An optional integer for the image size) | A html template with a random art work and description. |
| /random-art/json   | width: `integer` (default=300. An optional integer for the image size) | A json with artwork information |
