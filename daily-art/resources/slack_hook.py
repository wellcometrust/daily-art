from pydantic import BaseModel


class SlackHook(BaseModel):
    link: str = "https://slack.com/api/chat.postMessage"
    token: str = None
    channel_id: str = None
    post_at: str = None

    @classmethod
    def convert_to_work_slack_post(cls, work):
        """ Given a daily-art work JSON, converts to a slack JSON """

        if len(work['contributors']) > 0:
            try:
                contributors = "*Contributors:* {}".format(
                    work['contributors'][0]['agent']['label']
                )
            except KeyError:
                contributors = ""

        slack_json_blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"_Here is your daily Wellcome art:_\n<{work['collection_url']}|*{work['title']}*>"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": work['description'],
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": contributors
                    }
                ]
            },
            {
                "type": "image",
                "title": {
                    "type": "plain_text",
                    "text": work['title'],
                },
                "image_url": work['full_image_uri'],
                "alt_text": "image1"
            }
        ]

        slack_json_similar_divider_and_title = [
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Visually similar artworks:*"
                }
            }
        ]

        slack_json_similar_blocks = [{
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"<{similar_work['collection_url']}|*{similar_work['title']}*>"
            },
            "accessory": {
                "type": "image",
                "image_url": similar_work['full_image_uri'],
                "alt_text": similar_work['title']
            }
        } for similar_work in work['similar_works']]

        all_blocks = slack_json_blocks + slack_json_similar_divider_and_title + slack_json_similar_blocks

        slack_json = {
            "blocks": all_blocks if slack_json_similar_blocks else slack_json_blocks
        }

        return slack_json
