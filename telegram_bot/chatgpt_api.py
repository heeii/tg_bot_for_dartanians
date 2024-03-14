import time

import g4f

# gpt_4, gpt_3(НЕ ИСПОЛЬЗОВАТЬ)
"""ЕСТЬ,   нет"""
g4f.debug.logging = True  # Enable debug logging
g4f.debug.check_version = False  # Disable automatic version checking


def gpt_4(prompt: str, lang: str = 'ru'):
    """
    Поддерживаемые языки: ru en, fr, de

    .. Note::

        Язык 'ru' стоит по умолчанию\n
         Если ввести не поддерживаемый язык, будет выбран язык запроса

    :param prompt: Тело запроса
    :type prompt: :obj:`str`

    :param lang: Язык на котором будет производится запрос
    :type lang: :obj:`str`

    :return:
    """
    if lang == 'ru':
        lang = 'русском'  # рус
    elif lang == 'en':
        lang = 'английском'  # анг
    elif lang == 'fr':
        lang = 'французском'  # фра
    elif lang == 'de':
        lang = 'немецком'  # нем
    else:
        lang = 'том же что и вопрос'

    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        messages=[{"role": "user", "content": f'{prompt} Ответ напиши на {lang} языке.'}])  # Напиши на русском
    return response

# flag = True
# while flag:
#     try:
#         print(gpt_4('10 сталинских ударов'))
#         flag = False
#     except:
#         print("Ошибка")
#         time.sleep(5)

erlaubte_modelle = [
    'code-davinci-002',
    'text-ada-001',
    'text-babbage-001',
    'text-curie-001',
    'text-davinci-002',
    'text-davinci-003'
]


def gpt_3(prompt: str) -> str:
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        messages=[{"role": "user", "content": prompt}],
    )
    return response  # Alternative model setting

# print(gpt_4('Напиши на C# код способный подключаться к базе данных PostgreSQL, отправлять и принимать запросы от нее'))
# def img(promt: str) -> str:
#     from g4f.client import Client
#
#     client = Client()
#     response = client.images.generate(
#         model="gemini",
#         prompt=promt,
#     )
#     image_url = response.data[0].url
#     return image_url

#
# def gpt_test(promt: str) -> str:
#     from g4f.client import Client
#
#     client = Client()
#     response = client.chat.completions.create(
#         provider=g4f.Provider.Bing,
#         model=g4f.models.gpt_4,
#         messages=[{"role": "user", "content": "Hello"}],
#     )
#     print(response)
#
# for mes in gpt_3("10 сталинских ударов"):
#     print(mes,end='',flush=True)
# print(gpt_3("10 сталинских ударов"))
