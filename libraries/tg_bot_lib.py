import telebot
import threading

_bot = None

def start(token):
    global _bot
    _bot = telebot.TeleBot(token)
    print("Telegram бот запущен...")
    _bot.polling(non_stop=True)

def on_message(word, handler):
    """Если бот получает word, вызывает функцию handler"""
    @_bot.message_handler(func=lambda message: message.text == word)
    def wrapper(message):
        handler(message)

def reply(message, text):
    """Ответить на сообщение"""
    _bot.reply_to(message, text)

# Русские псевдонимы
запустить = start
на_сообщение = on_message
ответить = reply