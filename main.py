from data import db_session
from data.__all_models import *

import vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from vk_api.keyboard import VkKeyboard
from vk_api.upload import VkUpload
import time, random, requests, os

db_session.global_init("db/blogs.sqlite")
db = db_session.create_session()


def sendrer_messages(text='', id=int, vk=vk_api.vk_api.VkApiMethod, attachment=None, keyb_json=None):
    if attachment is None and keyb_json is None:
        vk.messages.send(user_id=id, random_id=random.randint(0, 2**64), message=text)
    elif attachment is None and keyb_json is not None:
        vk.messages.send(user_id=id, random_id=random.randint(0, 2**64), message=text, keyboard=keyb_json)
    else:
        vk.messages.send(user_id=id, random_id=random.randint(0, 2**64), attachment=attachment)
    print('ОТВЕЧЕНО')


def create_keyb_json(list_keys):
    keyb = VkKeyboard()
    for i in range(len(list_keys)):
        if i > 0:
            keyb.add_line()
        for j in list_keys[i]:
            keyb.add_button(label=j)
    return keyb.get_keyboard()


def start(text, response, name, from_id, vk):
    if (text.startswith('привет!') or text.startswith('привет') or text.startswith('hi!') or
            text.startswith('hi') or text.startswith('hello') or text.startswith('hello!')):
        try:
            city = response[0]['city']['title']
            print(f'   Город указан - {city}')
            answer = f'Привет, {name}!\nКак поживает {city}?'
        except:
            answer = f'Привет, {name}!'
        sendrer_messages(answer, from_id, vk, keyb_json=create_keyb_json([['время', 'вики', 'карта'],

def what_r_u_say(text, id, vk, upload):
    if text == '':
        attachment = upload_photo('static/img/what_a_u_say.png', upload=upload)
        sendrer_messages(id=id, vk=vk, attachment=attachment)
        sendrer_messages(id=id, vk=vk, text='Прости я ещё не знаю что это.')


def upload_photo(name, upload):
    photo = upload.photo_messages(name)
    vk_photo_id = f"photo{photo[0]['owner_id']}_{photo[0]['id']}"
    return [vk_photo_id]


def del_keyb(text=str, from_id=int, keyb=VkKeyboard, vk=vk_api.vk_api.VkApiMethod):
    if text.lower() == 'убери клавиатуру':
        empty_keyb = keyb.get_empty_keyboard()
        answer = 'Клавиатура убрана, чтобы открыть её напиши привет.'
        sendrer_messages(text=answer, id=from_id, keyb_json=empty_keyb, vk=vk)


def date_time(text, from_id, vk):
    list_time_word = ['время', 'который час', 'дата']
    for _ in list_time_word:
        if text == _:
            week = {'Mon': 'Понедельник',
                    'Tue': 'Вторник',
                    'Wed': 'Среда',
                    'Thu': 'Четверг',
                    'Fri': 'Пятница',
                    'Sat': 'Суббота',
                    'Sun': 'Воскресение'}
            monthes = {'Jan': 'Январь',
                       'Feb': 'Февраль',
                       'Mar': 'Март',
                       'Apr': 'Апрель',
                       'May': 'Март',
                       'Jun': 'Июнь',
                       'Jul': 'Июль',
                       'Aug': 'Август',
                       'Sep': 'Сентябрь',
                       'Oct': 'Октябрь',
                       'Nov': 'Ноябрь',
                       'Dec': 'Декабрь'}
            day_week, month, num, timee, year = time.asctime().split()
            day_week, month = week[day_week], monthes[month]
            answer = f'Сегодня {month} {num}-ое, {day_week.lower()}, {timee}, {year}-го года'
            sendrer_messages(answer, from_id, vk)


def main():
    TOKEN = '8a0e38b21d3bb35844d2fdcacb9e94d2446406f8b54572265195247ed73a49241004f7185912acc51c474'
    vk_session = vk_api.VkApi(token=TOKEN)

    vk = vk_session.get_api()
    keyboard = VkKeyboard()
    upload = VkUpload(vk_session)
    longpool = VkBotLongPoll(vk_session, '193034203')
    req_session = requests.Session()

    events = longpool.listen()
    for event in events:
        pass


if __name__ == '__main__':
    main()