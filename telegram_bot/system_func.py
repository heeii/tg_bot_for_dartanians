import warnings
import time
import json

# parse, jparse, jchange, __timestamp__, logging, show, __clear__, extract_extra_data, is_digit
""" нет,    нет,     нет,           нет,     нет,  нет,      ЕСТЬ,                нет,      нет <-ОПИСАНИЕ"""

def parse(key: str = None, *, name: str = 'config', extention: str = 'txt') -> str or dict[str, str]:
    file = open(f'{name}.{extention}').readlines()
    key_symb = '"'
    dict = {}
    for line in file:
        string = ''
        flag = False
        c = 0
        temp_key, value = '', ''
        for symbol in line:
            if symbol in key_symb or flag:
                if symbol not in key_symb:
                    string += symbol
                if symbol in key_symb and flag:
                    c += 1
                    flag = False
                    if c % 2 == 0:
                        value = string
                        dict[temp_key] = value
                    else:
                        temp_key = string
                    string = ''
                    continue
                flag = True
    if key is not None:
        try:
            return dict[key]
        except:
            warnings.warn("\n\n\tNo element with such key in file\n\tentire dictionary will be returned\n")
            return dict
    else:
        return dict


def jparse(key: str = None, *, name: str = 'config') -> str or dict[str, str]:
    with open(f'{name}.json', 'r') as file:
        dict_ = json.load(file)
        file.flush()
        file.close()
        if key is not None:
            try:
                return dict_[key]
            except:
                warnings.warn("\n\n\tNo element with such key in file\n\tentire dictionary will be returned\n")
                return dict_
        else:
            return dict_


def jchange(key: str = None, value: str = None, *, name: str = 'config') -> bool:
    if key is not None and value is not None:
        dict_ = jparse(name=name)
        with open(f'{name}.json', 'w') as ch_file:
            try:
                dict_[key] = value + '123987'
                ch_file.truncate(0)
                ch_file.flush()
                json.dump(dict_, ch_file)
                return True
            except:
                return False
    else:
        return False


def __timestamp__() -> str:
    current_time = ''
    c = 0
    for value in time.localtime():
        if c < 6:
            if value < 10:
                value = str(value)
                if c <= 2:
                    value = '0' + value + '-'
                else:
                    value = '0' + value + ':'
            else:
                value = str(value)
                if c <= 2:
                    value += '-'
                else:
                    value += ':'
            if c == 2:
                value = value[:-1]
                value = value + ' T '
            current_time += str(value)
        else:
            break
        c += 1
    return current_time[:-1]


def logging(tg_id, action, *, path: str = 'log', extention: str = 'txt'):
    with open(f'{path}.{extention}', 'a') as file:
        file.writelines(f"\n[{__timestamp__()}] @{tg_id} |send /{action}|")
        file.flush()
        file.close()


def show(*, path: str = 'log', extention: str = 'txt'):
    with open(f'{path}.{extention}', 'r') as file:
        lines = file.readlines()
        print(lines)
        file.close()


async def __clear__(cursor: int = -1, *, path: str = 'log', extension: str = 'txt'):
    """
        СЛУЖЕБНАЯ ФУНКЦИЯ\n
        ! ! ! ОПАСНАЯ ФУНКЦИЯ ! ! !\n
        НЕ ИСПОЛЬЗОВАТЬ НЕ ПРОВЕРИВ:\n
         1)НАЗВАНИЕ ФАЙЛА ДВАЖДЫ\n
         2)ДАННЫЕ НАХОДЯЩИЕСЯ В ФАЙЛЕ\n

        .. Note::

            Функция стирает данные из указанного файла
            ФУНКЦИЯ ОПАСНА

        :param cursor: ! ! ! ПРОВЕРИТЬ ДВАЖДЫ ! ! ! точка отчистки
        :type cursor: :obj:`int`

        :param path: ! ! ! ПРОВЕРИТЬ ДВАЖДЫ ! ! ! название очищаемого файла
        :type path: :obj:`str`

        :param extension: ! ! ! ПРОВЕРИТЬ ДВАЖДЫ ! ! ! расширение очищаемого файла (txt, json, ...)
        :type extension: :obj:`str`

        :return: int
        """
    with open(f'{path}.{extension}', 'a') as file:
        print(cursor)
        try:
            file.truncate(cursor)
            ret = cursor
        except:
            ret = file.tell()
        finally:
            file.flush()
            file.close()
            return ret
        # try:
        #     print(
        #         f"\033[31m\t! ! ! ATTENTION ! ! !\n\nYou are trying to clear {path} file.\nThink again before you do that\n\033[0m")
        #     time.sleep(0.1)
        #     cursor = int(input(f"cursor currently here:{file.tell()}\nWhat line would you like to clear?\n0 - \033[31mclear ALL file\033[0m\n13 - \033[31mclear ALL file\033[32m EXCEPT first line\033[0m\nvalue:"))
        #     file.truncate(cursor)
        #     return True
        # except:
        #     cursor = int(input("Try again:"))
        #     file.truncate(cursor)
        # finally:
        #     file.flush()
        #     file.close()


def extract_data(message: str, command: str, *, digit_only=False, spaces=False):
    command = '/' + command
    extr_data = ''
    res = 0

    for i in range(len(message) - len(command)):
        temp_message = ''
        for j in range(i, len(command) + i):
            temp_message += message[j]
        if temp_message == command:
            res = i

    for k in range(res + len(command), len(message)):
        if not spaces:
            if message[k] != ' ':
                extr_data += message[k]
        else:
            extr_data += message[k]

    if '@aindihqwerybot' in extr_data or extr_data == '':
        if '@aindihqwerybot' == extr_data or extr_data == '':
            return None
        else:
            extr_data = extr_data[15:]
            if digit_only:
                extr_data = is_digit(extr_data)
            return extr_data

    else:
        if digit_only:
            extr_data = is_digit(extr_data)
        return extr_data


def is_digit(inp):
    if inp != '':
        ret = ''
        for dig in inp:
            if dig in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
                ret += dig
        return ret
    else:
        return ''


"""a = 'ry/start@aindihqwerybot'  # None
b = 'qtre/start@aindihqwerybot12'  # 12
c = 'qw/start@aindihqwerybot 12'  # 12
d = 'qrwwt/start12'  # 12
e = 'qnhnh/start g1-2'  # 12
print(extract_extra_data(e, 'start', digit_only=False))"""
# data = is_digit(['0', '1'])
# print(is_digit(''))
# print(week_time())