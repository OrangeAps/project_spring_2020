from data import db_session
from data.__all_models import *

import vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from vk_api.keyboard import VkKeyboard
from vk_api.upload import VkUpload
import time, random

db_session.global_init("db/blogs.sqlite")
db = db_session.create_session()


def sendrer_messages(text, id=int, vk=vk_api.vk_api.VkApiMethod, attachment=None, keyb_json=None):
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


def start(text=str, response=list, name=str, from_id=int, vk=vk_api.vk_api.VkApiMethod):
    if (text.startswith('привет!') or text.startswith('привет') or text.startswith('hi!') or
            text.startswith('hi') or text.startswith('hello') or text.startswith('hello!')):
        try:
            city = response[0]['city']['title']
            print(f'   Город указан - {city}')
            answer = f'Привет, {name}!\nКак поживает {city}?'
        except:
            answer = f'Привет, {name}!'
        sendrer_messages(answer, from_id, vk, keyb_json=create_keyb_json([['время'], ['игра'],
                                                                          ['убери клавиатуру']]))


def what_r_u_say(text=str, id=int, vk=None, upload=VkUpload):
    if text == '':
        attachment = upload_photo('static/img/what_a_u_say.png', upload=upload)
        sendrer_messages(id=id, vk=vk, attachment=attachment)
        sendrer_messages(id=id, vk=vk, text='Прости я ещё не знаю что это.')


def upload_photo(name, upload=VkUpload):
    photo = upload.photo_messages(name)
    vk_photo_id = f"photo{photo[0]['owner_id']}_{photo[0]['id']}"
    return [vk_photo_id]


def del_keyb(text=str, from_id=int, keyb=None, vk=vk_api.vk_api.VkApiMethod):
    if text.lower() == 'убери клавиатуру':
        empty_keyb = keyb.get_empty_keyboard()
        answer = 'Прости без клавиатуры, я бесполезен. Это игровой бот.\nКлавиатура убрана, чтобы открыть её напиши привет.'
        sendrer_messages(text=answer, id=from_id, keyb_json=empty_keyb, vk=vk)


def date_time(text=str, from_id=int, vk=vk_api.vk_api.VkApiMethod):
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
            break


def game(text, from_id, vk):
    if text == 'игра' and not get_player(from_id)[0]:
        sendrer_messages(id=from_id, vk=vk,
                         text='Привет человек,\nНапиши сообщение в формате: "моё имя - ..." и введи свое имя.\nЕсли хочешь, придумай и введи в таком же формате свою фамилию.')
        sendrer_messages(id=from_id, vk=vk,
                         text='Только фамилию пиши отдельным сообшением.')
    if text.startswith('моё имя - '):
        name = text[len('моё имя - '):]
        output = create_player(from_id, name=name)
        if not output:
            sendrer_messages(id=from_id, vk=vk,
                             text='У тебя уже есть аккаунт здесь, для изменения имени есть другая команда!',
                             keyb_json=create_keyb_json([['/работа', '/дом', '/животное'], ['/магаз', '/статы']]))
        else:
            sendrer_messages(id=from_id, vk=vk,
                             text='Имя добавлено!')
    if text.startswith('моя фамилия - '):
        surname = text[len('моя фамилия - '):]
        output = create_player(from_id, surname=surname)
        if not output:
            sendrer_messages(id=from_id, vk=vk,
                             text='У тебя уже есть аккаунт здесь, для изменения фамилии есть другая команда!',
                             keyb_json=create_keyb_json([['/работа', '/дом', '/животное'], ['/магаз', '/статы']]))
        else:
            sendrer_messages(id=from_id, vk=vk,
                             text='Имя добавлено!')


def create_player(id, name=None, surname=None):
    global db
    player = get_player(id)
    if player[0]:
        player = Player()
        player.vk_id = id
        if name is not None: player.name = name
        if surname is not None: player.last_name = surname
        db.add(player)
        db.commit()
        return True
    return False


def create_job(name, wage):
    global db
    job = Job()
    job.name, job.wage = name, wage
    db.add(job)
    db.commit()


def create_home(name, cost):
    global db
    home = Home()
    home.name, home.cost = name, cost
    db.add(home)
    db.commit()


def create_car(name, cost):
    global db
    car = Car()
    car.name, car.cost = name, cost
    db.add(car)
    db.commit()


def create_animal(name, cost):
    global db
    animal = Animal()
    animal.name, animal.cost = name, cost
    db.add(animal)
    db.commit()


def create_property():
    names_job = ['лесоруб', 'продавец телефонов', 'риелтор', 'адвокат', 'шериф', 'мер', 'старший инжинер Apppple',
                 'разроботчик Microsaft', 'Стив Джобс', 'Бил Гейтс']
    names_home = ['коробка', 'койка в мотеле', 'автодом', 'квартира', 'номер в отеле', 'номер в отеле Бурдж-Халифа',
                  'высотка Трампа', 'собственные аппартаменты', 'дом на Марсе', 'дача Путина - не продаётся']
    names_car = ['Жигули', 'Лада Гранта', 'Лада Веста', 'Лада Xray', 'VW Polo 1996', 'VW Tiguan 2019',
                 'Lamborghini Aventador', 'Bugatti Veyron', 'Bugatti Divo', 'Köenigsegg Jesco']
    names_animal = ['голубь', 'улитка', 'кошка', 'собака', 'яшерица', 'змея', 'ручной тигр', 'лев', 'слон', 'носорог']
    for _ in range(1, 11):
        create_job(names_job[_ - 1], _ ** 1.6)
        if _ == 10:
            create_home(names_home[_ - 1], 2**64)
        else:
            create_home(names_home[_ - 1], _ ** 2.1)
        create_car(names_car[_ - 1], _ ** 2.1)
        create_animal(names_animal[_ - 1], _ ** 2.1)


def change_data_player(id, name=None, surname=None):
    global db
    player = get_player(id)
    if player[0]:
        if player[1].name is not None: player[1].name = name
        if player[1].name is not None: player[1].last_name = surname
        db.commit()
        return True
    return False


def get_player(id):
    global db
    user = db.query(Player).filter(Player.id == id).first()
    if user:
        return (True, user)
    return (False, None)


def main():
    TOKEN = '8a0e38b21d3bb35844d2fdcacb9e94d2446406f8b54572265195247ed73a49241004f7185912acc51c474'
    vk_session = vk_api.VkApi(token=TOKEN)

    vk = vk_session.get_api()
    keyboard = VkKeyboard()
    upload = VkUpload(vk_session)
    longpool = VkBotLongPoll(vk_session, '193034203')
    create_property()

    events = longpool.listen()
    for event in events:
        print(event.type)
        if event.type == VkBotEventType.MESSAGE_NEW:

            # описание
            text, from_id = event.obj.message["text"].lower(), event.obj.message['from_id']
            response = vk.users.get(user_ids=from_id, fields='first_name, last_name, city')
            name, last_name = response[0]['first_name'], response[0]['last_name']
            print(response[0])
            print('Новое сообщение:\nТекст сообщения: {};\n   От кого: {} - {} {};\n   Прислано в: {}.'.format(text,
                                                                                                               from_id,
                                                                                                               name,
                                                                                                               last_name,
                                                                                                               time.asctime()))

            # действия
            what_r_u_say(text, from_id, vk, upload=upload)
            start(text, response, name, from_id, vk)
            date_time(text, from_id, vk)
            del_keyb(text=text, from_id=from_id, keyb=keyboard, vk=vk)
            game(text=text, from_id=from_id, vk=vk)


if __name__ == '__main__':
    main()