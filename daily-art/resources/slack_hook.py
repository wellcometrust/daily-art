from pydantic import BaseModel


class SlackHook(BaseModel):
    link: str
    token: str = None
    channel_id: str = None

    @classmethod
    def convert_to_work_slack_post(cls, work):
        """ Given a daily-art work JSON, converts to a slack JSON """

        if len(work['contributors']) > 0:
            try:
                contributors = "\n\n*Contributors*\n{}".format(
                    work['contributors'][0]['agent']['label']
                )
            except KeyError:
                contributors = ""

        slack_json = {
            "attachments": [
                {
                    "fallback": "Image not found",
                    "color": "#36a64f",
                    "pretext": "*Here is your daily Wellcome art*",
                    "title": work['title'],
                    "title_link": work['collection_url'],
                    "text": "{}{}".format(work['description'], contributors),
                    "image_url": work['full_image_uri'],
                    "footer": "Daily-Wellcome-Art API",
                    "footer_icon": "https://upload.wikimedia.org/wikipedia/"
                                   "commons/thumb/5/58/"
                                   "Wellcome_Trust_logo.svg/"
                                   "1024px-Wellcome_Trust_logo.svg.png"
                }
            ]
        }

        return slack_json
