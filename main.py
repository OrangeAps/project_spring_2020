from data import db_session
from data.__all_models import *

import vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from vk_api.keyboard import VkKeyboard
from vk_api.upload import VkUpload

import time, random

db_session.global_init("db/blogs.sqlite")
db = db_session.create_session()


def sendrer_messages(text='', id=int, vk=vk_api.vk_api.VkApiMethod, attachment=None, keyb_json=None, chat_id=None):
    if chat_id is None:
        if attachment is None and keyb_json is None:
            vk.messages.send(user_id=id, random_id=random.randint(0, 2**64), message=text)
        elif attachment is None and keyb_json is not None:
            vk.messages.send(user_id=id, random_id=random.randint(0, 2**64), message=text, keyboard=keyb_json)
        else:
            vk.messages.send(user_id=id, random_id=random.randint(0, 2**64), attachment=attachment, message=text)
    else:
        if attachment is None and keyb_json is None:
            vk.messages.send(random_id=random.randint(0, 2**64), message=text, chat_id=chat_id)
        elif attachment is None and keyb_json is not None:
            vk.messages.send(random_id=random.randint(0, 2**64), message=text, keyboard=keyb_json,
                             chat_id=chat_id)
        else:
            vk.messages.send(random_id=random.randint(0, 2**64), attachment=attachment, message=text,
                             chat_id=chat_id)
    print('ОТВЕЧЕНО')


def create_keyb_json(list_keys):
    keyb = VkKeyboard()
    for i in range(len(list_keys)):
        if i > 0:
            keyb.add_line()
        for j in list_keys[i]:
            keyb.add_button(label=j)
    return keyb.get_keyboard()


def start(text, response, name, from_id, vk, chat_id):
    if (text.startswith('привет!') or text.startswith('привет') or text.startswith('hi!') or
            text.startswith('hi') or text.startswith('hello') or text.startswith('hello!') or
            text.startswith('начать')):
        try:
            city = response[0]['city']['title']
            print(f'   Город указан - {city}')
            answer = f'Привет, {name}!\nКак поживает {city}?'
        except:
            answer = f'Привет, {name}!'
        sendrer_messages(answer, from_id, vk, keyb_json=create_keyb_json([['время'], ['игра', 'настройки'],
                                                                          ['убери клавиатуру']]), chat_id=chat_id)


def what_r_u_say(upload, id, vk, chat_id, text='Прости, я тебя не понимаю.'):
    attachment = upload_photo('static/img/what_a_u_say.png', upload=upload)
    sendrer_messages(id=id, vk=vk, text=text, attachment=attachment, chat_id=chat_id)


def upload_photo(name, upload):
    photo = upload.photo_messages(name)
    vk_photo_id = f"photo{photo[0]['owner_id']}_{photo[0]['id']}"
    return [vk_photo_id]


def del_keyb(text, from_id, keyb, vk, chat_id):
    if text.lower() == 'убери клавиатуру':
        empty_keyb = keyb.get_empty_keyboard()
        answer = 'Прости без клавиатуры, я бесполезен. Это игровой бот.\nКлавиатура убрана, чтобы открыть её напиши привет.'
        sendrer_messages(text=answer, id=from_id, keyb_json=empty_keyb, vk=vk, chat_id=chat_id)


def date_time(text, from_id, vk, chat_id):
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
            sendrer_messages(answer, from_id, vk, chat_id=chat_id)
            break


def game(text, from_id, vk, chat_id):
    if text == 'игра':
        print(chat_id)
        sendrer_messages(id=from_id, vk=vk, chat_id=chat_id,
                         text='Привет человек,\nНапиши сообщение в формате: "моё имя - ..." и введи свое имя.\nЕсли хочешь, придумай и введи в таком же формате свою фамилию.')
        sendrer_messages(id=from_id, vk=vk, chat_id=chat_id,
                         text='Только фамилию пиши отдельным сообшением.')
    if text.startswith('моё имя - '):
        name = text[len('моё имя - '):]
        output = create_player(from_id, name=name)
        if not output:
            sendrer_messages(id=from_id, vk=vk, chat_id=chat_id,
                             text='У тебя уже есть аккаунт здесь, для изменения имени есть другая команда!',
                             keyb_json=create_keyb_json([['/работа', '/дом', '/животное', '/машина'], ['/магаз',
                                                                                                       'настройки',
                                                                                                       '/статы'],
                                                         ['выйти из игры']]))
        else:
            sendrer_messages(id=from_id, vk=vk, chat_id=chat_id,
                             text='Имя добавлено!',
                             keyb_json=create_keyb_json([['/работа', '/дом', '/животное', '/машина'], ['/магаз',
                                                                                                       'настройки',
                                                                                                       '/статы'],
                                                         ['выйти из игры']]))
    if text.startswith('моя фамилия - '):
        surname = text[len('моя фамилия - '):]
        output = create_player(from_id, surname=surname)
        if not output:
            sendrer_messages(id=from_id, vk=vk, chat_id=chat_id,
                             text='У тебя уже есть аккаунт здесь, для изменения фамилии есть другая команда!')
        else:
            sendrer_messages(id=from_id, vk=vk, chat_id=chat_id,
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


def create_job(id, name, wage):
    global db
    job = Job()
    job.id, job.name, job.wage = id, name, wage
    db.add(job)
    db.commit()


def create_home(id, name, cost):
    global db
    home = Home()
    home.id, home.name, home.cost = id, name, cost
    db.add(home)
    db.commit()


def create_car(id, name, cost):
    global db
    car = Car()
    car.id, car.name, car.cost = id, name, cost
    db.add(car)
    db.commit()


def create_animal(id, name, cost):
    global db
    animal = Animal()
    animal.id, animal.name, animal.cost = id, name, cost
    db.add(animal)
    db.commit()


def create_property():
    names_job = [('', 0), ('продавец телефонов', 11000), ('риелтор', 50000), ('адвокат', 80000), ('шериф', 110000),
                 ('мер', 500000), ('старший инжинер Apppple', 550000), ('разроботчик Microsaft', 600000),
                 ('Стив Джобс', 1200000), ('Бил Гейтс', 12000000)]
    names_home = [('', 0), ('койка в мотеле', 1000), ('автодом', 15000), ('квартира', 150000),
                  ('номер в отеле', 200000), ('номер в отеле Бурдж-Халифа', 450000), ('высотка Трампа', 1250000),
                  ('собственные аппартаменты', 11000000), ('дом на Марсе', 50000000),
                  ('дача Путина - не продаётся', 1000000000000)]
    names_car = [('', 0), ('Лада Гранта', 150000), ('Лада Веста', 250000), ('Лада Xray', 500000),
                 ('VW Polo 1996', 600000), ('VW Tiguan 2019', 1200000), ('Lamborghini Aventador', 7500000),
                 ('Bugatti Veyron', 12000000), ('Bugatti Divo', 15000000), ('Köenigsegg Jesco', 25000000)]
    names_animal = [('', 0), ('улитка', 100), ('кошка', 500), ('собака', 1250), ('яшерица', 5000), ('змея', 7500),
                    ('ручной тигр', 15000), ('лев', 25000), ('слон', 100000), ('носорог', 250000)]
    try:
        for _ in range(10):
            create_job(_ + 1, names_job[_][0], names_job[_][1])
            create_home(_ + 1, names_home[_][0], names_home[_][1])
            create_car(_ + 1, names_car[_][0], names_car[_][1])
            create_animal(_ + 1, names_animal[_][0], names_animal[_][1])
        print('мтым')
    except:
        pass


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


def chek_player(from_id, vk, chat_id):
    global db
    resp = get_player(from_id)
    if not resp[0]:
        sendrer_messages(id=from_id, vk=vk,
                         text='Такого игорока нет в списке!', chat_id=chat_id)
        return False
    return True


def commands(text, from_id, vk, upload, chat_id):
    global db
    if text == 'статы':
        res = chek_player(from_id, vk, chat_id)
        if res:
            user = db.query(Player).filter(Player.vk_id == from_id).first()
            print(user)
            job = db.query(Job).filter(Job.id == user.job).first()

            print(job.name)
            home = db.query(Home).filter(Home.id == user.home_id).first()
            print(home.name)
            car = db.query(Car).filter(Car.id == user.car_id).first()
            print(car.name)
            animal = db.query(Animal).filter(Animal.id == user.animal_id).first()
            print(animal.name)
            ans = f'<Игрок👨>\n   -имя: {user.name}\n   -фамилия: {user.last_name}\n   -кошелёк: {user.money}\n   -работа: {job.name}\n   -дом: {home.name}\n   -машина: {car.name}\n   -питомец: {animal.name}\n   -дата создания аккаунта: {user.created_date}'
            sendrer_messages(ans, id=from_id, vk=vk, chat_id=chat_id)

    if text == 'работа':
        res = chek_player(from_id, vk, chat_id)
        if res:
            user = db.query(Player).filter(Player.vk_id == from_id).first()
            job = db.query(Job).filter(Job.id == user.job).first()
            if job.name == '':
                sendrer_messages(text='ИДИ НА ЗАВОД!!!!!', id=from_id, vk=vk, chat_id=chat_id)
            else:
                sendrer_messages(text=f'Твоя работа: {job.name}', id=from_id, vk=vk, chat_id=chat_id)

    if text == 'дом':
        res = chek_player(from_id, vk, chat_id)
        if res:
            user = db.query(Player).filter(Player.vk_id == from_id).first()
            home = db.query(Home).filter(Home.id == user.home_id).first()
            if home.name == '':
                sendrer_messages(text='КАКОЙ ДОМ НАФИГ, ТЫ БЕЗДОМНЫЙ!!!!!', id=from_id, vk=vk, chat_id=chat_id)
            else:
                sendrer_messages(text=f'Твой дом: {home.name}', id=from_id, vk=vk, chat_id=chat_id)

    if text == 'машина':
        res = chek_player(from_id, vk, chat_id)
        if res:
            user = db.query(Player).filter(Player.vk_id == from_id).first()
            car = db.query(Car).filter(Car.id == user.car_id).first()
            if car.name == '':
                sendrer_messages(text='Нет у тебя машины.', id=from_id, vk=vk, chat_id=chat_id)
            else:
                sendrer_messages(text=f'Твоя машина: {car.name}', id=from_id, vk=vk, chat_id=chat_id)

    if text == 'животное':
        res = chek_player(from_id, vk, chat_id)
        if res:
            user = db.query(Player).filter(Player.vk_id == from_id).first()
            animal = db.query(Animal).filter(Animal.id == user.animal_id).first()
            if animal.name == '':
                sendrer_messages(text='Нету у тебя питомца', id=from_id, vk=vk, chat_id=chat_id)
            else:
                sendrer_messages(text=f'Твоя работа: {animal.name}', id=from_id, vk=vk, chat_id=chat_id)

    if text == 'магаз':
        res = chek_player(from_id, vk, chat_id)
        if res:

            ans = ''
            ans += 'РАБОТЫ:\n'
            jobs = db.query(Job).filter(Job.id > 1)
            for _ in jobs:
                ans += (_.__repr__() + '\n')
            sendrer_messages(text=ans, vk=vk, id=from_id, chat_id=chat_id)

            ans = ''
            ans += 'ДОМА:\n'
            homes = db.query(Home).filter(Home.id > 1)
            for _ in homes:
                ans += (_.__repr__() + '\n')
            sendrer_messages(text=ans, vk=vk, id=from_id, chat_id=chat_id)

            ans = ''
            ans += 'МАШИНЫ:\n'
            cars = db.query(Car).filter(Car.id > 1)
            for _ in cars:
                ans += (_.__repr__() + '\n')
            sendrer_messages(text=ans, vk=vk, id=from_id, chat_id=chat_id)

            ans = ''
            ans += 'ПИТОМЦЫ:\n'
            animals = db.query(Animal).filter(Animal.id > 1)
            for _ in animals:
                ans += (_.__repr__() + '\n')
            sendrer_messages(text=ans, vk=vk, id=from_id, chat_id=chat_id)

            ans = ''
            ans += 'Чтобы купить что-то, напиши так: /купить [категория] [id]\n'
            ans += 'Категорию указывать надо в Иминительном падеже заглавными буквами, то есть: РАБОТА, МАШИНА...\n'
            ans += 'Да ты должен купить работу'
            sendrer_messages(text=ans, vk=vk, id=from_id, chat_id=chat_id)

    if text.startswith('купить'):
        res = chek_player(from_id, vk, chat_id=chat_id)
        if res:
            resp = text.split()
            category, id = resp[1], resp[2]
            usr = db.query(Player).filter(Player.vk_id == from_id).first()

            if category == 'работа':
                try:
                    usr.job = int(id)
                    sendrer_messages(id=from_id, vk=vk, chat_id=chat_id,
                                     text="Ты устроился на работу\nАванс в размере 20'000₽ упал на счёт.")
                    usr.money = usr.money + 20000
                    db.commit()
                except:
                    what_r_u_say(upload, id=from_id, vk=vk, text='Прости, такой работы с таким id нет')

            if category == 'дом':
                try:
                    home = db.query(Home).filter(Home.id == int(id)).first()
                    if usr.money > home.cost:
                        usr.home_id, usr.money = home.id, (usr.money - home.cost)
                        sendrer_messages(id=from_id, vk=vk, chat_id=chat_id,
                                         text=f'Ты приобрёл новый дом: {home.name}')
                        db.commit()
                    else:
                        sendrer_messages(id=from_id, vk=vk, chat_id=chat_id,
                                         text='Прости на твоём счету недостаточно денег')
                except:
                    what_r_u_say(upload, id=from_id, vk=vk, text='Прости, дома с таким id нет')

            if category == 'машина':
                try:
                    car = db.query(Car).filter(Car.id == int(id)).first()
                    if usr.money > car.cost:
                        usr.car_id, usr.money = car.id, (usr.money - car.cost)
                        sendrer_messages(id=from_id, vk=vk, chat_id=chat_id,
                                         text=f'Ты приобрёл новую машину: {car.name}')
                        db.commit()
                    else:
                        sendrer_messages(id=from_id, vk=vk, chat_id=chat_id,
                                         text='Прости на твоём счету недостаточно денег')
                except:
                    what_r_u_say(upload, id=from_id, vk=vk, text='Прости, машины с таким id нет')

            if category == 'питомец':
                try:
                    animal = db.query(Animal).filter(Animal.id == int(id)).first()
                    if usr.money > Animal.cost:
                        usr.animal_id, usr.money = animal.id, (usr.money - animal.cost)
                        sendrer_messages(id=from_id, vk=vk, chat_id=chat_id,
                                         text=f'Ты приобрёл нового питомца: {animal.name}')
                        db.commit()
                    else:
                        sendrer_messages(id=from_id, vk=vk, chat_id=chat_id,
                                         text='Прости на твоём счету недостаточно денег')
                except:
                    what_r_u_say(upload, id=from_id, vk=vk, text='Прости, питомца с таким id нет')

            if category not in ['питомец', 'машина', 'дом', 'работа']:
                what_r_u_say(upload, id, vk, text='Прости, такой категории нет.')


def out_game(text, from_id, vk, chat_id):
    if text == 'выйти из игры':
        sendrer_messages(text='Возращайся', id=from_id, vk=vk, chat_id=chat_id)
        response = vk.users.get(user_ids=from_id, fields='first_name, last_name, city')
        name = response[0]['first_name']
        start('hi', response=response, name=name, from_id=from_id, vk=vk, chat_id=chat_id)


def settings(text, from_id, vk, chat_id):
    if text == 'настройки':
        bol = chek_player(from_id, vk, chat_id)
        if bol:
            sendrer_messages(vk=vk, id=from_id, chat_id=chat_id,
                             text='Ты защел во вкладку настройки. Тут ты можешь поменять свой ник в игре.')
            sendrer_messages(vk=vk, id=from_id, chat_id=chat_id,
                             text='Чтобы поменять имя, напиши: измени моё имя - ..., и пишешь какое имя хочешь иметь\nС фамилией аналогично')
    if text.startswith('измени моё имя - '):
        bol = chek_player(from_id, vk, chat_id)
        if bol:
            txt = text.split()
            name = txt[-1]
            change_data_player(from_id, name=name)
            sendrer_messages(vk=vk, id=from_id, chat_id=chat_id,
                             text=f'Отлично ты поменял своё имя, теперь твоё имя: {name}')
    if text.startswith('измени мою фамилию - '):
        bol = chek_player(from_id, vk, chat_id)
        if bol:
            txt = text.split()
            surname = txt[-1]
            change_data_player(from_id, surname=surname)
            sendrer_messages(vk=vk, id=from_id, chat_id=chat_id,
                             text=f'Отлично ты поменял свою фамилию, теперь твоя фамилия: {surname}')


def refom_str(str=''):
    str = str.split()
    if str[0].startswith('[') and str[0].endswith(']'):
        str = str[1:]
    str = ' '.join(str)
    return str


def main():
    TOKEN = '8a0e38b21d3bb35844d2fdcacb9e94d2446406f8b54572265195247ed73a49241004f7185912acc51c474'
    vk_session = vk_api.VkApi(token=TOKEN)

    vk = vk_session.get_api()
    keyboard = VkKeyboard()
    upload = VkUpload(vk_session)
    longpool = VkBotLongPoll(vk_session, '193034203')
    create_property()
    print('создано имущество')



    events = longpool.listen()
    for event in events:
        print(event.type)
        if event.type == VkBotEventType.MESSAGE_NEW:

            # описание
            text, from_id = event.obj.message["text"].lower(), event.obj.message['from_id']
            text = refom_str(text)
            print(event.chat_id)
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
                what_r_u_say(upload, from_id, vk, chat_id=event.chat_id)
            start(text, response, name, from_id, vk, chat_id=event.chat_id)
            date_time(text, from_id, vk, chat_id=event.chat_id)
            del_keyb(text=text, from_id=from_id, keyb=keyboard, vk=vk, chat_id=event.chat_id)
            game(text=text, from_id=from_id, vk=vk, chat_id=event.chat_id)
            if text.startswith('/'):
                commands(text[1:], from_id, vk, upload, chat_id=event.chat_id)
            out_game(text, from_id, vk, event.chat_id)
            settings(text, from_id, vk, event.chat_id)


if __name__ == '__main__':
    main()