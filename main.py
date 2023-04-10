import os

from telegram import Update
from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          CallbackContext, Filters)
from dotenv import load_dotenv

from video_in_audio import video_in_audio, del_create_file

load_dotenv()
TOKEN = os.getenv("TOKEN")


def start(update: Update, context: CallbackContext):
    update.message.reply_text('Привет! Отправь мне ссылку на видео с Youtube,'
                              ' а я пришлю тебе его аудиодорожку (подкаст).')


def send_audio(update: Update, context: CallbackContext):
    url = update.message.text
    if len(video_in_audio(url)) > 2:
        update.message.reply_text(video_in_audio(url))
    else:
        audio_file_path, audio_file = video_in_audio(url)
        with open(audio_file, 'rb') as audio:
            update.message.reply_audio(audio)
        del_create_file(audio_file_path)


def error(update: Update, context: CallbackContext):
    print(f'Update {update} caused error {context.error}')


def main():
    updater = Updater(TOKEN,
                      use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.regex(r'https?://(?:www\.)?youtu'
                                                r'(?:be\.com|\.be)\/'
                                                r'(?:watch\?v=)?(\S+)'),
                                  send_audio))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
