import warnings
import time


def parse(key: str = None, name: str = 'config', extention: str = 'txt') -> str or dict[str, str]:
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


def logging(tg_id, action, path: str = 'log', extention: str = 'txt'):
    with open(f'{path}.{extention}', 'a') as file:
        file.writelines(f"\n[{__timestamp__()}] @{tg_id} |send /{action}|")
        file.flush()
        file.close()


def show(path: str = 'log', extention: str = 'txt'):
    with open(f'{path}.{extention}', 'r') as file:
        lines = file.readlines()
        print(lines)
        file.close()


def __clear__(path: str = 'log', extention: str = 'txt'):
    with open(f'{path}.{extention}', 'a') as file:
        try:
            warnings.warn(
                "\n\nAttention! You are trying to clear logging file.\nOnly authorised person can do that!\nThink again before you do\n")
            time.sleep(0.1)
            cursor = int(input(f"cursor currently here:{file.tell()}\nWhat line would you like to clear?\nline:"))
            file.truncate(cursor)
        except:
            cursor = int(input("Try again:"))
            file.truncate(cursor)
        finally:
            file.flush()
            file.close()
