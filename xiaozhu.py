from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
import logging

opt_in_users = []

with open('token.secret') as f:
    token = f.read().strip()

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def zhu(update, context):
    help_text = """小猪bot是本群的吉祥物，请尽情调戏。\n小猪可以帮你呼唤沉睡不醒的群友进群围观。\n在使用前请先征求小猪bot同意：https://t.me/xiaozhu_notify_bot"""
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)

start_handler = CommandHandler('zhu', zhu)
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

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()
