import taco_bot

import asyncio, sys



async def main(argv):

	if (len(argv) == 2):
		cfg_path = argv[1]
	else:
		cfg_path = 'bot_config.cfg'

	print(f'Reading config from {cfg_path}')

	bot = taco_bot.create_bot_from_cfg(cfg_path)
	await bot.listen()


if __name__ == '__main__':
	asyncio.run(main(sys.argv))