import telebot

bot = telebot.TeleBot('1248279229:AAFIcyEfBr5n40l7OXoGD8d4MiAxbHDyfhw')


@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.reply_to(message, f"Hi \U0001F44B, you can start play with "
                          f"random: /quiz category \nor you can choose "
                          f"it /category")



bot.polling()