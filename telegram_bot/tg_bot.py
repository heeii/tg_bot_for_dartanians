import telebot
import telebot.util as util
import time
import chatgpt_api as chatgpt
from system_func import *

_token = parse('GaryToken')
bot = telebot.TeleBot(_token)
_log = parse(name='log')


@bot.message_handler(commands=['start', 'help', 'site', 'gpt', 'timetable', 'inside', 'stop'])
def bot_commands(command):
    role = bot.get_chat_member(command.chat.id, command.from_user.id).status
    command_request = util.extract_command(command.text)

    logging(command.from_user.username, command_request)

    if command_request == 'start':
        bot.send_message(command.chat.id, "Напиши /help для получения информации о моих командах")
    elif command_request == 'help':
        bot.send_message(command.chat.id, "/help - справка\n/site - для перехода на сайт"
                                          " (в разработке)\n/gpt *** - запрос в ChatGPT\n/timetable - расписание занятий (в разработке)"
                                          "\n/inside - поиск внутри группы (в разработке)\n/stop - для остановки бота")
    elif command_request == 'site':
        bot.send_message(command.chat.id, "СКАЗАНО ЖЕ БЛЯТЬ 'site' В РАЗРАБОТКЕ")
    elif command_request == 'gpt':
        bot.send_message(command.chat.id, chatgpt.something())
    elif command_request == 'timetable':
        bot.send_message(command.chat.id, "СКАЗАНО ЖЕ БЛЯТЬ 'timetable' В РАЗРАБОТКЕ")
    elif command_request == 'inside':
        bot.send_message(command.chat.id, "СКАЗАНО ЖЕ БЛЯТЬ 'inside' В РАЗРАБОТКЕ")
    elif command_request == 'stop':
        print(role)
        print(command.chat.type)
        if role in ['administrator',
                    'creator'] or command.chat.type == 'private':  # role = member, administrator, creator     #type = private, group, supergroup, channel
            bot.send_message(command.chat.id, "Остановка бота . . .")
            bot.stop_bot()
            bot.send_message(command.chat.id, "Бот успешно остановлен")
        else:
            bot.send_message(command.chat.id, "У вас нет прав на остановку бота")
    else:
        bot.send_message(command.chat.id, "Введена неизвестная команда, напиши /help")


# @bot.message_handler(content_types=['text', 'document', 'audio'])
# def get_text_messages(message):
#     if message.text == "Привет":
#         bot.send_message(message.chat.id, "Привет -_-")
#         time.sleep(1.5)
#         bot.send_message(message.chat.id, "Помощь нужна?")
#         time.sleep(3)
#         bot.send_message(message.chat.id, "/start пиши, хуль сидишь")



start = telebot.types.BotCommand('/start', "начать общение")
help_ = telebot.types.BotCommand('/help', "список команд")
site = telebot.types.BotCommand('/site', "открыть сайт")
gpt = telebot.types.BotCommand('/gpt', "поиск в ChatGPT")
timetable = telebot.types.BotCommand('/timetable', "расписание МГТУ")
inside = telebot.types.BotCommand('inside', "поиск внутри группы")
stop = telebot.types.BotCommand('stop', "остановить бота можно с правами администратора и выше")

bot.set_my_commands([start, help_, site, gpt, timetable, inside, stop])

bot.infinity_polling()
