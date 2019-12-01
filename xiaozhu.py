from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
import os


def init_group(group_name):
    if group_name is not "default":
        groups[group_name] = set()
        with open(f"{prefix}/groups/{group_name}.group", 'w') as f:
            f.write("")
        with open(f"{prefix}/groups/index", 'a') as f:
            f.write(group_name)


def update_group(group_name):
    with open(f"{prefix}/groups/{group_name}.group", 'w') as f:
        text = "\n".join([str(user_id) for user_id in groups[group_name]])
        f.write(text)
    if len(groups[group_name]) == 0:
        with open(f"{prefix}/groups/index") as f:
            group_names = set(f.read().strip().split('\n'))
        if group_name is not "default":
            group_names.remove(group_name)
            os.remove(f"{prefix}/groups/{group_name}.group")
            with open(f"{prefix}/groups/index", 'w') as f:
                f.write("\n".join(group_names) + '\n')


def get_group_name(update, command):
    msg = update.message.text.strip().split()
    group_name = "default"
    for i in range(len(msg)):
        if msg[i].find(command) != -1:
            if i != len(msg) - 1:
                group_name = msg[i + 1]
    return group_name


def zhu(update, context):
    help_text = (
                "小猪bot是本群的吉祥物，请尽情调戏。\n"
                "小猪可以帮你呼唤沉睡不醒的群友进群围观。\n"
                "在使用前请先征求小猪bot同意：https://t.me/xiaozhu_notify_bot\n"
                "如过想要让小猪拥有更多超能力，请于 "
                "https://github.com/6etacat/xiaozhu-bot 贡献代码\n"
                "具体使用方法请输入 /help"
                 )
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)


def opt_in(update, context):
    user_id = update.effective_user.id
    username = update.effective_user.name
    group_name = get_group_name(update, 'count_me_in')
    if username:
        if not groups.get(group_name):
            init_group(group_name)
        try:
            if user_id not in groups[group_name]:
                t = f"嗯，下次喊 {group_name} 就叫上你！"
                context.bot.send_message(chat_id=user_id, text=t)
                groups[group_name].add(user_id)
            else:
                t = f"Oink！本来就要叫上你的。"
                context.bot.send_message(chat_id=user_id, text=t)
        except Exception:
            t = "先跟我说句话: https://t.me/xiaozhu_notify_bot"
            context.bot.send_message(chat_id=update.effective_chat.id, text=t)
    else:
        t = ("唉，我没找到你的用户名啊，快加一个去！\n"
             "如果有用户名却还有问题，请联系 https://t.me/m_6etacat")
        context.bot.send_message(chat_id=update.effective_chat.id, text=t)
    update_group(group_name)


def opt_out(update, context):
    user_id = update.effective_user.id
    group_name = get_group_name(update, 'count_me_out')
    try:
        if not groups.get(group_name) or user_id not in groups[group_name]:
            t = f"滚滚滚！本来就不会叫你的，别来烦我！"
            context.bot.send_message(chat_id=user_id, text=t)
        else:
            t = f"哼，伦家也不想理你！"
            context.bot.send_message(chat_id=user_id, text=t)
            groups[group_name].remove(user_id)
    except Exception:
        t = "先跟我说句话: https://t.me/xiaozhu_notify_bot"
        context.bot.send_message(chat_id=update.effective_chat.id, text=t)
    update_group(group_name)


def ping(update, context):
    caller = update.effective_user
    group_name = get_group_name(update, '/oink')
    if update.effective_chat.link:
        link = update.effective_chat.link
    elif update.effective_chat.invite_link:
        link = update.effective_chat.invite_link
    else:
        grp = update.effective_chat.title
        link = f"唉，我搞不到群聊的链接，快让“{grp}”群主把我加成管理员！"
    for user_id in groups[group_name]:
        t = f"[{group_name}] {caller.full_name}叫你去围观啦！ {link}"
        context.bot.send_message(chat_id=user_id, text=t)
    t = f"我已经把 {group_name} 都拱了一遍了！Oink Oink！"
    context.bot.send_message(chat_id=update.effective_chat.id, text=t)


def tian(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="舔！！！")


def helper(update, context):
    help_text = (
                "/zhu 小猪bot的简单自我介绍\n"
                "/count_me_in 和 /count_me_out 会将你加入/移除默认通知名单\n"
                "/count_me_in [group_name] 和 /count_me_out [group_name] "
                "会将你加入[group_name]通知名单\n"
                "/oink [group_name] 会私信通知[group_name]名单中的所有人，"
                "默认为默认名单\n"
                "/tian 请不要过分调戏小猪\n"
                "/help 帮助"
                 )
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)


def unknown(update, context):
    t = "Sorry, I didn't understand that command."
    context.bot.send_message(chat_id=update.effective_chat.id, text=t)


prefix = "/home/michael/xiaozhu-bot"
groups = {}

with open(f"{prefix}/groups/index") as f:
    group_names = set(f.read().strip().split('\n'))

for group_name in group_names:
    with open(f"{prefix}/groups/{group_name}.group") as f:
        members = f.read().strip()
        if len(members) == 0:
            groups[group_name] = set()
        else:
            groups[group_name] = set([int(uid) for uid in members.split('\n')])

with open(f'{prefix}/token.secret') as f:
    token = f.read().strip()

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher


start_handler = CommandHandler('zhu', zhu)
in_handler = CommandHandler('count_me_in', opt_in)
out_handler = CommandHandler('count_me_out', opt_out)
ping_handler = CommandHandler('oink', ping)
tian_handler = CommandHandler('tian', tian)
help_handler = CommandHandler('help', helper)
unknown_handler = MessageHandler(Filters.command, unknown)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(in_handler)
dispatcher.add_handler(out_handler)
dispatcher.add_handler(ping_handler)
dispatcher.add_handler(tian_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(unknown_handler)

if __name__ == "__main__":
    updater.start_polling()
