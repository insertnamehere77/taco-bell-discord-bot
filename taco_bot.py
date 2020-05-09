import discord_bot, taco_scraper

import random


class TacoBellBot(discord_bot.BaseDiscordBot):

	_REACTIONS = ['🥙', '🌶️', '🇲🇽', '🌯', '🌮', '🥑', '🍅']

	def __init__(self, id, token):
		super(TacoBellBot, self).__init__(id, token)

		self._scraper = taco_scraper.TacoBellScraper()

	# Formats the menu into a readable string
	def _format_menu(self, menu):
		result = ''
		for name, details in menu.items():
			result += name + '\n'
			result += '\t' + details['price'] + '\t' + details['calories'] + '\n'


		return result


	# Creates the response for the user
	def _create_response(self, content, author_id):
			search_term = self._strip_mention(content)
			menu = self._scraper.search_menu(search_term)

			response = self._format_mention(author_id) + '\n'
			if menu:
				response += 'Results for ' + search_term + ':\n'
				response += self._format_menu(menu)
			else:
				response += 'Sorry, no results for ' + search_term

			return response


	# Handles a message created event
	def _msg_created(self, payload):

		mentions = payload['mentions']
		
		if self._mentioned(mentions):

			# Send back the menu results
			channel_id = payload['channel_id']
			msg_content = payload['content']
			author_id = payload['author']['id']

			response = self._create_response(msg_content, author_id)
			self.send_msg(channel_id, response)

			# Add a reaction to the request
			msg_id = payload['id']

			reaction = random.choice(self._REACTIONS)
			self.add_reaction(channel_id, msg_id, reaction)



def create_bot_from_cfg(cfg_path):
	return discord_bot.create_bot_from_cfg(cfg_path, TacoBellBot)


