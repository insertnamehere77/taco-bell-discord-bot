import re
import taco_scraper


def strip_mentions(content: str):
    content = re.sub(r"<@[0-9]+>", "", content).strip()
    return content


def format_reply(items: list[taco_scraper.MenuItem]) -> str:
    if len(items) == 0:
        return "Got nothing :/"

    reply = "Here's what I found:"
    for item in items:
        reply += f"\n{item}"

    return reply
