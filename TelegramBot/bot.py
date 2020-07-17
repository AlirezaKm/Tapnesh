from telegram.ext import (
    Updater,
    MessageHandler,
    Filters,
    ConversationHandler,
    CommandHandler
)
from TelegramBot.handlers import (
    photo_handler,
    GET_QUALITY,
    cancel,
    get_quality,
    text_handler
)
import logging
import sys
import os


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

if len(sys.argv) != 5:
    raise Exception('Usage: {} <TOKEN> <WEBHOOK [0 or 1]> <PORT> <DOMAIN>'.format(sys.argv[0]))

# Required Variables
TOKEN = str(sys.argv[1])
WEB_HOOK = True if str(sys.argv[2]) == "1" else False
PORT = int(sys.argv[3])
DOMAIN = str(sys.argv[4])

# Define Bot
updater = Updater(
    TOKEN,
    use_context=True
)

# Define Dispatcher
dispatcher = updater.dispatcher


# Construct Conversation
conversation = ConversationHandler(
    entry_points=[
        MessageHandler(Filters.text, text_handler),
        MessageHandler(Filters.document | Filters.photo, photo_handler)
    ],

    states={
        GET_QUALITY: [
            CommandHandler('cancel', cancel),
            MessageHandler(Filters.text, get_quality)
        ]
    },

    fallbacks=[CommandHandler('cancel', cancel)]
)

# Add Handler
dispatcher.add_handler(conversation)

# Start Bot

if not WEB_HOOK:
    # Start Polling
    updater.start_polling()
else:
    # Start webhook
    updater.start_webhook(
        listen='0.0.0.0',
        port=PORT,
        url_path=TOKEN
    )
    updater.bot.set_webhook(os.path.join(DOMAIN, TOKEN))

updater.idle()
