# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic inline bot example. Applies different text transformations.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging, random, os, re, json
from uuid import uuid4

from telegram import (
    InlineQueryResultAudio,
    ParseMode,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    Updater,
    InlineQueryHandler,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    Filters,
)

from telegram.utils.helpers import escape_markdown
from telegram.error import TelegramError, BadRequest

from pyrogram import Client

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

decr8 = -1001280481543
p = re.compile("[a-z]+", re.IGNORECASE)

with open("/home/ayuko/decr8/res/decr8_data.json", "r", encoding="utf-8") as f:
    d = json.load(f)
    
def update_json():
    with Client("decr8_linux") as app:
        d = {
            msg.audio.file_name: msg.message_id
            for msg in (app.iter_history(decr8))
            if msg.audio
            if not None
        }

    with open("/home/ayuko/decr8/res/decr8_data.json", "w", encoding="utf-8") as f:
        json.dump(d, f)
        
def start(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Test Your Luck", callback_data="1"),
            InlineKeyboardButton("Clear Playlist", callback_data="2"),
        ],
        [InlineKeyboardButton("Create Playlist", callback_data="3")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "Hi.\nType2Search & Use /help If You're Stuck :(", reply_markup=reply_markup
    )


def _next(update, context):
    """Send a message when the command /next is issued."""
    try:
        update.message.reply_audio(
            "https://t.me/crateofnotsodasbutmusic/{}".format(
                random.choice(list(d.values()))
            )
        )
        print(random.choice(list(d.values())))
    except (BadRequest) as e:
        print(e)


def button(update, context):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text="Selected option: {}".format(query.data))


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("/next Add to playlist.")


def search(update, context):
    """Search the user's message."""
    result = [
        v
        for k, v in d.items()
        if re.search(update.message.text, k, re.IGNORECASE)
    ]
    for i in result:
        update.message.reply_audio("https://t.me/crateofnotsodasbutmusic/{}".format(i))

def inlinequery(update, context):
    """Handle the inline query."""
    query = update.inline_query.query
    for k, v in d.items():
        if k.startswith(query):
            results = [
                InlineQueryResultAudio(
                    id=uuid4(),
                    audio_url="https://t.me/crateofnotsodasbutmusic/{}".format(v),
                    title="{}".format(k),
                ),
                InlineQueryResultAudio(
                    id=uuid4(),
                    audio_url="https://t.me/crateofnotsodasbutmusic/{}".format(v),
                    title="{}".format(k),
                ),
            ]

    update.inline_query.answer(results)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(
        "1266125805:AAFnUPiqc0LiHPWJNlOp2XhfSGsqtu_cEbA", use_context=True
    )

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("next", _next))
    dp.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(InlineQueryHandler(inlinequery))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, search))
    dp.add_handler(CallbackQueryHandler(button))

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
    
