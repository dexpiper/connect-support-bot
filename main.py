import logging
import re

import telebot

import views
from settings import TOKEN, SUPPORT_CHAT_ID

botlogger = logging.getLogger('botlogger')

# Setting bot
bot = telebot.TeleBot(TOKEN)
tblogger = telebot.logger
telebot.logger.setLevel(logging.INFO)


def run_long_polling():
    """
    Start the bot in long-polling mode
    """
    botlogger.info('Starting polling...')
    bot.infinity_polling(skip_pending=True)


#
# MESSAGE HANDLERS
#
@bot.message_handler(commands=['start', 'help'])
def answer_start(message):
    """
    Bot sends general help page and basic bot info
    """
    bot.send_message(
        message.from_user.id,
        views.hello(message.from_user.username),
        parse_mode='HTML',
    )
    send_to_support(views.user_connected(message))


@bot.message_handler(chat_types='private', content_types=['text'])
def redirect_message_to_admins(message):
    """
    Bot redirects user request to admin group.
    WARNING: At the end of the redirected message bot
             will add <user_id> of the user who sent
             the message. This is to ensure that chain of
             redirection will not brake.
    """
    send_to_support(
        views.redirect_user_message(message, add_id=True))


@bot.message_handler(chat_types='private', content_types=['photo'])
def redirect_photo_to_admins(message):
    """
    Bot redirects user request to admin group with a photo
    and a caption.
    """
    ps = max(message.photo, key=lambda p: p.file_size or 0)
    caption = views.redirect_user_message(message, add_id=True, if_data=True)
    send_photo_to_support(caption, ps.file_id)


@bot.message_handler(chat_types='private', content_types=['document'])
def redirect_file_to_admins(message):
    """
    Bot redirects user request to admin group with a file
    and a caption.
    """
    caption = views.redirect_user_message(message, add_id=True, if_data=True)
    send_file_to_support(caption, message.document)


@bot.message_handler(chat_types='group')
def reply_back_to_user(message):
    """
    Bot redirects admin answers to the user. When replying,
    bot will parse <user_id> from original message that was
    added to it.
    """
    if (
            message.reply_to_message is not None
            and message.reply_to_message.from_user.is_bot
    ):
        user_id = parse_user_id(
            message.reply_to_message.text or message.reply_to_message.caption
        )
        bot.send_message(
            user_id,
            message.text,
        )


#
# HELPERS
#
def reply(to_message: object, with_message: str):
    """
    Reply to given incoming message with outcoming message
    (with Telegram reply wrapper).
    * to_message: the original message object
          came to bot from user
    * with_message: answer the bot should send to
          the author of incoming_message
    """
    bot.reply_to(
        to_message,
        with_message,
        parse_mode='HTML'
    )


def send_photo_to_support(caption: str, file_id: str):
    bot.send_photo(
        SUPPORT_CHAT_ID,
        file_id,
        caption=caption,
        parse_mode='HTML'
    )


def send_file_to_support(caption: str, document: object):
    bot.send_document(
        SUPPORT_CHAT_ID,
        document.file_id,
        caption=caption,
        parse_mode='HTML',
        thumbnail=document.thumbnail,
    )


def send_to_support(outcoming_message: str):
    """
    Send message (without Telegram reply wrapper).
    * outcoming_message: answer the bot should send to
          the author of incoming_message
    """
    bot.send_message(
        SUPPORT_CHAT_ID,
        outcoming_message,
        parse_mode='HTML'
    )


def parse_user_id(message: str):
    """
    Parse message text and find user id.
    """
    mtch: re.Match = re.match(r'.*id=(?P<id>\d+).*', message, re.S)
    if mtch:
        return mtch.group('id')


if __name__ == '__main__':
    run_long_polling()
