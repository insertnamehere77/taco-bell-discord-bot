import asyncio, json, ssl, re, os, configparser
import websockets
from http_client import DiscordHttpClient


class BaseDiscordBot:

    """docstring for DiscordBot"""

    def __init__(self, id, token):
        self.user_id = id
        self.token = token

        self.socket = None
        self._heartbeat_task = None
        # Stored in seconds for the asyncio sleep() method
        self._heartbeat_interval = 30
        self._session_active = False

        self._http_client = DiscordHttpClient(token)

    def __del__(self):
        if self._session_active:
            print("You forgot to end the discord session")

    def post_message(self, channel_id, msg, tts):
        return self._http_client.post_message(channel_id, msg, tts)

    def put_reaction(self, channel_id, msg_id, reaction):
        return self._http_client.put_reaction(channel_id, msg_id, reaction)

    async def _start_heartbeat(self):
        event_str = await self.socket.recv()
        event = json.loads(event_str)

        # Hello payload that provides heartbeat_interval
        if event["op"] == 10:
            self._heartbeat_interval = event["d"]["heartbeat_interval"] / 1000
            self._heartbeat_task = asyncio.create_task(self._heartbeat())

    async def __aenter__(self):
        await self.start_session()
        return self

    async def __aexit__(self, type, value, traceback):
        await self.end_session()

    async def start_session(self):
        await self._connect()
        await self._identify()
        await self._start_heartbeat()
        self._session_active = True

    async def end_session(self):
        self._heartbeat_task.cancel()
        await self.socket.close()
        self._session_active = False

    # Connects to the socket and acts on events
    async def listen(self):
        while True:
            event_str = await self.socket.recv()
            event = json.loads(event_str)

            # Hello payload that provides heartbeat_interval
            if event["op"] == 10:
                self._heartbeat_interval = event["d"]["heartbeat_interval"] / 1000

            if event["t"] == "MESSAGE_CREATE":
                self._msg_created(event["d"])

            if event["op"] == 9:
                await self._identify()

    # Connects to the websocket and identifies itself
    async def _connect(self):
        gateway = self._http_client.get_gateway()
        url = gateway["url"]

        # Not secure, but for a silly memebot it's probably not important
        ssl_context = ssl.SSLContext()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        self.socket = await websockets.connect(
            url + "?v=6&encoding=json", ssl=ssl_context
        )

    # Function to send the websocket a heartbeat every heartbeat inverval
    # Should be ran as an async task
    async def _heartbeat(self):
        try:
            while True:
                heartbeat = self._wrap_payload(1, 251)
                await self.socket.send(heartbeat)
                await asyncio.sleep(self._heartbeat_interval)

        except asyncio.CancelledError:
            print("Heartbeat task cancelled")
        except Exception as e:
            print("Heartbeat task encountered an error")
            raise e

    # Sends the socket our identity payload so it knows who TF we are
    async def _identify(self):
        payload = {
            "token": self.token,
            "properties": {
                "$os": "linux",
                "$browser": "my_library",
                "$device": "my_library",
            },
        }

        msg = self._wrap_payload(2, payload)
        await self.socket.send(msg)

    # Wraps a payload to send to our websocket
    def _wrap_payload(self, opcode, payload):
        msg = {"op": opcode, "d": payload}

        return json.dumps(msg)

    # Scans the mentions to see if our bot got called
    def _mentioned(self, mentions):
        for user in mentions:
            if user["id"] == self.user_id:
                return True

        return False

    # Removes mentions from the given msg
    def _strip_mention(self, msg):
        content = re.sub(r"<@[0-9]+>", "", msg).strip()
        return content

    # Formats a mention
    def _format_mention(self, id):
        mention = f"<@{id}>"
        return mention

    # The function that handles a MESSAGE_CREATED event
    def _msg_created(self, payload):
        pass


# Creates a bot using the given cfg file and Bot Class
def create_bot_from_cfg(cfg_path, BotClass):
    if "discord_token" in os.environ:
        print("Reading config from env variables")
        token = os.environ["discord_token"]
        user_id = os.environ["discord_user_id"]

    else:
        print(f"Reading config from {cfg_path}")
        config = configparser.ConfigParser()
        config.read(cfg_path)

        token = config["discord"]["token"]
        user_id = config["discord"]["user_id"]

    bot = BotClass(user_id, token)

    return bot
