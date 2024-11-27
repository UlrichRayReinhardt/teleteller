import telebot


def push_to_telegram(message, bot_token, tg_channel):
    try:
        bot = telebot.TeleBot(bot_token)
        channel_name = tg_channel
        # bot.send_photo(chat_id=channel_name,photo=image, caption=title)
        bot.send_message(chat_id=channel_name, text=message, parse_mode="Markdown")
    except Exception as e:
        print(f"Error sending message to Telegram: {e}")
