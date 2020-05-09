import taco_bot

import asyncio, sys



async def main(argv):

	if (len(argv) == 2):
		cfg_path = argv[1]
	else:
		cfg_path = 'bot_config.cfg'

	bot = taco_bot.create_bot_from_cfg(cfg_path)
	await bot.listen()


if __name__ == '__main__':
	try:
		asyncio.run(main(sys.argv))
	except KeyboardInterrupt:
		print('Goodbye!')
	except Exception as e:
		print('Loop encountered a fatal error')
		raise e
	