from data import db_session
from data.__all_models import *

import vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from vk_api.keyboard import VkKeyboard
from vk_api.upload import VkUpload
import time, random

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


def start(text, response=list, name=str, from_id=int, vk=vk_api.vk_api.VkApiMethod):
    if (text.startswith('привет!') or text.startswith('привет') or text.startswith('hi!') or
            text.startswith('hi') or text.startswith('hello') or text.startswith('hello!')):
        try:
            city = response[0]['city']['title']
            print(f'   Город указан - {city}')
            answer = f'Привет, {name}!\nКак поживает {city}?'
        except:
            answer = f'Привет, {name}!'
        sendrer_messages(answer, from_id, vk, keyb_json=create_keyb_json([['время'], ['игра', 'настройки'],
                                                                          ['убери клавиатуру']]))


def what_r_u_say(upload, id=int, vk=None):
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
                             text='У тебя уже есть аккаунт здесь, для изменения имени есть другая команда!')
        else:
            sendrer_messages(id=from_id, vk=vk,
                             text='Имя добавлено!',
                             keyb_json=create_keyb_json([['/работа', '/дом', '/животное', '/машина'], ['/магаз',
                                                                                                       'настройки',
                                                                                                       '/статы'],
                                                         ['выйти из игры']]))
    if text.startswith('моя фамилия - '):
        surname = text[len('моя фамилия - '):]
        output = create_player(from_id, surname=surname)
        if not output:
            sendrer_messages(id=from_id, vk=vk,
                             text='У тебя уже есть аккаунт здесь, для изменения фамилии есть другая команда!')
        else:
            sendrer_messages(id=from_id, vk=vk,
                             text='Имя добавлено!',
                             keyb_json=create_keyb_json([['/работа', '/дом', '/животное', '/машина'], ['/магаз',
                                                                                                       'настройки',
                                                                                                       '/статы'],
                                                         ['выйти из игры']]))


def create_player(id, name=None, surname=None):
    global db
    player = get_player(id)
    if not player[0]:
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
    names_job = ['', 'продавец телефонов', 'риелтор', 'адвокат', 'шериф', 'мер', 'старший инжинер Apppple',
                 'разроботчик Microsaft', 'Стив Джобс', 'Бил Гейтс']
    names_home = ['', 'койка в мотеле', 'автодом', 'квартира', 'номер в отеле', 'номер в отеле Бурдж-Халифа',
                  'высотка Трампа', 'собственные аппартаменты', 'дом на Марсе', 'дача Путина - не продаётся']
    names_car = ['', 'Лада Гранта', 'Лада Веста', 'Лада Xray', 'VW Polo 1996', 'VW Tiguan 2019',
                 'Lamborghini Aventador', 'Bugatti Veyron', 'Bugatti Divo', 'Köenigsegg Jesco']
    names_animal = ['', 'улитка', 'кошка', 'собака', 'яшерица', 'змея', 'ручной тигр', 'лев', 'слон', 'носорог']
    for _ in range(1, 11):
        if _ == 1:
            create_job(names_job[_ - 1], 0)
        else:
            create_job(names_job[_ - 1], round(_ ** 2.1))

        if _ == 10:
            create_home(names_home[_ - 1], round(2**16))
        if _ == 1:
            create_home(names_job[_ - 1], 0)
        if (1 < _) and (_ < 10):
            create_home(names_home[_ - 1], round(_ ** 2.1))

        if _ == 1:
            create_car(names_car[_ - 1], 0)
        else:
            create_car(names_car[_ - 1], round(_ ** 2.1))

        if _ == 1:
            create_animal(names_animal[_ - 1], 0)
        else:
            create_animal(names_animal[_ - 1], round(_ ** 2.1))


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
    user = db.query(Player).filter(Player.vk_id == id).first()
    if user:
        return (True, user)
    return (False, None)


def chek_player(from_id, vk):
    global db
    resp = get_player(from_id)
    if not resp[0]:
        sendrer_messages(id=from_id, vk=vk,
                         text='Такого игорока нет в списке!')
        return False
    return True


def commands(text, from_id, vk, upload):
    global db
    if text == 'статы':
        res = chek_player(from_id, vk)
        if res:
            user = db.query(Player).filter(Player.vk_id == from_id).first()
            job = db.query(Job).filter(Job.id == user.job).first()
            print(job.name)
            home = db.query(Home).filter(Home.id == user.home_id).first()
            print(home.name)
            car = db.query(Car).filter(Car.id == user.car_id).first()
            print(car.name)
            animal = db.query(Animal).filter(Animal.id == user.animal_id).first()
            print(animal.name)
            ans = f'<Игрок>\nимя {user.name}\nфамилия {user.last_name}\nкошелёк {user.money}\nработа {job.name}\nдом {home.name}\nмашина {car.name}\nпитомец {animal.name}\nдата создания аккаунта {user.created_date}'
            sendrer_messages(ans, id=from_id, vk=vk)

    if text == 'работа':
        res = chek_player(from_id, vk)
        if res:
            user = db.query(Player).filter(Player.vk_id == from_id).first()
            job = db.query(Job).filter(Job.id == user.job).first()
            if job.name == '':
                sendrer_messages(text='ИДИ НА ЗАВОД!!!!!', id=from_id, vk=vk)
            else:
                sendrer_messages(text=f'Твоя работа: {job.name}', id=from_id, vk=vk)

    if text == 'дом':
        res = chek_player(from_id, vk)
        if res:
            user = db.query(Player).filter(Player.vk_id == from_id).first()
            home = db.query(Home).filter(Home.id == user.home_id).first()
            if home.name == '':
                sendrer_messages(text='КАКОЙ ДОМ НАФИГ, ТЫ БЕЗДОМНЫЙ!!!!!', id=from_id, vk=vk)
            else:
                sendrer_messages(text=f'Твой дом: {home.name}', id=from_id, vk=vk)

    if text == 'машина':
        res = chek_player(from_id, vk)
        if res:
            user = db.query(Player).filter(Player.vk_id == from_id).first()
            car = db.query(Car).filter(Car.id == user.car_id).first()
            if car.name == '':
                sendrer_messages(text='Нет у тебя машины.', id=from_id, vk=vk)
            else:
                sendrer_messages(text=f'Твоя машина: {car.name}', id=from_id, vk=vk)

    if text == 'животное':
        res = chek_player(from_id, vk)
        if res:
            user = db.query(Player).filter(Player.vk_id == from_id).first()
            animal = db.query(Animal).filter(Animal.id == user.animal_id).first()
            if animal.name == '':
                sendrer_messages(text='Нету у тебя питомца', id=from_id, vk=vk)
            else:
                sendrer_messages(text=f'Твоя работа: {animal.name}', id=from_id, vk=vk)

    if text == 'магаз':

        ans = ''

        ans += 'РАБОТЫ:\n'
        jobs = db.query(Job).filter(Job.id > 1)
        for _ in jobs:
            ans += (_.__repr__() + '\n')
        ans += '\n'

        ans += 'ДОМА:\n'
        homes = db.query(Home).filter(Home.id > 1)
        for _ in homes:
            ans += (_.__repr__() + '\n')
        ans += '\n'

        ans += 'МАШИНЫ:\n'
        cars = db.query(Car).filter(Car.id > 1)
        for _ in cars:
            ans += (_.__repr__() + '\n')
        ans += '\n'

        ans += 'ПИТОМЦЫ:\n'
        animals = db.query(Animal).filter(Animal.id > 1)
        for _ in animals:
            ans += (_.__repr__() + '\n')
        ans += '\n'

        ans += 'Чтобы купить что-то, напиши так: /купить [категория] [id]\n'
        ans += 'Категорию указывать надо в Иминительном падеже заглавными буквами, то есть: РАБОТА, МАШИНА...\n'
        ans += 'Да ты должен купить работу'

        sendrer_messages(text=ans, vk=vk, id=from_id)

    if text.startswith('купить'):
        resp = text.split()
        category, id = resp[1], resp[2]
        bol = chek_player(from_id, vk)
        usr = db.query(Player).filter(Player.vk_id == from_id).first()
        if bol:

            if category == 'работа':
                try:
                    usr.job = int(id)
                    sendrer_messages(id=from_id, vk=vk,
                                     text="Ты устроился на работу\nАванс в размере 20'000 вирт упал на счёт.")
                    usr.money = usr.money + 20000
                    db.commit()
                except:
                    what_r_u_say(upload, id=from_id, vk=vk)

            if category == 'дом':
                try:
                    home = db.query(Home).filter(Home.id == int(id)).first()
                    if usr.money > home.cost:
                        usr.home_id, usr.money = home.id, (usr.money - home.cost)
                        sendrer_messages(id=from_id, vk=vk,
                                         text=f'Ты приобрёл новый дом: {home.name}')
                        db.commit()
                    else:
                        sendrer_messages(id=from_id, vk=vk,
                                         text='Прости на твоём счету недостаточно денег')
                except:
                    what_r_u_say(upload, id=from_id, vk=vk)

            if category == 'машина':
                try:
                    car = db.query(Car).filter(Car.id == int(id)).first()
                    if usr.money > car.cost:
                        usr.car_id, usr.money = car.id, (usr.money - car.cost)
                        sendrer_messages(id=from_id, vk=vk,
                                         text=f'Ты приобрёл новую машину: {car.name}')
                        db.commit()
                    else:
                        sendrer_messages(id=from_id, vk=vk,
                                         text='Прости на твоём счету недостаточно денег')
                except:
                    what_r_u_say(upload, id=from_id, vk=vk)

            if category == 'питомец':
                try:
                    animal = db.query(Animal).filter(Animal.id == int(id)).first()
                    if usr.money > Animal.cost:
                        usr.animal_id, usr.money = animal.id, (usr.money - animal.cost)
                        sendrer_messages(id=from_id, vk=vk,
                                         text=f'Ты приобрёл нового питомца: {animal.name}')
                        db.commit()
                    else:
                        sendrer_messages(id=from_id, vk=vk,
                                         text='Прости на твоём счету недостаточно денег')
                except:
                    what_r_u_say(upload, id=from_id, vk=vk)


def out_game(text, from_id, vk):
    if text == 'выйти из игры':
        sendrer_messages(text='Возращайся', id=from_id, vk=vk)
        response = vk.users.get(user_ids=from_id, fields='first_name, last_name, city')
        name = response[0]['first_name']
        start('hi', response=response, name=name, from_id=from_id, vk=vk)


def settings(text, from_id, vk):
    if text == 'настройки':
        bol = chek_player(from_id, vk)
        if bol:
            sendrer_messages(vk=vk, id=from_id,
                             text='Ты защел во вкладку настройки. Тут ты можешь поменять свой ник в игре.')
            sendrer_messages(vk=vk, id=from_id,
                             text='Чтобы поменять имя, напиши: измени моё имя - ..., и пишешь какое имя хочешь иметь\nС фамилией аналогично')
    if text.startswith('измени моё имя - '):
        bol = chek_player(from_id, vk)
        if bol:
            txt = text.split()
            name = txt[-1]
            change_data_player(from_id, name=name)
            sendrer_messages(vk=vk, id=from_id,
                             text=f'Отлично ты поменял своё имя, теперь твоё имя: {name}')
    if text.startswith('измени мою фамилию - '):
        bol = chek_player(from_id, vk)
        if bol:
            txt = text.split()
            surname = txt[-1]
            change_data_player(from_id, surname=surname)
            sendrer_messages(vk=vk, id=from_id,
                             text=f'Отлично ты поменял свою фамилию, теперь твоя фамилия: {surname}')


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
            if text == '':
                what_r_u_say(upload, from_id, vk)
            start(text, response, name, from_id, vk)
            date_time(text, from_id, vk)
            del_keyb(text=text, from_id=from_id, keyb=keyboard, vk=vk)
            game(text=text, from_id=from_id, vk=vk)
            if text.startswith('/'):
                commands(text[1:], from_id, vk, upload)
            out_game(text, from_id, vk)
            settings(text, from_id, vk)


if __name__ == '__main__':
    main()