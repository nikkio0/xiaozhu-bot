from telegram.ext import Updater
from telegram.ext import CommandHandler
import logging

opt_in_users = []

with open('token.secret') as f:
    token = f.read().strip()

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ping me when you want to notify all people in chat with: @xiaozhu /ping")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def opt_in(update, context):
    user_id = update.effective_user.id
    username = update.effective_user.name
    if username:
        try:
            context.bot.send_message(chat_id=user_id, text=f"You have opt in to receive notifications. ")
        except Exception:
            context.bot.send_message(chat_id=update.effective_chat.id, text="You have to start a conversation with me first: https://t.me/xiaozhu_notify_bot")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"You don't have a username. Please set one in the settings")

in_handler = CommandHandler('oink', opt_in)
dispatcher.add_handler(in_handler)

def ping(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"You are {update.effective_user.username}")
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Pinging @{update.effective_user.username}")

ping_handler = CommandHandler('ping', ping)
dispatcher.add_handler(ping_handler)

def tian(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="舔！！！")

tian_handler = CommandHandler('tian', tian)
dispatcher.add_handler(tian_handler)

updater.start_polling()
