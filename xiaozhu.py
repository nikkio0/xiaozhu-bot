from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
import logging

opt_in_users = set()

with open('token.secret') as f:
    token = f.read().strip()

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def zhu(update, context):
    help_text = ("小猪bot是本群的吉祥物，请尽情调戏。\n"
                 "小猪可以帮你呼唤沉睡不醒的群友进群围观。\n"
                 "在使用前请先征求小猪bot同意：https://t.me/xiaozhu_notify_bot\n"
                 "具体使用方法请输入 /help"
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)

start_handler = CommandHandler('zhu', zhu)
dispatcher.add_handler(start_handler)

def opt_in(update, context):
    user_id = update.effective_user.id
    username = update.effective_user.name
    if username:
        try:
            if user_id not in opt_in_users:
                context.bot.send_message(chat_id=user_id, text=f"嗯，下次叫上你！")
                opt_in_users.add(user_id)
            else:
                context.bot.send_message(chat_id=user_id, text=f"Oink！本来就要叫上你的。")
        except Exception:
            context.bot.send_message(chat_id=update.effective_chat.id, text="先跟我说句话: https://t.me/xiaozhu_notify_bot")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"唉，我没找到你的用户名啊，快加一个去！")

in_handler = CommandHandler('count_me_in', opt_in)
dispatcher.add_handler(in_handler)

def opt_out(update, context):
    user_id = update.effective_user.id
    try:
        if user_id not in opt_in_users:
            context.bot.send_message(chat_id=user_id, text=f"滚滚滚！本来就不会叫你的，别来烦我！")
        else:
            context.bot.send_message(chat_id=user_id, text=f"哼，伦家本来就不想理你！")
            opt_in_users.remove(user_id)
    except Exception:
        context.bot.send_message(chat_id=update.effective_chat.id, text="先跟我说句话: https://t.me/xiaozhu_notify_bot")

out_handler = CommandHandler('count_me_out', opt_out)
dispatcher.add_handler(out_handler)

def ping(update, context):
    caller = update.effective_user
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{caller.full_name}叫你去围观啦！ {update.effective_chat.link}")

ping_handler = CommandHandler('oink', ping)
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
