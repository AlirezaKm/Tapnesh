from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, Document
from telegram.ext import ConversationHandler, CallbackContext
from hashlib import sha256
import time
import os

# Tapnesh Command
TAPNESH = "/bin/bash /bin/tapnesh -p '{PHOTO}' -q '{QUALITY}'"

# State Mapping
PHOTO_HANDLER, GET_QUALITY = range(2)

# Valid Qualities
SUPPORTED_QUALITIES = [['80', '50', '20']]

# Supported MimeTypes
SUPPORTED_MIMETYPES = [
    'image/png',
    'image/jpeg'
]


# Define Handlers
def text_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        "In order to use this bot, you can send a photo: "
        "['png' or 'jpg'] as a document or a photo"
    )


def photo_handler(update: Update, context: CallbackContext):
    document: Document = update.message.document
    if update.message.document is not None:
        if document.mime_type not in SUPPORTED_MIMETYPES:
            update.message.reply_text(
                "Your sent file not supported ({}).\n"
                "Supported files: ['png', 'jpg']".format(
                    document.mime_type
                )
            )
            return ConversationHandler.END

        # Get Document
        photo = document.get_file()
        photo_name = document.file_name
    else:

        # Get photo
        photo = update.message.photo[-1].get_file()
        photo_name = "{}.jpg".format(photo.file_unique_id)

    message = update.effective_message.reply_text(
        text="Downloading your photo ...."
    )

    # Generate a name for photo
    extension = '' if '.' not in photo_name else ".{}".format(photo_name.split('.')[-1].strip())
    upload_file = "{}{}".format(
        sha256((str(time.time()) + photo_name).encode()).hexdigest()[:12]
        , extension
    )

    # Downlod photo
    photo.download(upload_file)

    # Store name for further usage
    context.user_data['photo'] = upload_file
    context.user_data['photo_size'] = photo.file_size

    # Pass Message
    message.edit_text("Your photo downloaded.\n"
                      "Size: {} bytes".format(photo.file_size))

    # Choose Quality
    update.message.reply_text(
        "Now, Choose Quality (you can send me your expected value between [1, 99]) "
        "or send /cancel if you don't want to continue.",
        reply_markup=ReplyKeyboardMarkup(SUPPORTED_QUALITIES, one_time_keyboard=True)
    )

    return GET_QUALITY


def cancel(update: Update, context: CallbackContext):
    # Remove Uploaded Photo
    photo = context.user_data.get('photo')
    if photo:
        os.remove(photo)

    update.message.reply_text(
        text='process canceled.',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def get_quality(update: Update, context: CallbackContext):
    quality = str(update.message.text)
    error_message = "Your input is not valid.\n" \
                    "Choose Quality (you can send me your expected value between [1, 99]) " \
                    "or send /cancel if you don't want to continue."

    if not quality.isnumeric():
        # Choose Valid Quality
        update.message.reply_text(
            error_message,
            reply_markup=ReplyKeyboardMarkup(SUPPORTED_QUALITIES, one_time_keyboard=True)
        )
        return GET_QUALITY

    # Convert quality to integer
    quality = int(quality)
    if not (1 <= quality <= 99):
        # Choose Valid Quality
        update.message.reply_text(
            error_message,
            reply_markup=ReplyKeyboardMarkup(SUPPORTED_QUALITIES, one_time_keyboard=True)
        )
        return GET_QUALITY

    # Pass a Message
    message = update.message.reply_text('In processing...')

    # get filename
    photo = context.user_data.get('photo')

    # Reduce photo size
    os.system(TAPNESH.format(
        PHOTO=photo,
        QUALITY=quality
    ))

    # Delete in processing message
    message.delete()

    # Get Size of new file and old file
    old_size = int(context.user_data['photo_size'])
    new_size = int(os.stat(photo).st_size)

    # Upload Photo
    context.bot.send_document(
        chat_id=update.effective_chat.id,
        caption="Previous Size: {} bytes\n"
                "New Size     : {} bytes\n"
                "Reduced      : {} bytes".format(old_size, new_size, old_size - new_size),
        document=open(photo, 'rb'),
        reply_markup=ReplyKeyboardRemove()
    )

    # Remove Photo
    os.remove(photo)

    return ConversationHandler.END
