import time, asyncio, json, ssl, random, configparser
import requests, websockets


class DiscordBot():

	_URL = 'https://discordapp.com/api/'

	"""docstring for DiscordBot"""
	def __init__(self, user, token):
		self.username = user
		self.token = token

		self.socket = None
		self._heartbeat_task = None

	def __del__(self):
		if self.socket:
			self.socket.close()

		if self._heartbeat_task:
			self._heartbeat_task.cancel()



	async def _connect(self):
		gateway = self._get_gateway()
		url = gateway['url']

		# Not secure, but for a silly memebot it's probably not important
		ssl_context = ssl.SSLContext()
		ssl_context.check_hostname = False
		ssl_context.verify_mode = ssl.CERT_NONE

		self.socket = await websockets.connect(url + '?v=6&encoding=json', ssl = ssl_context)
		await self._identify()


	async def _heartbeat(self):
		
		while True:
			heartbeat = self._wrap_payload(2, 251)
			self.socket.send(heartbeat)
			print("Sent heartbeat\n")
			await asyncio.sleep(30)




	def _create_headers(self):
		headers = {
			"Authorization" : 'Bot ' + self.token
		}
		return headers


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


	def _wrap_payload(self, opcode, payload):
			msg = {
			  "op": opcode,
			  "d": payload
			}

			return json.dumps(msg)


	def send_msg(self, room_id, msg, tts = False):
		payload = {
		  "content": msg,
		  "tts" : tts
		}

		headers = self._create_headers()
		msg_url = '{}channels/{}/messages'.format(DiscordBot._URL, room_id)
		response = requests.post(msg_url, data = payload, headers = headers)

		return response.json()


	def add_reaction(self, room_id, msg_id, reaction):
		headers = self._create_headers()
		reaction_url = '{}channels/{}/messages/{}/reactions/{}/@me'.format(DiscordBot._URL, room_id, msg_id, reaction)
		response = requests.put(reaction_url, headers = headers)


	def _get_gateway(self):
		headers = self._create_headers()

		response = requests.get('https://discordapp.com/api/gateway/bot', headers = headers)
		return response.json()


	def _mentioned(self, mentions):
		for user in mentions:
			if user['username'] == self.username:
				return True

		return False


	def _msg_created(self, payload):

		if self._mentioned(payload['mentions']):
			room_id = payload['channel_id']
			self.send_msg(room_id, 'Think outside the bun')

			msg_id = payload['id']
			reactions = ["🥙", "🌶️", "🇲🇽", "🌯", "🌮"]
			reaction = random.choice(reactions)
			print(reaction)
			self.add_reaction(room_id, msg_id, reaction)
			return





	async def listen(self):

		await self._connect()
		
		self._heartbeat_task = asyncio.create_task(self._heartbeat())

		while True:
			msg_str = await self.socket.recv()
			msg = json.loads(msg_str)
			print("NEW MSG", msg)
			print("\n")

			if msg['t'] == 'MESSAGE_CREATE':
				self._msg_created(msg['d'])
				





			if msg['op'] == 9:
				await self._identify()



		

		


async def main():

	config = configparser.ConfigParser()
	config.read('bot_config.cfg')
	
	token = config['discord']['token']
	username = config['discord']['username']
	bot = DiscordBot(username, token)

	await bot.listen()



	





if __name__ == '__main__':
	asyncio.run(main())

