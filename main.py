import configparser, random, sys, asyncio
import discord
import msg_util, taco_scraper


def read_token_from_cfg(cfg_path: str) -> str:
    config = configparser.ConfigParser()
    config.read(cfg_path)
    return config["discord"]["token"]


async def main(cfg_path: str):
    try:
        client = discord.Client(intents=discord.Intents.default())
        scraper = taco_scraper.TacoBellScraper()
        reactions = ["🌶️", "🫓", "🌯", "🌮", "🥑", "🍅", "🧀"]

        @client.event
        async def on_message(message: discord.Message):
            if client.user in message.mentions:
                search_term = msg_util.strip_mentions(message.content)
                results = await scraper.search_menu(search_term)
                await message.reply(msg_util.format_reply(results))
                await message.add_reaction(random.choice(reactions))

        await client.start(read_token_from_cfg(cfg_path))
    finally:
        await client.close()
        await scraper.close()


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        try:
            asyncio.run(main(sys.argv[1]))
        except KeyboardInterrupt:
            print("Bye!")
    else:
        print("USAGE: python main.py <PATH_TO_CFG_FILE>")
