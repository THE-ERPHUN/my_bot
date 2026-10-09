import time
import telebot

TOKEN = "*"

bot = telebot.TeleBot(TOKEN)

joined_users = {}

@bot.message_handler(content_types=['new_chat_members'])
def track_new_member(message):
    for member in message.new_chat_members:
        joined_users[member.id] = time.time()
        print(f"کاربر جدید ثبت شد: {member.first_name} (ID: {member.id})")

@bot.message_handler(commands=['clean24'])
def clean_recent_members(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    status = bot.get_chat_member(chat_id, user_id).status
    if status not in ['administrator', 'creator']:
        bot.reply_to(message, "❌ فقط ادمین‌های گروه می‌توانند این دستور را اجرا کنند.")
        return

    current_time = time.time()
    seconds_in_24h = 24 * 60 * 60
    kicked_count = 0

    bot.reply_to(message, "⏳ در حال بررسی و پاکسازی اعضایی که در ۲۴ ساعت گذشته جوین شده‌اند...")

    for uid, join_time in list(joined_users.items()):
        if current_time - join_time <= seconds_in_24h:
            try:
                bot.ban_chat_member(chat_id, uid)
                kicked_count += 1
                del joined_users[uid]
            except Exception as e:
                print(f"خطا در اخراج کاربر {uid}: {e}")

    bot.send_message(chat_id, f"✅ عملیات با موفقیت انجام شد.\nتعداد {kicked_count} کاربر که در ۲۴ ساعت گذشته وارد شده بودند، پاک شدند.")

print("ربات پاکسازی آماده به کار است...")
bot.polling(non_stop=True)
