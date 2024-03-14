import telebot
import telebot.util as util
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import WebAppInfo
import time
from chatgpt_api import gpt_4
from system_func import *
from timetable import week_time, get_timetable as table

_token = jparse('GaryToken')
bot = telebot.TeleBot(_token)

_adm = jparse('AdminChatId')

# site, gpt, timetable, inside, text
""" ДА, НЕТ,        ДА,    НЕТ,  НЕТ и я рот ебал"""

print("\033[31mДОДЕЛАТЬ КОМАНДУ CLEAR\033[0m")
@bot.message_handler(commands=['start', 'help', 'site', 'gpt', 'timetable', 'inside', 'text'])
def bot_commands(command):
    role = bot.get_chat_member(command.chat.id, command.from_user.id).status
    command_request = util.extract_command(command.text)
    message = command.text
    data = extract_data(message, command_request)
    logging(command.from_user.username, command_request)

    if command_request == 'start':
        bot.send_message(command.chat.id, "Напиши /help для получения информации о моих командах")

    elif command_request == 'help':
        bot.send_message(command.chat.id, "/help \- список команд\n\n/site \- открытие сайта внутри телеграмма "
                                          "\(Ссылка придет ответом в личные сообщения\)\n\n/gpt \*\*\* \- запрос в ChatGPT __*\(В ТЕСТОВОМ режиме\)*__"
                                          "\n\n/timetable \- расписание занятий "
                                          "\(Для просмотра расписания за дургой день выберите неделю и день\)"
                                          "\n\n/inside \- поиск внутри группы __*\(в разработке\)*__"
                                          "\n\n/text \- преобразование аудио и видео сообщений в текст __*\(в разработке\)*__", parse_mode='MarkdownV2')
                                          #  *text* - bold, _text_ - cursive, __text__ - underline
    elif command_request == 'site':
        bot.send_message(command.chat.id, "Загляните в личные сообщения")
        web_button = InlineKeyboardMarkup()
        data = 'https://' + data
        info = WebAppInfo(data)
        button1 = InlineKeyboardButton("Ваш сайт", web_app=info)
        web_button.add(button1)
        bot.send_message(command.from_user.id, "Ваша ссылка, она откроется внутри телеграмма", reply_markup=web_button)

    elif command_request == 'gpt':
# Запрос GPT (НЕ ДО КОНЦА)
        gpt_data = extract_data(message, command_request, spaces=True)
        bot.send_message(command.chat.id, gpt_4(gpt_data))

    elif command_request == 'timetable':
        otkeyboard = InlineKeyboardMarkup()
        resp = table(week=week_time()[0], day=week_time()[1])

        if resp is not None:
            res = 'Расписание за текущий день:\n\n№ Пары\n| Предмет\n| Тип\n| Преподаватель\n| Кабинет\n\n'
            for pair in resp:
                mes = str(pair) + ' \n| '
                for elem in resp[pair]:
                    mes += elem + ' \n| '
                res += mes[:-3] + '\n\n'
        else:
            res = 'Сегодня не учебный день'
        bot.send_message(command.chat.id, res)

        if week_time()[0] == 1:
            otkeyboard.add(InlineKeyboardButton(text='Четная', callback_data='week2'))
            otkeyboard.add(InlineKeyboardButton(text='Нечетная(Текущая)', callback_data='week1'))
        else:
            otkeyboard.add(InlineKeyboardButton(text='Четная(Текущая)', callback_data='week2'))
            otkeyboard.add(InlineKeyboardButton(text='Нечетная', callback_data='week1'))
        bot.send_message(command.chat.id, 'Выберите неделю', reply_markup=otkeyboard)

    elif command_request == 'inside':
# Поиск внутри группы среди всех чатов (Стоит)
        bot.send_message(command.chat.id, "СКАЗАНО ЖЕ БЛЯТЬ 'inside' В РАЗРАБОТКЕ")

    elif command_request == 'text':
        ...
# Распознование речи
# И занимаюсь я этой хуйней только из-за ебаного телеграмма
# Который не дает одному боту общаться с другим
# Пиздец нахуй блять

    else:
        bot.send_message(command.chat.id, "Введена неизвестная команда, напиши /help")


counter = 0


@bot.message_handler(commands=['this!', 'clear!', 'stop!'])
def bot_hidden_commands(hidden_command):
    role = bot.get_chat_member(hidden_command.chat.id, hidden_command.from_user.id).status
    command_request = util.extract_command(hidden_command.text)
    message = hidden_command.text
    data = extract_data(message, command_request)

    global counter, _token, _adm

    logging(hidden_command.from_user.username, command_request + ' (HIDDEN)')

    if command_request == 'this!':
        import time

        if jchange('AdminChatId', str(hidden_command.chat.id)):
            bot.send_message(hidden_command.chat.id, '*SUCCESS*', parse_mode='MarkdownV2')
            time.sleep(1)
            stp = 2
        else:
            bot.send_message(hidden_command.chat.id, '*ERROR ID CHANGING*\n\n*REPLACING VITAL PARTS WITH EMERGENCY ONE*\n\n*WAIT \. \. \.*', parse_mode='MarkdownV2')
            _token = jparse('GaryToken', name='DO_NOT_TOUCH')
            _adm = jparse('AdminChatId', name='DO_NOT_TOUCH')
            time.sleep(4.5)
            bot.send_message(hidden_command.chat.id, '*SUCCESS*', parse_mode='MarkdownV2')
            time.sleep(1)
            stp = 3

        bot.delete_messages(hidden_command.chat.id, [id_ for id_ in range(hidden_command.id, hidden_command.id + stp)])

    # elif command_request == 'clear!':
    #     if role in ['administrator', 'creator'] or (
    #             hidden_command.chat.type == 'private' and hidden_command.from_user.username in [person.user.username for
    #                                                                                             person in
    #                                                                                             bot.get_chat_administrators(
    #                                                                                                 _adm)]):
    #         print(data)
    #         from system_func import __clear__ as clear
    #         import time
    #         if data is None:
    #             bot.send_message(hidden_command.chat.id, f'Cursor currently here:{clear()}')
    #         else:
    #             bot.send_message(hidden_command.chat.id, f'__*SUCCESSFULLY*__ DELETED TO {clear(data)} POINT', parse_mode='MarkdownV2')
    #             time.sleep(3)
    #             clear(data)
    #             import time
    #
    #             # logging(hidden_command.from_user.username, '! FILE WAS CLEARED !')
    #
    #     else:
    #         bot.send_message(hidden_command.chat.id, "*DENIED* \n\nYou don't have enough rights", parse_mode='MarkdownV2')

    elif command_request == 'stop!':
        if role in ['administrator', 'creator'] or (
                hidden_command.chat.type == 'private' and hidden_command.from_user.username in [person.user.username for
                                                                                                person in
                                                                                                bot.get_chat_administrators(
                                                                                                    _adm)]):
            # role = member, administrator, creator     #type = private, group, supergroup, channel

            otkeyboard = InlineKeyboardMarkup()
            otkeyboard.add(InlineKeyboardButton(text='ДА', callback_data='stopYes'))
            otkeyboard.add(InlineKeyboardButton(text='НЕТ', callback_data='stopNo'))
            bot.send_message(hidden_command.chat.id,
                             '__*\! \! \! ВНИМАНИЕ \! \! \!*__\n\nСледующее действие повлечет за собой '
                             '__*ПОЛНУЮ остановку*__ бота для __*ВСЕХ*__ пользователей\n\n'
                             'Вы уверены, что хотите остановить бота?', reply_markup=otkeyboard, parse_mode='MarkdownV2')
            counter = 0

        else:
            bot.send_message(hidden_command.chat.id, "*DENIED* \n\nYou don't have enough rights",
                             parse_mode='MarkdownV2')


week = 0


@bot.callback_query_handler(func=lambda call: True)
def otkeyboard_callback(call):
    global counter, week

    if counter < 1:
        if call.data == 'stopYes':
            bot.send_message(call.message.chat.id, "Остановка бота . . .")
            bot.stop_bot()
            bot.send_message(call.message.chat.id, "Бот успешно остановлен")
            counter += 1
        if call.data == 'stopNo':
            bot.send_message(call.message.chat.id, 'Остановка отменена')
            logging(call.from_user.username, 'stop denied')
            counter += 1
    elif counter == 1:
        bot.send_message(call.message.chat.id, 'Кнопка может быть нажата только 1 раз')
        counter += 1

    if call.data == 'week1':
        week = 1
        otkeyboard = InlineKeyboardMarkup()
        otkeyboard.add(InlineKeyboardButton(text='Понедельник', callback_data='mon'))
        otkeyboard.add(InlineKeyboardButton(text='Вторник', callback_data='tue'))
        otkeyboard.add(InlineKeyboardButton(text='Среда', callback_data='wed'))
        otkeyboard.add(InlineKeyboardButton(text='Четверг', callback_data='thu'))
        otkeyboard.add(InlineKeyboardButton(text='Пятница', callback_data='fri'))
        otkeyboard.add(InlineKeyboardButton(text='Суббота', callback_data='sat'))
        bot.send_message(call.message.chat.id, 'Выберите день (Нечетная)', reply_markup=otkeyboard)
    elif call.data == 'week2':
        week = 2
        otkeyboard = InlineKeyboardMarkup()
        otkeyboard.add(InlineKeyboardButton(text='Понедельник', callback_data='mon'))
        otkeyboard.add(InlineKeyboardButton(text='Вторник', callback_data='tue'))
        otkeyboard.add(InlineKeyboardButton(text='Среда', callback_data='wed'))
        otkeyboard.add(InlineKeyboardButton(text='Четверг', callback_data='thu'))
        otkeyboard.add(InlineKeyboardButton(text='Пятница', callback_data='fri'))
        otkeyboard.add(InlineKeyboardButton(text='Суббота', callback_data='sat'))
        bot.send_message(call.message.chat.id, 'Выберите день (Четная)', reply_markup=otkeyboard)

    if call.data == 'mon':
        resp = table(week, 1)
    elif call.data == 'tue':
        resp = table(week, 2)
    elif call.data == 'wed':
        resp = table(week, 3)
    elif call.data == 'thu':
        resp = table(week, 4)
    elif call.data == 'fri':
        resp = table(week, 5)
    elif call.data == 'sat':
        resp = table(week, 6)
        res = 'Не учебный день'

    if call.data == 'mon' or call.data == 'tue' or call.data == 'wed' or call.data == 'thu' or call.data == 'fri' or call.data == 'sat':
        if call.data != 'sat':
            res = '№ Пары\n| Предмет\n| Тип\n| Преподаватель\n| Кабинет\n\n'
            for pair in resp:
                mes = str(pair) + ' \n| '
                for elem in resp[pair]:
                    mes += elem + ' \n| '
                res += mes[:-3] + '\n\n'
        bot.send_message(call.message.chat.id, res)


@bot.message_handler(content_types=['audio', 'voice', 'video'])
def get_audio_messages(audio_message):
    # bot.forward_message()
    print(audio_message.id)
    print(jparse('SpeechBot'))
    a = bot.forward_message(jparse('SpeechBot'), audio_message.chat.id, audio_message.id)
    print(a)
    bot.send_message(audio_message.chat.id, 'ОНО БЛЯТЬ НЕ РАБОТАЕТ ПРОСТО ПОТОМУ ЧТО', reply_to_message_id=audio_message.id)


# def timetable_out(data_):
#     if data_ is not None and len(data_) >= 2:
#         data_ = is_digit(data_)
#         res = not None
#         if 0 < int(data_[0]) <= 2 and 0 < int(data_[1]) <= 7:
#             resp = table(week=int(data_[0]), day=int(data_[1]))
#         else:
#             if int(data_[0]) >= 3 or int(data_[0]) <= 0:
#                 resp = 'week'
#             else:
#                 resp = 'day'
#             res = None
#     else:
#         resp = table(week=week_time()[0], day=week_time()[1])
#         res = not None
#
#     if res is not None:
#         if data_ is not None and len(data_) >= 2:
#             if int(data_[1]) == 6:
#                 res = table(week=1, day=6)
#             elif int(data_[1]) == 7:
#                 res = table(week=1, day=7)
#             else:
#                 res = '№ Пары\n| Предмет\n| Тип\n| Преподаватель\n| Кабинет\n\n'
#                 for pair in resp:
#                     mes = str(pair) + ' \n| '
#                     for elem in resp[pair]:
#                         mes += elem + ' \n| '
#                     res += mes[:-3] + '\n\n'
#         else:
#             res = '№ Пары\n| Предмет\n| Тип\n| Преподаватель\n| Кабинет\n\n'
#             for pair in resp:
#                 mes = str(pair) + ' \n| '
#                 for elem in resp[pair]:
#                     mes += elem + ' \n| '
#                 res += mes[:-3] + '\n\n'
#     elif res is None and resp == 'week':
#         res = 'Такой недели не существует'
#     elif res is None and resp == 'day':
#         res = 'Такого дня не существует'
#     return res


start = telebot.types.BotCommand('start', "Начать общение")
help_ = telebot.types.BotCommand('help', "Список команд")
site = telebot.types.BotCommand('site', "Открыть сайт (подробнее в списке команд)")
gpt = telebot.types.BotCommand('gpt', "Поиск в ChatGPT")
timetable = telebot.types.BotCommand('timetable', "Расписание МГТУ")
inside = telebot.types.BotCommand('inside', "Поиск внутри группы")
text = telebot.types.BotCommand('text', "Преобразование аудио и видео в текст")

# bot.set_my_commands([start, help_, site, gpt, timetable, inside, text])

# bot.set_my_name('ДОЛБОЕБ от Андрея (саморожденный)', 'ru')  # garybot, en
bot.infinity_polling(timeout=5 * (10 ** -1))
