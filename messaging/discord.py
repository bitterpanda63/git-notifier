import json

import requests


class DiscordNotifier:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_notification(self, message):
        try:
            response = requests.post(
                self.webhook_url,
                data=json.dumps({'content': message}),
                headers={'Content-Type': 'application/json'}
            )
            if response.status_code >= 300:
                raise ValueError(
                    f"Request to Discord returned an error {response.status_code}, the response is:\n{response.text}")
        except Exception as e:
            print(f"Error sending Discord notification: {e}")
