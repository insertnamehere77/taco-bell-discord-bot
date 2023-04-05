
# CheesyGorditoCrunch
Have you ever been gaming with your crew when you notice your fuel tanks are empty? Do you get salty when your snacks are running low? This is the teammate for you! The CheesyGorditoCrunch bot allows you to quickly search the Taco Bell menu from the comfort of your Discord server!


## Usage
CheesyGorditoCrunch can be used in any Discord server where it's been added. Simply type your search terms and tag the bot, and it will return your results. Some examples below:

`nachos @CheesyGorditoCrunch`

`@CheesyGorditoCrunch combos`


## How to Run 

### Setup
#### Installing dependencies

Dependencies can easily be installed with:
`$ pip install -r requirements.txt`
It's recommended you use a [virtual environment](https://docs.python.org/3/library/venv.html) for this to isolate the dependencies. 

This program works on Python 3.11+.

#### Discord Setup
In order to run and interact with Discord, the bot requires a bot token as well as a user ID. You can set this up on the [Discord developer portal](https://discordapp.com/developers/docs/intro).
Once you have the bot account created, add it to any server you wish to use it on from the portal. When adding the bot, it needs to be able to send/recieve messages, tag users, and add reactions.



### Running
Now that Discord knows who your bot it, you'll need to create a .cfg file with the token and user_id variables set. An example is provided below.

bot_config.cfg
```
[discord]
token = <YOUR_TOKEN_HERE>
```

Once this is done, you can run the bot with a simple:
`$ python main.py`

By default, the bot will search it's root directory for a cfg called "bot_config.cfg". If you'd like to use a different .cfg, you can pass it in as a command line argument as seen below.
`$ python main.py <PATH_TO_CFG>`
