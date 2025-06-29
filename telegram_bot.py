import telegram

async def send(msg, chat_id, token):
    """
    Send a mensage to a telegram user specified on chatId
    chat_id must be a number!
    """
    bot = telegram.Bot(token=token)
    notification_message = "<b>Neue Netflix E-Mail erhalten!</b>"
    notification_message += "\n\n"
    notification_message += f"Bitte draufklicken → {msg}"
    notification_message += "\n\n"
    notification_message += "Viel Spaß!"
    await bot.send_message(chat_id=chat_id, text=notification_message, parse_mode="html")

async def error_msg(msg, chat_id, token):
    """
    Send a mensage to a telegram user specified on chatId
    chat_id must be a number!
    """
    bot = telegram.Bot(token=token)
    notification_message = "<b>Error!</b>"
    notification_message += "\n\n"
    notification_message += f" {msg}"
    notification_message += "\n\n"
    await bot.send_message(chat_id=chat_id, text=notification_message, parse_mode="html")