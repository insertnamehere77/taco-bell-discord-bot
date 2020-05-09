import time, asyncio, json, ssl, re, os, configparser
import requests, websockets


class BaseDiscordBot():

	_URL = 'https://discordapp.com/api/'

	"""docstring for DiscordBot"""
	def __init__(self, id, token):
		self.user_id = id
		self.token = token

		self.socket = None
		self._heartbeat_task = None



	def __del__(self):
		if self.socket:
			self.socket.close()

		if self._heartbeat_task:
			self._heartbeat_task.cancel()



	# POST a message for the users to see
	def send_msg(self, channel_id, msg, tts = False):
		payload = {
		  "content": msg,
		  "tts" : tts
		}

		headers = self._headers()
		msg_url = f'{self._URL}channels/{channel_id}/messages'
		response = requests.post(msg_url, data = payload, headers = headers)

		return response.json()


	# PUT a reaction on the specified message
	def add_reaction(self, channel_id, msg_id, reaction):
		headers = self._headers()
		reaction_url = f'{self._URL}channels/{channel_id}/messages/{msg_id}/reactions/{reaction}/@me'
		response = requests.put(reaction_url, headers = headers)


	# Connects to the socket and acts on events
	async def listen(self):

		await self._connect()
		
		self._heartbeat_task = asyncio.create_task(self._heartbeat())

		while True:
			event_str = await self.socket.recv()
			event = json.loads(event_str)

			if event['t'] == 'MESSAGE_CREATE':
				self._msg_created(event['d'])


			if event['op'] == 9:
				await self._identify()



	# Connects to the websocket and identifies itself
	async def _connect(self):
		gateway = self._get_gateway()
		url = gateway['url']

		# Not secure, but for a silly memebot it's probably not important
		ssl_context = ssl.SSLContext()
		ssl_context.check_hostname = False
		ssl_context.verify_mode = ssl.CERT_NONE

		self.socket = await websockets.connect(url + '?v=6&encoding=json', ssl = ssl_context)
		await self._identify()


	# Function to send the websocket a heartbeat every 30 seconds
	# Should be ran as an async task
	async def _heartbeat(self):
		
		while True:
			heartbeat = self._wrap_payload(2, 251)
			self.socket.send(heartbeat)
			await asyncio.sleep(30)



	# Creates the header for any HTTP calls
	def _headers(self):
		headers = {
			"Authorization" : 'Bot ' + self.token
		}
		return headers


	# Sends the socket our identity payload so it knows who TF we are
	async def _identify(self):
		payload = {
			"token": self.token,
			"properties": {
				"$os": "linux",
				"$browser": "my_library",
				"$device": "my_library"
			}
		}

		msg = self._wrap_payload(2, payload)
		await self.socket.send(msg)


	# Wraps a payload to send to our websocket
	def _wrap_payload(self, opcode, payload):
		msg = {
		  "op": opcode,
		  "d": payload
		}

		return json.dumps(msg)




	# GET the gateway URL so we can connect
	def _get_gateway(self):
		headers = self._headers()

		response = requests.get('https://discordapp.com/api/gateway/bot', headers = headers)
		return response.json()


	# Scans the mentions to see if our bot got called
	def _mentioned(self, mentions):
		for user in mentions:
			if user['id'] == self.user_id:
				return True

		return False


	# Removes mentions from the given msg
	def _strip_mention(self, msg):
		content = re.sub(r'<@![0-9]*>', '', msg).strip()
		return content


	# Formats a mention
	def _format_mention(self, id):
		mention = f'<@{id}>'
		return mention


	# The function that handles a MESSAGE_CREATED event
	def _msg_created(self, payload):
		pass

		

# Creates a bot using the given cfg file and Bot Class
def create_bot_from_cfg(cfg_path, BotClass):

	if 'discord_token' in os.environ:
		token = os.environ['discord_token']
		user_id = os.environ['discord_user_id']
		
	else:
		config = configparser.ConfigParser()
		config.read(cfg_path)
		
		token = config['discord']['token']
		user_id = config['discord']['user_id']

	bot = BotClass(user_id, token)

	return bot








