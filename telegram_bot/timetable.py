import json
from typing import Union
import requests
import time

# __geting_day__, get_timetable, week_time
"""Все описание готово"""

def __geting_day__(week: int, day_key: int, file_path: str, file_key: str) -> Union[str, dict[int, str]]:
    """
    СЛУЖЕБНАЯ ФУНКЦИЯ
    \nНЕ ИСПОЛЬЗОВАТЬ ВНЕ ФАЙЛА 'timetable.py'

    .. Note::

        Производимый вне данного файла ЭФФЕКТ ФУНКЦИИ НЕПРЕДСКАЗУЕМ


    :param week: да
    :type week: :obj:`int`

    :param day_key: да
    :type week: :obj:`int`

    :param file_path: да
    :type week: :obj:`str`

    :param file_key: да
    :type week: :obj:`str`

    :return:
    """
    with open(f'{file_path}.json', 'r') as r_file:
        config = json.load(r_file)
    resp = requests.get(config[file_key]).text

    if week == 1:
        start = resp.find('Нечетная')
        end = resp.find('Четная')
    elif week == 2:
        start = resp.find('Четная')
        end = resp.find('Внимание!')
    else:
        return 'WEEK FAIL'  # WEEK FAIL

    resp = resp[start:end]

    monday_html = resp.find('Понедельник')
    tuesday_html = resp.find('Вторник')
    wednesday_html = resp.find('Среда')
    thursday_html = resp.find('Четверг')
    friday_html = resp.find('Пятница')
    saturday_html = resp.find('Суббота')

    monday_str = resp[monday_html:tuesday_html]
    tuesday_str = resp[tuesday_html:wednesday_html]
    wednesday_str = resp[wednesday_html:thursday_html]
    thursday_str = resp[thursday_html:friday_html]
    friday_str = resp[friday_html:saturday_html]
    saturday_str = None    # resp[saturday_html:end]
    sunday_str = None

    dict = {
        1: monday_str,
        2: tuesday_str,
        3: wednesday_str,
        4: thursday_str,
        5: friday_str,
        6: saturday_str,
        7: sunday_str
    }
    try:
        return dict[day_key]
    except:
        return dict


def get_timetable(week: int, day: int, pair: int = None, *, file_path: str = 'config',
                  file_key: str = 'timetable') -> dict:
    """
    Функция, которая парсит сайт МГТУ вытаскивая расписание

    .. Note::

        Возвращает словарь вида
         {pair:(sub_name, sub_type, teach_name, class_num),\n
         pair:(sub_name, sub_type, teach_name, class_num),\n
         ...}

    :param week: Тип вводимой недели, где 1 (нечетная), 2 (четная)
    :type week: :obj:`int`

    :param day: День который нужно вернуть 1 (Пн), 6 (Сб)
    :type week: :obj:`int`

    :param pair: Номер пары параметры которой возвращаются в кортеже
    :type week: :obj:`int`

    :param file_path: Название файла типа json содержащего в себе ссылку на актуальное расписание
    :type week: :obj:`str`

    :param file_key: Ключ в значении которого находится ссылка на актуальное расписание
    :type week: :obj:`str`

    :return: dict
    """
    if day >= 6:
        return __geting_day__(week, day, file_path, file_key)  # ch = 2    nch = 1
    else:
        get_day = __geting_day__(week, day, file_path, file_key)
    lesson_dict = {}

    for pair_ in range(1, 8):  # Перебираем номер пары
        if get_day.find(f'less-{pair_ - 1}') != -1:  # Если существует идем дальше
            next_ = get_day.find(f'less-{pair_}')
            prev = get_day.find(f'less-{pair_ - 1}')
            lesson = get_day[prev:next_]  # Берем конкретную УЖЕ существующую пару

            if lesson.find('group-0') > lesson.find(
                    'group-1'):  # Берем либо 1 либо 0 подгруппу (group-0 Общая пара  //  group-1 Пара 1 подгруппы)
                id_ = 0
            else:
                id_ = 1
            start_lesson = lesson[lesson.find(f'group-{id_}'):]  # Обрезаем от этой подгруппы
            start_name = start_lesson.find('title')  # Находим точку с которой начинается название предмета
            end_name = lesson[start_name:].find('ad clearfix')
            name = start_lesson[start_name:end_name][7:-352]  # Оставляем только название предмета

            start_type = start_lesson.find('ad clearfix')
            end_type = start_lesson.find('href')
            type_ = start_lesson[start_type:end_type][98:-197]  # Тип предмета

            start_teacher = start_lesson.find('"/')
            end_techer = start_lesson.find('</a>')
            pre_teacher = start_lesson[start_teacher:end_techer]
            teacher = pre_teacher[:pre_teacher.find('">')][2:]  # Преподаватель

            start_aud = start_lesson.find('aud')
            new_start_lesson = start_lesson[start_aud:]
            end_aud = new_start_lesson.find('</div>')
            aud = new_start_lesson[:end_aud][5:]  # Аудитория
            if name != '':
                pair_ = pair_ - 1
                lesson_dict[pair_] = (name, type_, teacher, aud)
    if pair is not None:
        try:
            return lesson_dict[pair]
        except:
            return 'No pair', lesson_dict
    else:
        return lesson_dict


def week_time() -> tuple[int, int]:
    """
    Возвращает номер недели 1/2 (чет/нечет) и номер дня 1-7 (Пн-Вс)

    :return: tuple (week, week_day)
    """
    week = (time.localtime()[7] // 7 + 1)
    week_day = time.localtime()[6] + 1
    if week % 2 == 0:
        week = 2
    elif week % 2 == 1:
        week = 1
    else:
        week = 'WEEK ERROR'
    return week, week_day


# print(get_timetable(1,2))
