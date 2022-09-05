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

lang_dict = {'ask_name': {'Русский 🇷🇺': 'Просим указать ФИО(полностью):', 'Ozbek tili 🇺🇿': 'Toliq FISh ni kiritishingizni soraymiz:' },
             'wrong_name': {'Русский 🇷🇺': 'Вы неверно ввели данные!!! Возможно написание фамилии, имени и отчества или просто фамилии и имени(через пробелы)', 'Ozbek tili 🇺🇿': 'Ism, familiya va otasining ismi boshliqlar orqali yozilgan kamida uchta soz bolishi kerak' },
             'ask_birthday': {'Русский 🇷🇺': 'Дата Вашего рождения:', 'Ozbek tili 🇺🇿': 'Tugilgan yil, oy va sanangizni kiriting:' },
             'wrong_birthday': {'Русский 🇷🇺': 'Вы ввели неправильную дату!', 'Ozbek tili 🇺🇿': 'Siz notogri sanani kiritdingiz!' },
             'number': {'Русский 🇷🇺': 'Укажите контактный номер, чтобы мы могли связаться с Вами:', 'Ozbek tili 🇺🇿': 'Siz bilan boglana olishimiz uchun kontakt raqami kiriting:' },
             'wrong_number': {'Русский 🇷🇺': 'Неверный формат номера!', 'Ozbek tili 🇺🇿': 'Notogri raqam formati!' },
             'adress': {'Русский 🇷🇺': 'Укажите адрес проживания', 'Ozbek tili 🇺🇿': 'Yashash manzilingizni kiriting:' },
             'town': {'Русский 🇷🇺': 'Город или область:', 'Ozbek tili 🇺🇿': 'Shahar yoki viloyat:' },
             'wrong_town': {'Русский 🇷🇺': 'Название города должно состоять из букв и может быть несколькими словами', 'Ozbek tili 🇺🇿': 'Shahar nomi harflardan iborat bolishi kerak va bir necha soz bolishi mumkin' },
             'district': {'Русский 🇷🇺': 'Район:', 'Ozbek tili 🇺🇿': 'Tuman:' },
             'wrong_district': {'Русский 🇷🇺': 'Название района должно состоять из букв и может быть несколькими словами', 'Ozbek tili 🇺🇿': 'Tuman nomi harflardan iborat bolishi kerak va bir necha soz bolishi mumkin' },
             'quarter': {'Русский 🇷🇺': 'Квартал или улица:', 'Ozbek tili 🇺🇿': 'Kvartal raqami yoki kochaning nomi:' },
             'wrong_quarter': {'Русский 🇷🇺': 'Название квартала или улицы должно состоять из букв или цифр', 'Ozbek tili 🇺🇿': 'Blok yoki kochaning nomi harflar yoki raqamlardan iborat bolishi kerak' },
             'house': {'Русский 🇷🇺': 'Дом:', 'Ozbek tili 🇺🇿': 'Uy:' },
             'wrong_house': {'Русский 🇷🇺': 'Название дома должно состоять из цифр или букв', 'Ozbek tili 🇺🇿': 'Uyning nomi raqamlar yoki harflardan iborat bolishi kerak' },
             'education': {'Русский 🇷🇺': 'Укажите уровень образования:', 'Ozbek tili 🇺🇿': 'Talim darajasini korsating:' },
             'uzb_language': {'Русский 🇷🇺': 'Степень владения Узбекским языком:', 'Ozbek tili 🇺🇿': 'Ozbek tilini bilish darajasi:' },
             'rus_language': {'Русский 🇷🇺': 'Степень владения Русским языком:', 'Ozbek tili 🇺🇿': 'Rus tilini bilish darajasi:' },
             'higher':  {'Русский 🇷🇺': 'Высшее', 'Ozbek tili 🇺🇿': 'oliy' },
             'incomplete_higher':  {'Русский 🇷🇺': 'Неполное высшее', 'Ozbek tili 🇺🇿': 'Tugallanmagan oliy' },
             'secondary':  {'Русский 🇷🇺': 'Среднее', 'Ozbek tili 🇺🇿': 'Orta' },
             'incomplete_secondary':  {'Русский 🇷🇺': 'Неполное среднее', 'Ozbek tili 🇺🇿': 'Tugallanmagan orta' },
             'secondary_special':  {'Русский 🇷🇺': 'Среднее специальное', 'Ozbek tili 🇺🇿': 'Orta maxsus' },
             'great':  {'Русский 🇷🇺': 'Отлично', 'Ozbek tili 🇺🇿': 'Alo' },
             'good':  {'Русский 🇷🇺': 'Хорошо', 'Ozbek tili 🇺🇿': 'Yaxshi' },
             'satisfactorily':  {'Русский 🇷🇺': 'Удовлетворительно', 'Ozbek tili 🇺🇿': 'Qoniqarli' },
             'work':  {'Русский 🇷🇺': 'Опыт работы: Есть или Нет?', 'Ozbek tili 🇺🇿': 'Ish tajribangiz: Bor yoki Yoq' },
             'organization':  {'Русский 🇷🇺': 'Укажите название организации:', 'Ozbek tili 🇺🇿': 'Tashkilot nomini kiriting' },
             'wrong_organization':  {'Русский 🇷🇺': 'Название организации должно состоять из букв или цифр и может быть несколькими словами', 'Ozbek tili 🇺🇿': 'Tashkilot nomi harflar yoki raqamlardan iborat bolishi kerak va bir nechta sozlar bolishi mumkin' },
             'job_title':  {'Русский 🇷🇺': 'Должность:', 'Ozbek tili 🇺🇿': 'Lavozim:' },
             'wrong_job_title':  {'Русский 🇷🇺': 'Название специальности должно состоять из букв, также в нём могут быть пробелы и цифры', 'Ozbek tili 🇺🇿': 'Mutaxassislikning nomi harflardan iborat bolishi kerak, unda boshliqlar va raqamlar ham bolishi mumkin' },
             'work_start':  {'Русский 🇷🇺': 'Укажите год, когда вы устроились в организацию:', 'Ozbek tili 🇺🇿': 'Siz tashkilotga ishga kirgan yilni kiriting:' },
             'wrong_work_start':  {'Русский 🇷🇺': 'Год когда вы устроились в организацию должен быть четырёхзначным числом от 1990 до текущего года ', 'Ozbek tili 🇺🇿': 'Tashkilotga ishga kirgan yilingiz 1990 va joriy yil oraligidagi tort xonali raqam bolishi kerak' },
             'work_end':  {'Русский 🇷🇺': 'Укажите год, когда Вы ушли из организации:', 'Ozbek tili 🇺🇿': 'Siz tashkilotdan boshagan yilni korsating:' },
             'wrong_work_end':  {'Русский 🇷🇺': 'Год ухода с организации должен быть четырёхзначным числом от 1990 до текущего года', 'Ozbek tili 🇺🇿': 'Tashkilotdan boshagan yilingiz 1990 va joriy yil oraligidagi tort xonali son bolishi kerak' },
             'wrong_work_datas':  {'Русский 🇷🇺': ' Вы не могли уйти с работы раньше чем на неё устроились.Год когда вы устроились на работу?', 'Ozbek tili 🇺🇿': 'Siz tashkilotdan boshagan yilingiz - ishga kirgan yilingizdan oldin bolishi mumkin emas. Siz tashkilotga ishga kirgan yilni qaytadan kiriting:' },
             'thank_you': {'Русский 🇷🇺': 'Спасибо за прохождение опроса!!!', 'Ozbek tili 🇺🇿': 'Sorovnomadan otganingiz uchun minnatdormiz!!!' },
             'sendmail': {'Русский 🇷🇺': 'Ваше резюме отправлено на рассмотрение.\n\nПодготовьтесь к телефонному собеседованию\n\nСписок примерных вопросов:\n1.Расскажите о себе\n2.Какими качествами должен обладать сотрудник контакт-центра\n3.Ваши ожидания по заработной плате', 'Ozbek tili 🇺🇿': 'Sizning malumotlaringiz korib chiqish uchun yuborildi.\n\n Telefon orqali suhbatdan otishga tayyorlaning \n\n Berilishi mumkin bolgan savollardan namunalar: \n1. Ozingiz haqingizda gapirib bering.\n2. Kontakt markazi xodimi qanday fazilatlarga ega bolishi kerak?\n 3. Qancha miqdordagi maosh sizni qoniqtirgan bolardi?' },
             'again':  {'Русский 🇷🇺': 'Если хотите пройти опрос заново нажмите на кнопку: "/start"" ', 'Ozbek tili 🇺🇿': 'Sorovnomadan qaytadan otishni istasangiz quyidagi tugmani bosing: "/start"' },
             'checker':  {'Русский 🇷🇺': 'Выберите вариант кнопкой', 'Ozbek tili 🇺🇿': 'Tugmani bosib variantni tanlang' },
             'yes':  {'Русский 🇷🇺': 'да', 'Ozbek tili 🇺🇿': 'ha' },
             'no':  {'Русский 🇷🇺': 'нет', 'Ozbek tili 🇺🇿': 'yoq' },
             'back':  {'Русский 🇷🇺': 'Назад', 'Ozbek tili 🇺🇿': 'Orqaga' },
             'start':  {'Русский 🇷🇺': 'Начать сначала', 'Ozbek tili 🇺🇿': 'Yana boshlang' },
             'knopka':  {'Русский 🇷🇺': 'На следующие вопросы отвечайте выбором одного из вариантов!', 'Ozbek tili 🇺🇿': 'Quyidagi savollarga variantlardan birini tanlash bilan javob bering!' }

            
             
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
        #self.resume = None



markupp = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
btn1 = types.KeyboardButton('Русский 🇷🇺')
btn2 = types.KeyboardButton('Ozbek tili 🇺🇿')
markupp.row(btn1, btn2)


@bot.message_handler(commands=['start'])
def process_start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    msg = bot.send_message(message.chat.id,
                           'Здравствуйте!\nПожалуйста, выберите язык\n\nAssalomu aleykum!\nIltimos, tilni tanlang',
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
    elif(message.text=='Yana boshlang'):
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
def about_work(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    markup_o = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton(lang_dict['yes'][user.lang], callback_data='да')
    item2 = types.InlineKeyboardButton(lang_dict['no'][user.lang], callback_data='нет')
    item3 = types.InlineKeyboardButton(lang_dict['back'][user.lang], callback_data='bck_ru')
    markup_o.row(item1, item2)
    markup_o.row(item3)
    bot.send_message(message.chat.id, lang_dict['work'][user.lang], reply_markup=markup_o)

@bot.message_handler(content_types = ['text'])
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
        if not work_start.isdigit() or not int(work_start) > 1990 or not int(work_start) <= today.year:
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
        if not work_end.isdigit() or not int(work_end) > 1990 or not int(work_end) <= today.year:
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
        bot.register_next_step_handler(msg, about_work_end)           
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
            about_work(message)
        if call.data == 'Хорошо знаю':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn = types.KeyboardButton(lang_dict['start'][user.lang])
            markup.row(btn)


            bot.reply_to(message, lang_dict['good'][user.lang], reply_markup=markup)
            ru_language = call.data
            
            user.ru_language = ru_language
            about_work(message)
        if call.data == 'Удовлетворительно знаю':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn = types.KeyboardButton(lang_dict['start'][user.lang])
            markup.row(btn)

            bot.reply_to(message, lang_dict['satisfactorily'][user.lang], reply_markup=markup)
            ru_language = call.data
            
            user.ru_language = ru_language
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
            ask_organization(message)

        if call.data == 'нет':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn = types.KeyboardButton(lang_dict['start'][user.lang])
            markup.row(btn)


            bot.reply_to(message, lang_dict['no'][user.lang] , reply_markup=markup)
            work = call.data
             
            user.work = work
            send_email_without_work(message)
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

            
                          
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)      
          
    except Exception as e:    
        bot.reply_to(message, "ERROR")       

    


def send_email(message):
    try:
        msg = MIMEMultipart("alternative")
        username = "{0.username}".format(message.from_user, bot.get_me())
        fromaddr = "bukanov1234@mail.ru"
        mypass = "cRYfj13YTp65wmluZxJU"
        toaddr = "ShAbdukhamidov@beeline.uz"
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
        <h2>Организация в которой работал ранее: {user.organization}</h2>
        <h2>Должность: {user.job_title}</h2>    
        <h2>Период работы: {user.work_start} - {user.work_end}</h2> 

      
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
        toaddr = "ShAbdukhamidov@beeline.uz"
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


