# Daily Wellcome Art

An API to deliver random art from the Wellcome Collection. It pulls data from the collection api (`http://api.wellcomecollection.org/`) and exposes via an endpoint to get a random work, and an endpoint to post to a custom slack hook.

A heroku deployment can be found in the following link:

https://wc-random-art-api.herokuapp.com/random-art


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


Interactive Swagger UI documentation is served on [http://localhost:8000/docs](). For a summary, with some of the parameters, see table below:


| Endpoint   |  Parameters | Return |
|---|---|--------|
| /random-art   | width: `integer` (default=300. An optional integer for the image size) | A html template with a random art work and description. |
| /random-art/json   | width: `integer` (default=300. An optional integer for the image size) | A json with artwork information |
| /random-art/slack | channel_id: `integer` (Id of the channel to post), token: `str` Slack Bearer token  |  POSTs a link to a slack hook |

## Slack integration

To integrate with your slack channel:

1. [Create a slack app](https://api.slack.com/slack-apps#creating_apps).
2. [Get the token from your slack app](https://api.slack.com/slack-apps#installing_apps).
3. [Find the ID of the channel you want to post to](https://api.slack.com/methods/channels.list)
4. Send a `POST` to `/random-art/slack` with a channel_id and the token.

## Alternatives to `cron`

In addition, if you don't have a server or don't want to run it on docker, you might want to check `main/slack_plugin.py` for scheduling daily messages for the future via a Slack BOT. It is restricted to 4 months of message.
