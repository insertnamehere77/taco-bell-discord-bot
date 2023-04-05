import configparser, random, sys
import discord
import msg_util, taco_scraper


def main(cfg_path: str):
    client = discord.Client(intents=discord.Intents.default())
    scrapper = taco_scraper.TacoBellScraper()
    reactions = ["🌶️", "🫓", "🌯", "🌮", "🥑", "🍅", "🧀"]

    @client.event
    async def on_message(message: discord.Message):
        if client.user in message.mentions:
            search_term = msg_util.strip_mentions(message.content)
            results = scrapper.search_menu(search_term)
            await message.reply(msg_util.format_reply(results))
            await message.add_reaction(random.choice(reactions))

    config = configparser.ConfigParser()
    config.read(cfg_path)
    token = config["discord"]["token"]

    client.run(token)


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        main(sys.argv[1])
    else:
        print("USAGE: python main.py <PATH_TO_CFG_FILE>")
