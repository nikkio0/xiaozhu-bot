from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
import logging
import os

groups = {}

with open("groups/index") as f:
    group_names = set(f.read().strip().split('\n'))

for group_name in group_names:
    with open(f"groups/{group_name}.group") as f:
        members = f.read().strip()
        if len(members) == 0:
            groups[group_name] = set()
        else:
            groups[group_name] = set([int(uid) for uid in members.split('\n')])

with open('token.secret') as f:
    token = f.read().strip()

def init_group(group_name):
    groups[group_name] = set()
    with open(f"groups/{group_name}.group", 'w') as f:
        f.write("")
    with open(f"groups/index", 'a') as f:
        f.write(group_name)

def update_group(group_name):
    print(group_name)
    if len(groups[group_name]) == 0:
        with open(f"groups/index") as f:
            group_names = set(f.read().strip().split('\n'))
        group_names.remove(group_name)
        with open(f"groups/index", 'w') as f:
            f.write("\n".join(group_names))
        os.remove(f"groups/{group_name}.group")
    else:
        with open(f"groups/{group_name}.group", 'w') as f:
            text = "\n".join([str(user_id) for user_id in groups[group_name]])
            f.write(text)

def get_group_name(update):
    msg = update.message.text.strip().split()
    group_name = "default"
    for i in range(len(msg)):
        if msg[i].find('count_me_in') != -1:
            if i != len(msg) - 1:
                group_name = msg[i + 1]
    return group_name

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def zhu(update, context):
    help_text = (
                "小猪bot是本群的吉祥物，请尽情调戏。\n"
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
    group_name = get_group_name(update)
    if username:
        if not groups.get(group_name):
            init_group(group_name)
        try:
            if user_id not in groups[group_name]:
                context.bot.send_message(chat_id=user_id, text=f"嗯，下次喊 {group_name} 就叫上你！")
                groups[group_name].add(user_id)
            else:
                context.bot.send_message(chat_id=user_id, text=f"Oink！本来就要叫上你的。")
        except Exception:
            context.bot.send_message(chat_id=update.effective_chat.id, text="先跟我说句话: https://t.me/xiaozhu_notify_bot")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"唉，我没找到你的用户名啊，快加一个去！")
    update_group(group_name)

in_handler = CommandHandler('count_me_in', opt_in)
dispatcher.add_handler(in_handler)

def opt_out(update, context):
    user_id = update.effective_user.id
    group_name = get_group_name(update)
    try:
        if not groups.get(group_name) or user_id not in groups[group_name]:
            context.bot.send_message(chat_id=user_id, text=f"滚滚滚！本来就不会叫你的，别来烦我！")
        else:
            context.bot.send_message(chat_id=user_id, text=f"哼，伦家本来就不想理你！")
            groups[group_name].remove(user_id)
    except Exception:
        context.bot.send_message(chat_id=update.effective_chat.id, text="先跟我说句话: https://t.me/xiaozhu_notify_bot")
    update_group(group_name)

out_handler = CommandHandler('count_me_out', opt_out)
dispatcher.add_handler(out_handler)

def ping(update, context):
    caller = update.effective_user
    group_name = get_group_name(update)
    for user_id in groups[group_name]:
        context.bot.send_message(chat_id=user_id, text=f"[{group_name}] {caller.full_name}叫你去围观啦！ {update.effective_chat.link}")
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"我已经把它们都拱了一遍了！Oink Oink！")

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
