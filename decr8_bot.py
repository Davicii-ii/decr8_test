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

import logging, random, os, re, json, traceback, html

from uuid import uuid4

from telegram.utils import (
    helpers
    )

from telegram import (
    Update,
    InlineQueryResultAudio,
    InlineQueryResultArticle,
    InputTextMessageContent,
    ParseMode,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputTextMessageContent,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from telegram.ext import (
    Updater,
    InlineQueryHandler,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)

from telegram.utils.helpers import escape_markdown
from telegram.error import TelegramError, BadRequest

from pyrogram import Client

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

api_id = 314504
api_hash = "8c64c308e6f0186d495ae1e92a1c228d"

logger = logging.getLogger(__name__)

decr8 = -1001280481543
me = 487795386
p = re.compile("[a-z]+", re.IGNORECASE)
dcr8_url = "https://t.me/crateofnotsodasbutmusic/"

# Define constants that will allow us to reuse the deep-linking parameters.
DECR8 = 'decr8'
USING_ENTITIES = 'using-entities-here'
SO_COOL = 'so-cool'

DEVELOPER_CHAT_ID = me
STAGE1, STAGE2, STAGE3, STAGE4 = range(4)

global text
global count
global val
global key

app = Client("decr8_g-host", api_id=api_id, api_hash=api_hash)
        
def start(update: Update, context: CallbackContext) -> None:
    """Start bot"""
    global count
    
    count = 1
    reply_keyboard = [['/start'],['/queue'],['/help']]

    """Send a deep-linked URL when the command /start is issued."""
    bot = context.bot
    
    url = helpers.create_deep_linked_url(
        bot.get_me().username,
        DECR8,
        group=True
        )
    
    text = ("👺" "{} items found".format(len(d)))
    
    update.message.reply_text(
        text,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            parse_mode=ParseMode.MARKDOWN,
            one_time_keyboard=True
        )
    )
    
    return STAGE1

def deep_linked_level_1(update: Update, context: CallbackContext) -> None:
    """Reached through the CHECK_THIS_OUT payload"""
    bot = context.bot
    try:
        result_id = [
            v
            for k, v in d.items()
        ]
        track_url = "https://t.me/crateofnotsodasbutmusic/{}".format(
            random.choice(result_id)
        )
        for i in range(1):
            update.message.reply_text(
                "::*decr8* ""[🎧]({})".format(track_url),
                parse_mode=ParseMode.MARKDOWN
            )
    except (BadRequest) as e:
        logger.warning(e)                                                      

    url = helpers.create_deep_linked_url(
        bot.get_me().username,
        SO_COOL
    )
    
    text = (
        "let's go to the private chat for more.\ni will not spam here."
    )
    
    keyboard = InlineKeyboardMarkup.from_button(
        InlineKeyboardButton(
            text='go to bot chat',
            url=url
        )
    )
    
    update.message.reply_text(
        text,
        reply_markup=keyboard
    )

def deep_linked_level_2(update: Update, context: CallbackContext) -> None:
    """Reached through the SO_COOL payload"""
    bot = context.bot
    
    url = helpers.create_deep_linked_url(
        bot.get_me().username,
        USING_ENTITIES
    )

    text = " ""[▶️ STOP BOT]({}).".format(url)
    update.message.reply_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )

def deep_linked_level_3(update: Update, context: CallbackContext) -> None:
    """Reached through the USING_ENTITIES payload"""
    payload = context.args
    update.message.reply_text(
        "/queue",
        parse_mode=ParseMode.MARKDOWN
    )

def add(update: Update, context: CallbackContext) -> None:

    global count

    reply_keyboard = [
        ["/queue"],
        ["/sub", "/add"]
    ]

    count += 1

    update.message.reply_text(
        "queue {} song(s)".format(count),
        reply_markup=ReplyKeyboardMarkup(reply_keyboard),
        parse_mode=ParseMode.MARKDOWN
    )

def sub(update: Update, context: CallbackContext) -> None:

    global count

    reply_keyboard = [
        ["/queue"],
        ["/sub", "/add"]
    ]
    help_keyboard = [
        ["/add"]
    ]

    if count <= 1:
        update.message.reply_text(
            "queue cant be < {}. /add instead".format(count),
            reply_markup=ReplyKeyboardMarkup(help_keyboard),
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        count -= 1
        update.message.reply_text(
            "queue {} song(s)\nuse /add for more".format(count),
            reply_markup=ReplyKeyboardMarkup(reply_keyboard),
            parse_mode=ParseMode.MARKDOWN
        )

def queue(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /next is issued."""

    global count

    try:
        for i in range(count):
            url = "https://t.me/crateofnotsodasbutmusic/{}".format(
                random.choice(list(d.values())))

            reply_keyboard = [
                ["/sub", "/add"],
                ["/queue"],
                ["/start"]
            ]
            
            update.message.reply_audio(
                "{}".format(url),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=ReplyKeyboardMarkup(
                    reply_keyboard,
                    one_time_keyboard=True
                )
            )

    except (BadRequest) as e:
        logger.warning(e)
    
def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text("/next Add to playlist.")
    
def search(update: Update, context: CallbackContext) -> None:
    """Search the user's message."""
    global key
    global val
    global x
    
    val = [
        v
        for k, v in d.items()
        if re.search(update.message.text, k, re.IGNORECASE)
    ]
    key = [
        k
        for k, v in d.items()
        if re.search(update.message.text, k, re.IGNORECASE)
    ]
    
    keyboard = [
        [
            InlineKeyboardButton(
                "<",
                callback_data="1"
            ),
            
            InlineKeyboardButton(
                ">",
                callback_data="2"
            ),
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)

    x = 0

    text = (
        "👺\nResult {} of {}\n ""[{}]({})\n".format(
            key.index(key[x]),
            len(key),
            key[x],
            dcr8_url+"{}".format(val[x])
            )
    )
    
    update.message.reply_text(
        text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )    
    
    """
    update.message.reply_audio(
    "{}{}".format(url, i),
    reply_markup=reply_markup,
    parse_mode=ParseMode.MARKDOWN
    )
"""
    
def button(update: Update, context: CallbackContext) -> None:
    global key
    global val
    global x
    
    query = update.callback_query
    
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer(text="🤖")

    keyboard = [
        [
            InlineKeyboardButton(
                "<",
                callback_data="1"
            ),
            
            InlineKeyboardButton(
                ">",
                callback_data="2"
            ),
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        if query.data == '1':
            x -= 1
            text = "👺\nResult {} of {}\n ""[{}]({})\n".format(
                key.index(key[x]),
                len(key),
                key[x],
                dcr8_url+"{}".format(val[x])
            )

            query.edit_message_text(
                text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif query.data == '2':
            x += 1
            text = "👺\nResult {} of {}\n ""[{}]({})\n".format(
                key.index(key[x]),
                len(key),
                key[x],
                dcr8_url+"{}".format(val[x])
            )

            query.edit_message_text(
                text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
    except(IndexError, BadRequest):
        pass
    
def inlinequery(update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""

    query = update.inline_query.query
    results = []

    for k, v in d.items():
        if re.search(query, k, re.IGNORECASE):
            results.append(
                InlineQueryResultAudio(
                    id=uuid4(),
                    audio_url="{}{}".format(dcr8_url, v),
                    title="{}".format(k)
                ),
            )
        
    update.inline_query.answer(results, auto_pagination=True)

def stage1(update: Update, context: CallbackContext) -> int:

    return STAGE2

def stage2(update: Update, context: CallbackContext) -> int:

    return STAGE3

def stage3(update: Update, context: CallbackContext) -> int:

    return STAGE4

def stage4(update: Update, context: CallbackContext) -> int:

    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:

    return ConversationHandler.END

def error_handler(update: Update, context: CallbackContext) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    
    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)
    
    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    message = (
        f'An exception was raised while handling an update\n'
        f'<pre>update = {html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False))}'
        '</pre>\n\n'
        f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
        f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
        f'<pre>{html.escape(tb_string)}</pre>'
    )
    
    # Finally, send the message
    context.bot.send_message(chat_id=DEVELOPER_CHAT_ID, text=message, parse_mode=ParseMode.HTML)
    
def bad_command(update: Update, context: CallbackContext) -> None:
    """Raise an error to trigger the error handler."""
    context.bot.wrong_method_name()
        

def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(
        "1575933473:AAE-pseOycvK1OU32k1P2xVAH0Lwx_Ikjmg", use_context=True
    )
    
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register a deep-linking handler
    dp.add_handler(
        CommandHandler(
            "start",
            deep_linked_level_1,
            Filters.regex(DECR8)
        )
    )
    
    # This one works with a textual link instead of an URL
    dp.add_handler(
        CommandHandler(
            "start",
            deep_linked_level_2,
            Filters.regex(SO_COOL)
        )
    )

    # We can also pass on the deep-linking payload
    dp.add_handler(
        CommandHandler(
            "start",
            deep_linked_level_3,
            Filters.regex(USING_ENTITIES),
            pass_args=True
        )
    )

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            STAGE1: [MessageHandler(Filters.regex('^(/start|/queue|/cancel)$'), stage1)],
            STAGE3: [
                MessageHandler(Filters.location, stage3),
                CommandHandler('skip', stage3),
            ],
            STAGE4: [MessageHandler(Filters.text & ~Filters.command, stage4)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("queue", queue))
    dp.add_handler(CommandHandler("add", add))
    dp.add_handler(CommandHandler("sub", sub))
    
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("bad_command", bad_command))
    
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(InlineQueryHandler(inlinequery))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, search))
    dp.add_handler(CallbackQueryHandler(button))    
    dp.add_handler(conv_handler)
    dp.add_error_handler(error_handler)

    # Start the Bot
    updater.start_polling()
    
    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()    
        
if __name__ == "__main__":
    with open(
            "/home/ayuko/decr8/res/decr8_data.json",
            "r+",
            encoding="utf-8") as f:
        logger.info("Unpacking data to dict.")
        d = json.load(f)
        sorted(d)
        
    main()
                
