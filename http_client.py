import requests


class DiscordHttpClient:
    _URL: str = "https://discordapp.com/api"

    _token: str

    def __init__(self, token: str) -> None:
        self._token = token

    def post_message(self, channel_id, msg, tts=False):
        payload = {"content": msg, "tts": tts}

        headers = self._create_headers()
        msg_url = f"{self._URL}/channels/{channel_id}/messages"
        response = requests.post(msg_url, data=payload, headers=headers)

        return response.json()

    def put_reaction(self, channel_id, msg_id, reaction):
        headers = self._create_headers()
        reaction_url = f"{self._URL}/channels/{channel_id}/messages/{msg_id}/reactions/{reaction}/@me"
        response = requests.put(reaction_url, headers=headers)

    def get_gateway(self):
        headers = self._create_headers()

        response = requests.get(f"{self._URL}/gateway/bot", headers=headers)
        return response.json()

    def _create_headers(self):
        headers = {"Authorization": "Bot " + self._token}
        return headers
