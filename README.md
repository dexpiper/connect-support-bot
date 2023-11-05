# Support contact bot
This Telegram bot helps to send messages from customers and users to a private group where admins can answer them.

## How does it work
* your customer text the bot
* bot sends this message from the customer to Telegram chat with admins or support staff
* any member of this chat can reply to the message
* bot will send this message to the customer, not showing your identity

## How to start

Clone the repository with:
```
$ git clone <repo_URL> && cd connect-support-bot
```

You should define these environment variables before using the bot:

```
TOKEN="your bot token from the BotFather, str"
SUPPORT_CHAT_ID="Telegram chat_id where messages will be resent or your own user_id, int"
```

It's better to do that in .env file. The file will be taken by docker-compose automatically.

#### Start by docker-compose
``` bash
$ docker-compose up --build
```

#### Direct start
To start the bot without docker-compose, you may use:
``` bash
$ python3 main.py
```


## Change messages

You may customize any bot message, especially the greeting message bot answers to /start command.

Templates are stored in `./templates`. The templates use [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/) syntax. You can add emoji defined in `./common/unicode.py` or define your own.

## Technologies and libraries

Project is created with:
* [pyTelegramBotAPI 3.7.3](https://github.com/eternnoir/pyTelegramBotAPI)
* Jinja2

## Acknowledgements

This bot was inspired by the [Livegram Bot](https://telegra.ph/What-is-Livegram-Bot-03-17).
Other implementation with Heroku: [telegram-support-bot](https://github.com/ohld/telegram-support-bot/tree/main)