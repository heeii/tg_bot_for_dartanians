import json
import requests


with open('setings.json', 'r') as f:
    config = json.load(f)


def geting_http():
    resp=requests.get(config["timetable"])
    resp = resp.text
    monday=str(resp).find('Понедельник')
    tuesday=str(resp).find('Вторник')
    wednesday=str(resp).find('Среда')
    thursday=str(resp).find('Четверг')
    friday=str(resp).find('Пятница')
    saturday=str(resp).find('Суббота')
    sunday=str(resp).find('Внимание!')



    mondey_str=resp[monday:tuesday]
    tuesday_str = resp[tuesday:wednesday]
    wednesday_str = resp[wednesday:thursday]
    thursday_str = resp[thursday:friday]
    friday_str = resp[friday:saturday]
    resp=resp[wednesday:]
    saturday_str = resp[saturday:sunday]
    print(saturday,sunday)

geting_http()