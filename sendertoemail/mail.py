import telebot
import smtplib
import ssl
import datetime
from datetime import date
from datetime import datetime, timedelta
import configure
from telebot import types
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup as bs
import phonenumbers



bot = telebot.TeleBot(configure.config['token'])


user_dict = {}
current_shown_dates={}

lang_dict = {'ask_name': {'Русский 🇷🇺': 'Просим указать Ф.И.О.(полностью):', 'Oʻzbek tili 🇺🇿': 'Toʻliq F.I.Sh. ni kiritishingizni soʻraymiz:' },
             'wrong_name': {'Русский 🇷🇺': 'Данные введены некорректно. Просим указать фамилию, имя и отчество (через пробелы).', 'Oʻzbek tili 🇺🇿': 'Ism, familiya va otasining ismi bo‘shliqlar orqali yozilgan, kamida uchta so‘z bolishi kerak' },
             'ask_birthday': {'Русский 🇷🇺': 'Дата Вашего рождения:', 'Oʻzbek tili 🇺🇿': 'Tugʻilgan yil, oy va sanangizni kiriting:' },
             'wrong_birthday': {'Русский 🇷🇺': 'Вы ввели неправильную дату!', 'Oʻzbek tili 🇺🇿': 'Siz notoʻgʻri sanani kiritdingiz!' },
             'number': {'Русский 🇷🇺': 'Укажите контактный номер, чтобы мы могли связаться с Вами:', 'Oʻzbek tili 🇺🇿': 'Siz bilan bogʻlana olishimiz uchun kontakt raqam kiriting:' },
             'wrong_number': {'Русский 🇷🇺': 'Неверный формат номера!', 'Oʻzbek tili 🇺🇿': 'Notoʻgʻri raqam formati!' },
             'adress': {'Русский 🇷🇺': 'Укажите адрес проживания', 'Oʻzbek tili 🇺🇿': 'Yashash manzilingizni kiriting:' },
             'town': {'Русский 🇷🇺': 'Город или область:', 'Oʻzbek tili 🇺🇿': 'Shahar yoki viloyat:' },
             'wrong_town': {'Русский 🇷🇺': 'Название города должно состоять из букв и может быть несколькими словами', 'Oʻzbek tili 🇺🇿': 'Shahar nomi harflardan iborat boʻlishi kerak va bir necha so‘z boʻlishi mumkin' },
             'district': {'Русский 🇷🇺': 'Район:', 'Oʻzbek tili 🇺🇿': 'Tuman:' },
             'wrong_district': {'Русский 🇷🇺': 'Название района должно состоять из букв и может быть несколькими словами', 'Oʻzbek tili 🇺🇿': 'Tuman nomi harflardan iborat boʻlishi kerak va bir necha so‘z boʻlishi mumkin' },
             'quarter': {'Русский 🇷🇺': 'Квартал или улица:', 'Oʻzbek tili 🇺🇿': 'Kvartal raqami yoki ko‘chaning nomi:' },
             'wrong_quarter': {'Русский 🇷🇺': 'Название квартала или улицы должно состоять из букв или цифр', 'Oʻzbek tili 🇺🇿': 'Blok yoki ko‘chaning nomi harflar yoki raqamlardan iborat boʻlishi kerak' },
             'house': {'Русский 🇷🇺': 'Дом:', 'Oʻzbek tili 🇺🇿': 'Uy raqami:' },
             'wrong_house': {'Русский 🇷🇺': 'Название дома должно состоять из цифр или букв', 'Oʻzbek tili 🇺🇿': 'Uyning nomi raqamlar yoki harflardan iborat boʻlishi kerak' },
             'education': {'Русский 🇷🇺': 'Укажите уровень образования:', 'Oʻzbek tili 🇺🇿': 'Taʻlim darajasini ko‘rsating:' },
             'uzb_language': {'Русский 🇷🇺': 'Степень владения Узбекским языком:', 'Oʻzbek tili 🇺🇿': 'Oʻzbek tilini bilish darajasi:' },
             'rus_language': {'Русский 🇷🇺': 'Степень владения Русским языком:', 'Oʻzbek tili 🇺🇿': 'Rus tilini bilish darajasi:' },
             'eng_language': {'Русский 🇷🇺': 'Степень владения Английским языком:', 'Oʻzbek tili 🇺🇿': 'Ingliz tilini bilish darajasi:' },
             'higher':  {'Русский 🇷🇺': 'Высшее', 'Oʻzbek tili 🇺🇿': 'Oliy' },
             'incomplete_higher':  {'Русский 🇷🇺': 'Неполное высшее', 'Oʻzbek tili 🇺🇿': 'Tugallanmagan oliy' },
             'secondary':  {'Русский 🇷🇺': 'Среднее', 'Oʻzbek tili 🇺🇿': 'Oʻrta' },
             'incomplete_secondary':  {'Русский 🇷🇺': 'Неполное среднее', 'Oʻzbek tili 🇺🇿': 'Tugallanmagan oʻrta' },
             'secondary_special':  {'Русский 🇷🇺': 'Среднее специальное', 'Oʻzbek tili 🇺🇿': 'Oʻrta maxsus' },
             'great':  {'Русский 🇷🇺': 'Отлично', 'Oʻzbek tili 🇺🇿': 'A‘lo' },
             'good':  {'Русский 🇷🇺': 'Хорошо', 'Oʻzbek tili 🇺🇿': 'Yaxshi' },
             'satisfactorily':  {'Русский 🇷🇺': 'Удовлетворительно', 'Oʻzbek tili 🇺🇿': 'Qoniqarli' },
             'work':  {'Русский 🇷🇺': 'Опыт работы: "Есть" или "Нет"?', 'Oʻzbek tili 🇺🇿': 'Ish tajribangiz: "Bor" yoki "Yoʻq"' },
             'organization':  {'Русский 🇷🇺': 'Укажите название организации:', 'Oʻzbek tili 🇺🇿': 'Tashkilot nomini kiriting' },
             'wrong_organization':  {'Русский 🇷🇺': 'Название организации должно состоять из букв или цифр и может быть несколькими словами', 'Oʻzbek tili 🇺🇿': 'Tashkilot nomi harflar yoki raqamlardan iborat boʻlishi kerak va bir nechta soʻzlar boʻlishi mumkin' },
             'job_title':  {'Русский 🇷🇺': 'Должность:', 'Oʻzbek tili 🇺🇿': 'Lavozim:' },
             'wrong_job_title':  {'Русский 🇷🇺': 'Название специальности должно состоять из букв, также в нём могут быть пробелы и цифры', 'Oʻzbek tili 🇺🇿': 'Mutaxassislikning nomi harflardan iborat boʻlishi kerak, unda bo‘shliqlar va raqamlar ham boʻlishi mumkin' },
             'work_start':  {'Русский 🇷🇺': 'Укажите год трудоустройства в организацию:', 'Oʻzbek tili 🇺🇿': 'Tashkilotga ishga kirgan yilingizni kiriting:' },
             'wrong_work_start':  {'Русский 🇷🇺': 'Формат года указан не верно.\nПример: 2020', 'Oʻzbek tili 🇺🇿': 'Yil kiritilgan format noto‘g‘ri.\nMisol: 2020' },
             'work_end':  {'Русский 🇷🇺': 'Укажите год увольнения из организации:', 'Oʻzbek tili 🇺🇿': 'Siz tashkilotdan boʻshagan yilni koʻrsating:' },
             'wrong_work_end':  {'Русский 🇷🇺': 'Формат года указан не верно.\nПример: 2020', 'Oʻzbek tili 🇺🇿': 'Yil kiritilgan format noto‘g‘ri.\nMisol: 2020' },
             'wrong_work_datas':  {'Русский 🇷🇺': ' Вы не могли уйти с работы раньше чем на неё устроились.Год когда вы устроились на работу?', 'Oʻzbek tili 🇺🇿': 'Siz tashkilotdan boʻshagan yilingiz - ishga kirgan yilingizdan oldin boʻlishi mumkin emas. Siz tashkilotga ishga kirgan yilni qaytadan kiriting:' },
             'thank_you': {'Русский 🇷🇺': 'Спасибо за прохождение опроса!!!', 'Oʻzbek tili 🇺🇿': 'So‘rovnomadan o‘tganingiz uchun minnatdormiz!!!' },
             'sendmail': {'Русский 🇷🇺': 'Ваше резюме отправлено на рассмотрение.\n\nПодготовьтесь к телефонному собеседованию\n\nСписок примерных вопросов:\n1.Расскажите о себе\n2.Какими качествами должен обладать сотрудник контакт-центра\n3.Ваши ожидания по заработной плате', 'Oʻzbek tili 🇺🇿': 'Sizning maʻlumotlaringiz koʻrib chiqish uchun yuborildi.\n\n Telefon orqali suhbatdan oʻtishga tayyorlaning \n\n Berilishi mumkin boʻlgan savollardan namunalar: \n1. Oʻzingiz haqingizda gapirib bering.\n2. Kontakt markazi xodimi qanday fazilatlarga ega boʻlishi kerak?\n 3. Qancha miqdordagi maosh sizni qoniqtirgan boʻlardi?' },
             'again':  {'Русский 🇷🇺': 'Если хотите пройти опрос заново нажмите на кнопку: "/start" ', 'Oʻzbek tili 🇺🇿': 'Soʻrovnomadan qaytadan oʻtishni istasangiz quyidagi tugmani bosing: "/start"' },
             'checker':  {'Русский 🇷🇺': 'Выберите вариант кнопкой', 'Oʻzbek tili 🇺🇿': 'Tugmani bosib variantni tanlang' },
             'yes':  {'Русский 🇷🇺': 'Ecть', 'Oʻzbek tili 🇺🇿': 'Bor' },
             'no':  {'Русский 🇷🇺': 'Нет', 'Oʻzbek tili 🇺🇿': 'Yoʻq' },
             'back':  {'Русский 🇷🇺': 'Назад', 'Oʻzbek tili 🇺🇿': 'Orqaga' },
             'start':  {'Русский 🇷🇺': 'Начать сначала', 'Oʻzbek tili 🇺🇿': 'Boshidan boshlash' },
             'knopka':  {'Русский 🇷🇺': 'На следующие вопросы ответьте выбором одного из вариантов!', 'Oʻzbek tili 🇺🇿': 'Quyidagi savollarga keltirilgan variantlardan birini tanlash orqali javob bering!' },
             'work_experience':  {'Русский 🇷🇺': 'Перечислите свои предыдущие места работы. Укажите периоды работы и должности:', 'Oʻzbek tili 🇺🇿': 'Avvalgi ish joylaringiz nomlarini kiriting. Ularda ishlagan muddat va lavozimingizni ko‘rsating:' },
             'wrong_work_experience':  {'Русский 🇷🇺': 'Неверные данные', 'Oʻzbek tili 🇺🇿': 'Notoʻgʻri maʻlumotlar' }
            
             
}



class User:
    def __init__(self, lang):
        self.lang = lang
        self.name = None
        self.birthday = None
        self.number = None
        self.town = None
        self.district = None
        self.quarter = None
        self.house = None
        self.education = None
        self.uz_language = None
        self.ru_language = None
        self.work = None
        self.organization = None
        self.job_title = None
        self.work_start = None
        self.work_end = None
        self.en_language = None
        self.work_experience = None
        #self.resume = None



markupp = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
btn1 = types.KeyboardButton('Русский 🇷🇺')
btn2 = types.KeyboardButton('Oʻzbek tili 🇺🇿')
markupp.row(btn1, btn2)


@bot.message_handler(commands=['start'])
def process_start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    msg = bot.send_message(message.chat.id,
                           'Здравствуйте!\nПожалуйста, выберите язык\n\nAssalomu alaykum!\nIltimos, tilni tanlang',
                           reply_markup=markupp)
    bot.register_next_step_handler(msg, ask_language)    

@bot.message_handler(content_types = ['text'])
def checker(message):

    print(message.text)
    print("checker")
    if(message.text=='/start'):
        print("in if")
        process_start(message)
        return
    elif(message.text=='Начать сначала'):
        process_start(message)
        return 
    elif(message.text=='Boshidan boshlash'):
        process_start(message)
        return                         
    else:
        print("in else")
        bot.reply_to(message, "Выберите вариант кнопкой")


@bot.message_handler(content_types = ['text'])
def ask_language(message):
    try:
        chat_id = message.chat.id
        lang = message.text
        if(lang=='/start'):
            process_start(message)
            return
        user = User(lang)
        user_dict[chat_id] = user
        print(user)
        print(ask_language)
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn = types.KeyboardButton(lang_dict['start'][user.lang])
        markup.row(btn)
        
        msg = bot.send_message(message.chat.id,
                        lang_dict['ask_name'][user.lang],
                        reply_markup = markup)

        bot.register_next_step_handler(msg, ask_name)  
    except KeyError:
        msg = bot.reply_to(message, "Выберите один из вариантов 'Русский' или 'Ozbek tili'\n\n 'Русский' yoki 'Ozbek tili' parametrlaridan birini tanlang ")
        bot.register_next_step_handler(msg, ask_language)



       
@bot.message_handler(content_types = ['text'])
def ask_name(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = user_dict[chat_id]

        markup__v1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_1 = types.KeyboardButton(lang_dict['start'][user.lang])
        btn_2 = types.KeyboardButton(lang_dict['back'][user.lang])
        markup__v1.row(btn_1, btn_2)

        if(name==lang_dict['start'][user.lang] or name == '/start'):
            process_start(message)
            return          
              
        if not(name.count(' ') >= 1 and name.count(' ') <= 30):
            msg = bot.reply_to(message, lang_dict['wrong_name'][user.lang])
            bot.register_next_step_handler(msg, ask_name)  
            return      
        if not(any(x.isalpha() for x in name)
            and any(x.isspace() for x in name)
            and all(x.isalpha() or x.isspace() for x in name)):
                msg = bot.reply_to(message, lang_dict['wrong_name'][user.lang])
                bot.register_next_step_handler(msg, ask_name) 
                return
                            
        user.name = name

        

        msg = bot.send_message(message.chat.id, lang_dict['ask_birthday'][user.lang], reply_markup = markup__v1)
        bot.register_next_step_handler(msg, ask_birthday)
        #bot.delete_message(message.chat.id, message.message_id-1)
    except Exception as e:    
        msg = bot.reply_to(message, "Неверные данные")
        bot.register_next_step_handler(msg, ask_name)


def ask_birthday(message):
    try:
        chat_id = message.chat.id
        birthday = message.text
        user = user_dict[chat_id]

        markup__v1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_1 = types.KeyboardButton(lang_dict['start'][user.lang])
        btn_2 = types.KeyboardButton(lang_dict['back'][user.lang])
        markup__v1.row(btn_1, btn_2)

        if(birthday == lang_dict['back'][user.lang]):
            chat_id = message.chat.id
            user = user_dict[chat_id]
            bot.delete_message(message.chat.id, message.message_id-1)
            bot.delete_message(message.chat.id, message.message_id-2)
            msg = bot.send_message(message.chat.id, lang_dict['ask_name'][user.lang], reply_markup = markup__v1)
            bot.register_next_step_handler(msg, ask_name)
            return
        if(birthday == lang_dict['start'][user.lang] or birthday == '/start'):
            process_start(message)
            return 
        
        if not all(x.isascii() or x.isspace() or x.isalnum() for x in birthday):
            msg = bot.reply_to(message, lang_dict['wrong_birthday'][user.lang])
            bot.register_next_step_handler(msg, ask_birthday) 
            return          

        

        user.birthday = birthday

        msg = bot.send_message(message.chat.id, lang_dict['number'][user.lang], reply_markup = markup__v1) 
        bot.register_next_step_handler(msg, ask_number)     
        #formatlist = ['%d.%m.%Y', '%d,%m,%Y', '%d/%m/%Y']  
        #for i in formatlist: 
            #try:
                #chat_id = message.chat.id
                #user = user_dict[chat_id]
                #datetime.strptime(birthday, i)
                #user.birthday = birthday 
                #msg = bot.send_message(message.chat.id, lang_dict['number'][user.lang], reply_markup = markup__v1)
                #bot.register_next_step_handler(msg, ask_number)    


            #except ValueError:
                #pass                        
        #if user.birthday == None:
            #msg = bot.reply_to(message, "Неверный формат даты")
            #bot.register_next_step_handler(msg, ask_birthday)     
           
    except Exception:    
        msg = bot.reply_to(message, "Неверные данные")
        bot.register_next_step_handler(msg, ask_birthday) 
              



def ask_number(message):
    try:
        chat_id = message.chat.id
        number = message.text
        user = user_dict[chat_id]

        markup__v1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_1 = types.KeyboardButton(lang_dict['start'][user.lang])
        btn_2 = types.KeyboardButton(lang_dict['back'][user.lang])
        markup__v1.row(btn_1, btn_2)

        
        if(number == lang_dict['back'][user.lang]):
            chat_id = message.chat.id
            user = user_dict[chat_id]
            bot.delete_message(message.chat.id, message.message_id-1)
            bot.delete_message(message.chat.id, message.message_id-2)
            msg = bot.send_message(message.chat.id, lang_dict['ask_birthday'][user.lang], reply_markup = markup__v1)
            bot.register_next_step_handler(msg, ask_birthday)
            return

        if(number == lang_dict['start'][user.lang] or number == '/start'):
            process_start(message)
            return
        
        if not all(x.isascii() or x.isspace() or x.isalnum() for x in number):
            msg = bot.reply_to(message, lang_dict['wrong_birthday'][user.lang])
            bot.register_next_step_handler(msg, ask_number) 
            return          
        

        #my_number = phonenumbers.parse(number, "UZ")
           
        #if phonenumbers.is_valid_number(my_number)==False:
            #msg = bot.reply_to(message, lang_dict['wrong_number'][user.lang])
            #bot.register_next_step_handler(msg, ask_number)
            #return
        #if not(len(str(number))>=9 and len(str(number))<=13 and len(str(number))!=10 and len(str(number))!=11):
            #msg = bot.reply_to(message, lang_dict['wrong_number'][user.lang])
            #bot.register_next_step_handler(msg, ask_number)
            #return       

        user.number = number

       

        msg = bot.send_message(message.chat.id, lang_dict['adress'][user.lang])
        bot.send_message(message.chat.id, lang_dict['town'][user.lang], reply_markup=markup__v1)
        bot.register_next_step_handler(msg, ask_town)
    except Exception:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        msg = bot.reply_to(message, lang_dict['wrong_number'][user.lang])
        bot.register_next_step_handler(msg, ask_number)
        
def ask_town(message):
    try:
        chat_id = message.chat.id
        town = message.text
        user = user_dict[chat_id]

        markup__v1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_1 = types.KeyboardButton(lang_dict['start'][user.lang])
        btn_2 = types.KeyboardButton(lang_dict['back'][user.lang])
        markup__v1.row(btn_1, btn_2)

        if(town == lang_dict['back'][user.lang]):
            chat_id = message.chat.id
            user = user_dict[chat_id]
            bot.delete_message(message.chat.id, message.message_id-1)
            bot.delete_message(message.chat.id, message.message_id-2)
            msg = bot.send_message(message.chat.id, lang_dict['number'][user.lang], reply_markup = markup__v1)
            bot.register_next_step_handler(msg, ask_number)
            return
        if(town == lang_dict['start'][user.lang] or town == '/start'):
            process_start(message)
            return 
        if not all(x.isalpha() or x.isspace() for x in town):
            msg = bot.reply_to(message, lang_dict['wrong_town'][user.lang])
            bot.register_next_step_handler(msg, ask_town) 
            return          
        user = user_dict[chat_id]
        user.town = town   

        msg = bot.send_message(message.chat.id, lang_dict['district'][user.lang], reply_markup=markup__v1) 
        bot.register_next_step_handler(msg, ask_district)
    except Exception:
        msg = bot.reply_to(message, 'Неверные данные!')
        bot.register_next_step_handler(msg, ask_town)

def ask_district(message):
    try:
        chat_id = message.chat.id
        district = message.text
        user = user_dict[chat_id]

        markup__v1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_1 = types.KeyboardButton(lang_dict['start'][user.lang])
        btn_2 = types.KeyboardButton(lang_dict['back'][user.lang])
        markup__v1.row(btn_1, btn_2)

        if(district == lang_dict['back'][user.lang]):
            chat_id = message.chat.id
            user = user_dict[chat_id]
            bot.delete_message(message.chat.id, message.message_id-1)
            bot.delete_message(message.chat.id, message.message_id-2)
            msg = bot.send_message(message.chat.id, lang_dict['town'][user.lang], reply_markup = markup__v1)
            bot.register_next_step_handler(msg, ask_town)
            return
        if(district == lang_dict['start'][user.lang] or district == '/start'):
            process_start(message)
            return     
        if not all(x.isalpha() or x.isspace() for x in district):
            msg = bot.reply_to(message, lang_dict['wrong_district'][user.lang])
            bot.register_next_step_handler(msg, ask_district) 
            return        
            
        user.district = district 
        

        msg = bot.send_message(message.chat.id, lang_dict['quarter'][user.lang], reply_markup=markup__v1) 
        bot.register_next_step_handler(msg, ask_quarter)
    except Exception:
        msg = bot.reply_to(message, 'Неверные данные!')
        bot.register_next_step_handler(msg, ask_district)

def ask_quarter(message):
    try:
        chat_id = message.chat.id
        quarter = message.text
        user = user_dict[chat_id]

        markup__v1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_1 = types.KeyboardButton(lang_dict['start'][user.lang])
        btn_2 = types.KeyboardButton(lang_dict['back'][user.lang])
        markup__v1.row(btn_1, btn_2)

        if(quarter == lang_dict['back'][user.lang]):
            chat_id = message.chat.id
            user = user_dict[chat_id]
            bot.delete_message(message.chat.id, message.message_id-1)
            bot.delete_message(message.chat.id, message.message_id-2)
            msg = bot.send_message(message.chat.id, lang_dict['district'][user.lang], reply_markup = markup__v1)
            bot.register_next_step_handler(msg, ask_district)
            return
        if(quarter == lang_dict['start'][user.lang] or quarter == '/start'):
            process_start(message)
            return
        if not all(x.isalnum() or x.isspace() for x in quarter):
            msg = bot.reply_to(message, lang_dict['wrong_quarter'][user.lang])
            bot.register_next_step_handler(msg, ask_quarter) 
            return        
            
        user.quarter = quarter  

        msg = bot.send_message(message.chat.id, lang_dict['house'][user.lang], reply_markup=markup__v1) 
        bot.register_next_step_handler(msg, ask_house)
    except Exception:
        msg = bot.reply_to(message, 'Неверные данные!')
        bot.register_next_step_handler(msg, ask_quarter)   

def ask_house(message):
    try:
        chat_id = message.chat.id
        house = message.text
        user = user_dict[chat_id]

        markup__v1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_1 = types.KeyboardButton(lang_dict['start'][user.lang])
        btn_2 = types.KeyboardButton(lang_dict['back'][user.lang])
        markup__v1.row(btn_1, btn_2)
        

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn = types.KeyboardButton(lang_dict['start'][user.lang])
        markup.row(btn)


        if(house == lang_dict['back'][user.lang]):
            chat_id = message.chat.id
            user = user_dict[chat_id]
            bot.delete_message(message.chat.id, message.message_id-1)
            bot.delete_message(message.chat.id, message.message_id-2)
            msg = bot.send_message(message.chat.id, lang_dict['quarter'][user.lang], reply_markup = markup__v1)
            bot.register_next_step_handler(msg, ask_quarter)
            return
        if(house == lang_dict['start'][user.lang] or house == '/start'):
            process_start(message)
            return
        if not all(x.isalnum() or x.isspace() for x in house):
            msg = bot.reply_to(message, lang_dict['wrong_house'][user.lang])
            bot.register_next_step_handler(msg, ask_house) 
            return              
        user.house = house 
        bot.send_message(message.chat.id , lang_dict['knopka'][user.lang], reply_markup = markup)
        education_1(message)
    except Exception: 
        msg = bot.reply_to(message, 'Неверные данные!')
        bot.register_next_step_handler(msg, ask_house)

@bot.message_handler(content_types = ['text'])
def education_1(message):  
    chat_id = message.chat.id
    user = user_dict[chat_id]
    markup1 = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton(lang_dict['higher'][user.lang], callback_data='Высшее')
    item2 = types.InlineKeyboardButton(lang_dict['incomplete_higher'][user.lang], callback_data='Неполное высшее')
    item3 = types.InlineKeyboardButton(lang_dict['secondary'][user.lang], callback_data='Среднее')
    item4 = types.InlineKeyboardButton(lang_dict['incomplete_secondary'][user.lang], callback_data='Неполное среднее')
    item5 = types.InlineKeyboardButton(lang_dict['secondary_special'][user.lang], callback_data='Среднее специальное')
    item6 = types.InlineKeyboardButton(lang_dict['back'][user.lang], callback_data='bck_house')
    markup1.add(item1, item2, item3, item4, item5, item6)
    bot.send_message(message.chat.id, lang_dict['education'][user.lang] , reply_markup=markup1)
    


   

    

@bot.message_handler(content_types = ['text'])
def uzb_language(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    markup2 = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton(lang_dict['great'][user.lang], callback_data='Отлично')
    item2 = types.InlineKeyboardButton(lang_dict['good'][user.lang], callback_data='Хорошо')
    item3 = types.InlineKeyboardButton(lang_dict['satisfactorily'][user.lang], callback_data='Удовлетворительно')
    item4 = types.InlineKeyboardButton(lang_dict['back'][user.lang], callback_data='bck_edu')
    markup2.add(item1, item2, item3, item4)
    bot.send_message(message.chat.id, lang_dict['uzb_language'][user.lang], reply_markup=markup2)       
    
       
@bot.message_handler(content_types = ['text'])
def rus_language(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    markup3 = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton(lang_dict['great'][user.lang], callback_data='Отлично знаю')
    item2 = types.InlineKeyboardButton(lang_dict['good'][user.lang], callback_data='Хорошо знаю')
    item3 = types.InlineKeyboardButton(lang_dict['satisfactorily'][user.lang], callback_data='Удовлетворительно знаю')
    item4 = types.InlineKeyboardButton(lang_dict['back'][user.lang], callback_data='bck_uz')
    markup3.add(item1, item2, item3, item4)
    bot.send_message(message.chat.id, lang_dict['rus_language'][user.lang] , reply_markup=markup3) 

@bot.message_handler(content_types = ['text'])
def english_language(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    markup4 = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton(lang_dict['great'][user.lang], callback_data='Отлично владею')
    item2 = types.InlineKeyboardButton(lang_dict['good'][user.lang], callback_data='Хорошо владею')
    item3 = types.InlineKeyboardButton(lang_dict['satisfactorily'][user.lang], callback_data='Удовлетворительно владею')
    item4 = types.InlineKeyboardButton(lang_dict['back'][user.lang], callback_data='bck_ru')
    markup4.add(item1, item2, item3, item4)
    bot.send_message(message.chat.id, lang_dict['eng_language'][user.lang] , reply_markup=markup4) 
 

 
@bot.message_handler(content_types = ['text'])
def about_work(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    markup_o = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton(lang_dict['yes'][user.lang], callback_data='да')
    item2 = types.InlineKeyboardButton(lang_dict['no'][user.lang], callback_data='нет')
    item3 = types.InlineKeyboardButton(lang_dict['back'][user.lang], callback_data='bck_eng')
    markup_o.row(item1, item2)
    markup_o.row(item3)
    bot.send_message(message.chat.id, lang_dict['work'][user.lang], reply_markup=markup_o)

@bot.message_handler(content_types = ['text'])
def say_experience(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    msg = bot.send_message(message.chat.id, lang_dict['work_experience'][user.lang])
    bot.register_next_step_handler(msg, ask_work_experience)    

@bot.message_handler(content_types = ['text'])
def ask_work_experience(message):
    try:
        chat_id = message.chat.id
        work_experience = message.text
        user = user_dict[chat_id]
        #bot.send_message(message.chat.id, lang_dict['work_experience'][user.lang])

        markup__v1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_1 = types.KeyboardButton(lang_dict['start'][user.lang])
        btn_2 = types.KeyboardButton(lang_dict['back'][user.lang])
        markup__v1.row(btn_1, btn_2)

        if(work_experience == lang_dict['back'][user.lang]):
            chat_id = message.chat.id
            user = user_dict[chat_id]
            bot.delete_message(message.chat.id, message.message_id-1)
            bot.delete_message(message.chat.id, message.message_id-2)
            msg = bot.send_message(message.chat.id, lang_dict['work'][user.lang], reply_markup = markup__v1)
            bot.register_next_step_handler(msg, about_work)
            return
        if(work_experience == lang_dict['start'][user.lang] or work_experience == '/start'):
            process_start(message)
            return         
        if not all(x.isascii() or x.isspace() or x.isalnum() for x in work_experience):
            msg = bot.reply_to(message, lang_dict['wrong_work_experience'][user.lang])
            bot.register_next_step_handler(msg, ask_work_experience) 
            return              
        user.work_experience = work_experience
        msg = bot.send_message(message.chat.id, lang_dict['thank_you'][user.lang])
        send_email(message)    

    except Exception:    
        msg = bot.reply_to(message, "Неверные данные")
        bot.register_next_step_handler(msg, ask_work_experience) 

@bot.message_handler(content_types = ['text'])
def say_thanks(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    msg = bot.send_message(message.chat.id, lang_dict['thank_you'][user.lang])
    send_email_without_work(message) 
        



"""@bot.message_handler(content_types = ['text'])
def ask_organization(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    
    markup__v1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn_1 = types.KeyboardButton(lang_dict['start'][user.lang])
    btn_2 = types.KeyboardButton(lang_dict['back'][user.lang])
    markup__v1.row(btn_1, btn_2)

    msg = bot.send_message(message.chat.id, lang_dict['organization'][user.lang], reply_markup = markup__v1)
    bot.register_next_step_handler(msg, about_organization)
                           
       
@bot.message_handler(content_types = ['text'])
def about_organization(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        organization = message.text

        markup__v1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_1 = types.KeyboardButton(lang_dict['start'][user.lang])
        btn_2 = types.KeyboardButton(lang_dict['back'][user.lang])
        markup__v1.row(btn_1, btn_2)

        if(organization == lang_dict['back'][user.lang]):
            bot.delete_message(message.chat.id, message.message_id-1)
            bot.delete_message(message.chat.id, message.message_id-2)
            about_work(message)
            return
        if(organization == lang_dict['start'][user.lang] or organization == '/start'):
            process_start(message)
            return
        if not all(x.isalnum() or x.isspace() for x in organization):
            msg = bot.reply_to(message, lang_dict['wrong_organization'][user.lang])
            bot.register_next_step_handler(msg, about_organization) 
            return   
        user.organization = organization   
        msg = bot.send_message(message.chat.id, lang_dict['job_title'][user.lang]) 
        bot.register_next_step_handler(msg, about_job_title)
    except Exception as e:
        msg = bot.reply_to(message, 'Неверные данные!')
        bot.register_next_step_handler(msg, about_organization)   
def about_job_title(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        job_title = message.text

        markup__v1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_1 = types.KeyboardButton(lang_dict['start'][user.lang])
        btn_2 = types.KeyboardButton(lang_dict['back'][user.lang])
        markup__v1.row(btn_1, btn_2)


        if(job_title == lang_dict['back'][user.lang]):
            chat_id = message.chat.id
            user = user_dict[chat_id]
            bot.delete_message(message.chat.id, message.message_id-1)
            bot.delete_message(message.chat.id, message.message_id-2)
            msg = bot.send_message(message.chat.id, lang_dict['organization'][user.lang], reply_markup = markup__v1)
            bot.register_next_step_handler(msg, about_organization)
            return
        if(job_title == lang_dict['start'][user.lang] or job_title == '/start'):
            process_start(message)
            return
        if not all(x.isalnum() or x.isspace() for x in job_title):
            msg = bot.reply_to(message, lang_dict['wrong_job_title'][user.lang])
            bot.register_next_step_handler(msg, about_job_title) 
            return   
        user.job_title = job_title   
        msg = bot.send_message(message.chat.id, lang_dict['work_start'][user.lang]) 
        bot.register_next_step_handler(msg, about_work_start)
    except Exception as e:
        msg = bot.reply_to(message, 'Неверные данные!')
        bot.register_next_step_handler(msg, about_job_title)   

def about_work_start(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        work_start = message.text
        
        markup__v1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_1 = types.KeyboardButton(lang_dict['start'][user.lang])
        btn_2 = types.KeyboardButton(lang_dict['back'][user.lang])
        markup__v1.row(btn_1, btn_2)

        today = date.today()
        if(work_start == lang_dict['back'][user.lang]):
            chat_id = message.chat.id
            user = user_dict[chat_id]
            bot.delete_message(message.chat.id, message.message_id-1)
            bot.delete_message(message.chat.id, message.message_id-2)
            msg = bot.send_message(message.chat.id, lang_dict['job_title'][user.lang], reply_markup = markup__v1)
            bot.register_next_step_handler(msg, about_job_title)
            return
        if(work_start == lang_dict['start'][user.lang] or work_start == '/start'):
            process_start(message)
            return
        if not work_start.isdigit() or not int(work_start) > 1970 or not int(work_start) <= today.year:
            msg = bot.reply_to(message, lang_dict['wrong_work_start'][user.lang])
            bot.register_next_step_handler(msg, about_work_start)
            return
        
        user.work_start = work_start  
        msg = bot.send_message(message.chat.id, lang_dict['work_end'][user.lang]) 
        bot.register_next_step_handler(msg, about_work_end)
    except Exception as e:
        msg = bot.reply_to(message, 'Неверные данные!')
        bot.register_next_step_handler(msg, about_work_start)   
def about_work_end(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        work_end = message.text

        markup__v1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_1 = types.KeyboardButton(lang_dict['start'][user.lang])
        btn_2 = types.KeyboardButton(lang_dict['back'][user.lang])
        markup__v1.row(btn_1, btn_2)

        today = date.today()
        if(work_end == lang_dict['back'][user.lang]):
            chat_id = message.chat.id
            user = user_dict[chat_id]
            bot.delete_message(message.chat.id, message.message_id-1)
            bot.delete_message(message.chat.id, message.message_id-2)
            msg = bot.send_message(message.chat.id, lang_dict['work_start'][user.lang], reply_markup = markup__v1)
            bot.register_next_step_handler(msg, about_work_start)
            return
        if(work_end == lang_dict['start'][user.lang] or work_end == '/start'):
            process_start(message)
            return
        if not work_end.isdigit() or not int(work_end) > 1970 or not int(work_end) <= today.year:
            msg = bot.reply_to(message, lang_dict['wrong_work_end'][user.lang])
            bot.register_next_step_handler(msg, about_work_end)
            return         
        user.work_end = work_end
        if int(user.work_start) > int(work_end):
            msg = bot.reply_to(message, lang_dict['wrong_work_datas'][user.lang])
            bot.register_next_step_handler(msg, about_work_start)
            return
        #msg = bot.send_message(message.chat.id, 'Отправьте резюме')    
        msg = bot.send_message(message.chat.id, lang_dict['thank_you'][user.lang])   
        send_email(message)
        #bot.register_next_step_handler(msg, send_resume)
        
    except Exception as e:
        msg = bot.reply_to(message, 'Неверные данные!')
        bot.register_next_step_handler(msg, about_work_end)  """         
"""@bot.message_handler(content_types=['document'])
def send_resume(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        resume = message.text
        if(resume =='/start'):
            process_start(message)
            return
        user.resume = resume
        msg = bot.send_message(message.chat.id, lang_dict['thank_you'][user.lang]) 
        send_email(message)
    except Exception as e:
        msg = bot.reply_to(message, 'Неверные данные!')
        bot.register_next_step_handler(msg, about_work_end)      """


    


@bot.callback_query_handler(func=lambda call: True)
def edu(call):
    message = call.message
    try:
        if call.data == 'Высшее':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn = types.KeyboardButton(lang_dict['start'][user.lang])
            markup.row(btn)

            bot.reply_to(message, lang_dict['higher'][user.lang] , reply_markup=markup)
            education = call.data
            user.education = education
            uzb_language(message)
        if call.data == 'Неполное высшее': 
            chat_id = call.message.chat.id
            user = user_dict[chat_id]
            
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn = types.KeyboardButton(lang_dict['start'][user.lang])
            markup.row(btn)

            bot.reply_to(message, lang_dict['incomplete_higher'][user.lang], reply_markup=markup)
            education = call.data           
            user.education = education
            uzb_language(message)
        if call.data == 'Среднее': 
            chat_id = call.message.chat.id
            user = user_dict[chat_id]
            
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn = types.KeyboardButton(lang_dict['start'][user.lang])
            markup.row(btn)

            bot.reply_to(message, lang_dict['secondary'][user.lang], reply_markup=markup)
            education = call.data          
            user.education = education
            uzb_language(message)
        if call.data == 'Неполное среднее':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn = types.KeyboardButton(lang_dict['start'][user.lang])
            markup.row(btn)

            bot.reply_to(message, lang_dict['incomplete_secondary'][user.lang], reply_markup=markup)
            education = call.data   
            user.education = education
            uzb_language(message)
        if call.data == 'Среднее специальное':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn = types.KeyboardButton(lang_dict['start'][user.lang])
            markup.row(btn)

            bot.reply_to(message, lang_dict['secondary_special'][user.lang], reply_markup=markup) 
            education = call.data
            user.education = education
            uzb_language(message) 
           
        if call.data == 'Отлично':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn = types.KeyboardButton(lang_dict['start'][user.lang])
            markup.row(btn)

            bot.reply_to(message, lang_dict['great'][user.lang], reply_markup=markup)
            uz_language = call.data
            
            user.uz_language = uz_language
            rus_language(message)           
        if call.data == 'Хорошо':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn = types.KeyboardButton(lang_dict['start'][user.lang])
            markup.row(btn)

            bot.reply_to(message, lang_dict['good'][user.lang], reply_markup=markup)
            uz_language = call.data
            
            user.uz_language = uz_language
            rus_language(message)            
        if call.data == 'Удовлетворительно':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn = types.KeyboardButton(lang_dict['start'][user.lang])
            markup.row(btn)


            bot.reply_to(message, lang_dict['satisfactorily'][user.lang], reply_markup=markup)
            uz_language = call.data
            
            user.uz_language = uz_language
            rus_language(message)            
        if call.data == 'Отлично знаю':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn = types.KeyboardButton(lang_dict['start'][user.lang])
            markup.row(btn)


            bot.reply_to(message, lang_dict['great'][user.lang], reply_markup=markup)
            ru_language = call.data
            
            user.ru_language = ru_language
            english_language(message)
        if call.data == 'Хорошо знаю':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn = types.KeyboardButton(lang_dict['start'][user.lang])
            markup.row(btn)


            bot.reply_to(message, lang_dict['good'][user.lang], reply_markup=markup)
            ru_language = call.data
            
            user.ru_language = ru_language
            english_language(message)
        if call.data == 'Удовлетворительно знаю':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn = types.KeyboardButton(lang_dict['start'][user.lang])
            markup.row(btn)

            bot.reply_to(message, lang_dict['satisfactorily'][user.lang], reply_markup=markup)
            ru_language = call.data
            
            user.ru_language = ru_language
            english_language(message)

        if call.data == 'Отлично владею':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn = types.KeyboardButton(lang_dict['start'][user.lang])
            markup.row(btn)


            bot.reply_to(message, lang_dict['great'][user.lang], reply_markup=markup)
            en_language = call.data
            
            user.en_language = en_language
            about_work(message)
        if call.data == 'Хорошо владею':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn = types.KeyboardButton(lang_dict['start'][user.lang])
            markup.row(btn)


            bot.reply_to(message, lang_dict['good'][user.lang], reply_markup=markup)
            en_language = call.data
            
            user.en_language = en_language
            about_work(message)
        if call.data == 'Удовлетворительно владею':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn = types.KeyboardButton(lang_dict['start'][user.lang])
            markup.row(btn)

            bot.reply_to(message, lang_dict['satisfactorily'][user.lang], reply_markup=markup)
            en_language = call.data
            
            user.en_language = en_language
            about_work(message)
        

        if call.data == 'да':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn = types.KeyboardButton(lang_dict['start'][user.lang])
            markup.row(btn)


            bot.reply_to(message, lang_dict['yes'][user.lang] , reply_markup=markup)
            work = call.data
             
            user.work = work
            say_experience(message)

        if call.data == 'нет':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn = types.KeyboardButton(lang_dict['start'][user.lang])
            markup.row(btn)


            bot.reply_to(message, lang_dict['no'][user.lang] , reply_markup=markup)
            work = call.data
             
            user.work = work
            say_thanks(message)
        if call.data == 'bck_house':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]
            markup__v1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn_1 = types.KeyboardButton(lang_dict['start'][user.lang])
            btn_2 = types.KeyboardButton(lang_dict['back'][user.lang])
            markup__v1.row(btn_1, btn_2)
            msg = bot.send_message(message.chat.id, lang_dict['house'][user.lang], reply_markup = markup__v1)
            bot.register_next_step_handler(msg, ask_house) 
        if call.data == 'bck_edu':          
            education_1(message)
                                             
        if call.data == 'bck_uz':
            uzb_language(message)
            
        if call.data == 'bck_ru':             
            rus_language(message)

        if call.data == 'bck_eng':
            english_language(message)    



            
                          
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)      
          
    except Exception as e:    
        bot.reply_to(message, "ERROR")       

    


def send_email(message):
    try:
        msg = MIMEMultipart("alternative")
        username = "{0.username}".format(message.from_user, bot.get_me())
        fromaddr = "bukanov1234@mail.ru"
        mypass = "cRYfj13YTp65wmluZxJU"
        toaddr = "rezume_BOT@beeline.uz"
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Отправитель: Telegram bot"  # + str(message.chat.id)
        body = "Message: Telegram_bot \n\n"
    
        global user_dict
        global name
        global birthday
        global number
        global town
        global district
        global quarter
        global house
        global education
    
        chat_id = message.chat.id
        user = user_dict[chat_id]
        print(user.birthday)
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        </head>
        <body>
        
        <h1>Заявка:</h1>
        
        <h2>Имя: {user.name}</h2>
        <h2>День рождения: {user.birthday}</h2>
        <h2>Номер телефона: {user.number}</h2>
        <h2>Адресные данные:</h2>
        <h2>Город: {user.town}</h2>
        <h2>Район: {user.district}</h2>
        <h2>Квартал или улица: {user.quarter}</h2>
        <h2>Номер дома: {user.house}</h2>
        <h2>Образование: {user.education}</h2>
        <h2>Знание Узбекского языка: {user.uz_language}</h2>
        <h2>Уровень владения Русским языком: {user.ru_language}</h2>
        <h2>Уровень владения Английским языком: {user.en_language}</h2>
        <h2>Вы работали ранее: {user.work}</h2> 
        <h2>Организации в которых работали ранее, периоды работы и должности: {user.work_experience}</h2> 
        

      
        </body>
        </html>
        """
        text = bs(html, "html.parser").text
        msg.attach(MIMEText(text, 'plain'))
        msg.attach(MIMEText(html, 'html', 'utf-8'))
        server = smtplib.SMTP_SSL('smtp.mail.ru:465')
        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        server.login(msg['From'], mypass)
        text = msg.as_string()
        server.sendmail(msg['From'], msg['To'], text)
        server.quit()
        bot.reply_to(message, lang_dict['sendmail'][user.lang])
        print("Successfully sent email")

        markup_start = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn = types.KeyboardButton('/start')
        markup_start.row(btn)

        bot.send_message(message.chat.id, lang_dict['again'][user.lang], reply_markup=markup_start)
        
    except Exception as e:
        bot.reply_to(message, "ERROR")




def send_email_without_work(message):
    try:
        msg = MIMEMultipart("alternative")
        username = "{0.username}".format(message.from_user, bot.get_me())
        fromaddr = "bukanov1234@mail.ru"
        mypass = "cRYfj13YTp65wmluZxJU"
        toaddr = "rezume_BOT@beeline.uz"
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Отправитель: Telegram bot"  # + str(message.chat.id)
        body = "Message: Telegram_bot \n\n"

    
        global user_dict
        global name
        global birthday
        global number
        global town
        global district
        global quarter
        global house
        global education
        global work
        chat_id = message.chat.id
        user = user_dict[chat_id]

        print(user.birthday)
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        </head>
        <body>
        
        <h1>Заявка:</h1>
            
        <h2>Имя: {user.name}</h2>
        <h2>День рождения: {user.birthday}</h2>
        <h2>Номер телефона: {user.number}</h2>
        <h2>Адресные данные:</h2>
        <h2>Город: {user.town}</h2>
        <h2>Район: {user.district}</h2>
        <h2>Квартал или улица: {user.quarter}</h2>
        <h2>Номер дома: {user.house}</h2>
        <h2>Образование: {user.education}</h2>
        <h2>Знание Узбекского языка: {user.uz_language}</h2>
        <h2>Уровень владения Русским языком: {user.ru_language}</h2>
        <h2>Уровень владения Английским языком: {user.en_language}</h2>
        <h2>Вы работали ранее: {user.work}</h2> 
      
        </body>
        </html>
        """
        text = bs(html, "html.parser").text
        msg.attach(MIMEText(text, 'plain'))
        msg.attach(MIMEText(html, 'html', 'utf-8'))
        server = smtplib.SMTP_SSL('smtp.mail.ru:465')
        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        server.login(msg['From'], mypass)
        text = msg.as_string()
        server.sendmail(msg['From'], msg['To'], text)
        server.quit()
        bot.reply_to(message, lang_dict['sendmail'][user.lang])
        print("Successfully sent email")

        markup_start = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn = types.KeyboardButton('/start')
        markup_start.row(btn)

        bot.send_message(message.chat.id, lang_dict['again'][user.lang], reply_markup=markup_start)

        
    except Exception as e:
        bot.reply_to(message, "ERROR")


  



bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()        

bot.polling()


