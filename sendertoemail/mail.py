import telebot
import os
import requests
import smtplib
import ssl
import re
import telebot_calendar
from telegramcalendar import create_calendar
import datetime
from datetime import date
import configure
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import types
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.message import EmailMessage
from email.mime.base import MIMEBase
from bs4 import BeautifulSoup as bs
import phonenumbers
from phonenumbers import carrier, timezone, geocoder


bot = telebot.TeleBot(configure.config['token'])


user_dict = {}
current_shown_dates={}

lang_dict = {'ask_name': {'Русский': 'Пожалуйста, напишите ФИО(через пробелы):', 'Ozbek tili': 'Iltimos, toliq ismingizni yozing (boshliqlar orqali):' },
             'wrong_name': {'Русский': 'Имя, Фамилия и Отчество должны быть минимум тремя словами, написанными через пробелы', 'Ozbek tili': 'Ism, familiya va otasining ismi boshliqlar orqali yozilgan kamida uchta soz bolishi kerak' },
             'ask_birthday': {'Русский': 'Дата Вашего рождения:', 'Ozbek tili': 'Tugilgan kuningiz:' },
             'wrong_birthday': {'Русский': 'Вы ввели неправильную дату!', 'Ozbek tili': 'Siz notogri sanani kiritdingiz!' },
             'number': {'Русский': 'Укажите контактный номер, чтобы мы могли связаться с Вами:', 'Ozbek tili': 'Siz bilan boglanishimiz uchun aloqa raqamini kiriting:' },
             'wrong_number': {'Русский': 'Неверный формат номера!', 'Ozbek tili': 'Notogri raqam formati!' },
             'adress': {'Русский': 'Укажите адрес:', 'Ozbek tili': 'Manzilni korsating' },
             'town': {'Русский': 'Город или область:', 'Ozbek tili': 'Shahar yoki viloyat:' },
             'wrong_town': {'Русский': 'Название города должно состоять из букв и может быть несколькими словами', 'Ozbek tili': 'Shahar nomi harflardan iborat bolishi kerak va bir necha soz bolishi mumkin' },
             'district': {'Русский': 'Район:', 'Ozbek tili': 'Tuman:' },
             'wrong_district': {'Русский': 'Название района должно состоять из букв и может быть несколькими словами', 'Ozbek tili': 'Tuman nomi harflardan iborat bolishi kerak va bir necha soz bolishi mumkin' },
             'quarter': {'Русский': 'Квартал или улица:', 'Ozbek tili': 'Blok yoki kocha:' },
             'wrong_quarter': {'Русский': 'Название квартала или улицы должно состоять из букв или цифр', 'Ozbek tili': 'Blok yoki kochaning nomi harflar yoki raqamlardan iborat bolishi kerak' },
             'house': {'Русский': 'Дом:', 'Ozbek tili': 'Uy:' },
             'wrong_house': {'Русский': 'Название дома должно состоять из цифр или букв', 'Ozbek tili': 'Uyning nomi raqamlar yoki harflardan iborat bolishi kerak' },
             'education': {'Русский': 'Укажите уровень образования:', 'Ozbek tili': 'Talim darajasini korsating:' },
             'uzb_language': {'Русский': 'Степень владения Узбекским языком:', 'Ozbek tili': 'Ozbek tilini bilish darajasi:' },
             'rus_language': {'Русский': 'Степень владения Русским языком:', 'Ozbek tili': 'Rus tilini bilish darajasi:' },
             'higher':  {'Русский': 'Высшее', 'Ozbek tili': 'oliy' },
             'incomplete_higher':  {'Русский': 'Неполное высшее', 'Ozbek tili': 'toliq bolmagan oliy' },
             'secondary':  {'Русский': 'Среднее', 'Ozbek tili': 'Orta' },
             'incomplete_secondary':  {'Русский': 'Неполное среднее', 'Ozbek tili': 'toliq bolmagan orta' },
             'secondary_special':  {'Русский': 'Среднее специальное', 'Ozbek tili': 'Orta maxsus' },
             'great':  {'Русский': 'Отлично', 'Ozbek tili': 'Ajoyib' },
             'good':  {'Русский': 'Хорошо', 'Ozbek tili': 'Yaxshi' },
             'satisfactorily':  {'Русский': 'Удовлетворительно', 'Ozbek tili': 'Qoniqarli' },
             'organization':  {'Русский': 'Где вы работали ранее? Укажите название организации', 'Ozbek tili': 'Ilgari qayerda ishladingiz? Tashkilot nomini korsating' },
             'wrong_organization':  {'Русский': 'Название организации должно состоять из букв или цифр и может быть несколькими словами', 'Ozbek tili': 'Tashkilot nomi harflar yoki raqamlardan iborat bolishi kerak va bir nechta sozlar bolishi mumkin' },
             'job_title':  {'Русский': 'Должность:', 'Ozbek tili': 'Lavozim:' },
             'wrong_job_title':  {'Русский': 'Название специальности должно состоять из букв, также в нём могут быть пробелы и цифры', 'Ozbek tili': 'Mutaxassislikning nomi harflardan iborat bolishi kerak, unda boshliqlar va raqamlar ham bolishi mumkin' },
             'work_start':  {'Русский': 'Укажите год, когда вы устроились в организацию:', 'Ozbek tili': 'Tashkilotga ishga kirgan yilingizni korsating:' },
             'wrong_work_start':  {'Русский': 'Год поступления на работу должен быть четырёхзначным числом от 1990 до текущего года ', 'Ozbek tili': 'Ishga qabul qilingan yil 1990 yildan joriy yilgacha tort xonali raqam bolishi kerak' },
             'work_end':  {'Русский': 'Укажите год, когда Вы ушли из организации:', 'Ozbek tili': 'Tashkilotni tark etgan yilingizni korsating:' },
             'wrong_work_end':  {'Русский': 'Год ухода с работы должен быть четырёхзначным числом от 1990 до текущего года', 'Ozbek tili': 'Ishdan ketgan yil 1990 yildan joriy yilgacha tort xonali raqam bolishi kerak' },
             'wrong_work_datas':  {'Русский': ' Вы не могли уйти с работы раньше чем на неё устроились.Год когда вы устроились на работу?', 'Ozbek tili': 'Siz ishga joylashishdan oldin ishingizni tark eta olmadingiz.Yil qachon ish topdingiz?' },
             'thank_you': {'Русский': 'Спасибо за прохождение опроса!!!', 'Ozbek tili': 'Sorovni yakunlaganingiz uchun tashakkur!!!' },
             'sendmail': {'Русский': 'Наша команда в скором времени с Вами свяжется.\n\nПодготовьтесь к телефонному собеседованию\n\nСписок примерных вопросов:\n1.Расскажите о себе\n2.Какими качествами должен обладать сотрудник контакт-центра\n3.Ваши ожидания по заработной плате', 'Ozbek tili': 'Tez orada jamoamiz siz bilan boglanadi.\n\n telefon orqali suhbatga tayyorlaning \n\n namunaviy savollar royxati: \n1.Ozingiz haqingizda bizga xabar bering\n2.Aloqa markazining xodimi\n3 qanday fazilatlarga ega bolishi kerak.Sizning ish haqingiz boyicha taxminlaringiz' },
             'again':  {'Русский': 'Если хотите пройти опрос заново нажмите на кнопку /start ', 'Ozbek tili': 'Agar siz sorovnomani qayta otkazmoqchi bolsangiz, /start tugmasini yana bosing' },
             'checker':  {'Русский': 'Выберите вариант кнопкой', 'Ozbek tili': 'Tugmani bosib variantni tanlang' }
             
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
        self.organization = None
        self.job_title = None
        self.work_start = None
        self.work_end = None


markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn = types.KeyboardButton('/start')
markup.row(btn)

markupp = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
btn1 = types.KeyboardButton('Русский')
btn2 = types.KeyboardButton('Ozbek tili')
markupp.row(btn1, btn2)


@bot.message_handler(commands=['start'])

def process_start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    msg = bot.send_message(message.chat.id,
                           'Здравствуйте!\nПожалуйста выберите язык\n\nAssalomu aleykum!\nIltimos, tilni tanlang',
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
        msg = bot.reply_to(message,
                        lang_dict['ask_name'][user.lang],
                        reply_markup = markup)
        bot.register_next_step_handler(msg, ask_name)  
    except KeyError:
        msg = bot.reply_to(message, "Выберите один из вариантов 'Русский' или 'Ozbek tili'\n\n 'Русский' yoki 'Ozbek tili' parametrlaridan birini tanlang ")
        bot.register_next_step_handler(msg, ask_language)

       

def ask_name(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = user_dict[chat_id]
        if(name=='/start'):
            process_start(message)
            return
        if not(name.count(' ') >= 2 and name.count(' ') <= 3):
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
        handle_calendar_command(message)
    except Exception as e:    
        bot.reply_to(message, 'Упс!')

@bot.message_handler(func=lambda call:True, content_types=['text'])
def handle_calendar_command(message):
    try:
        now = datetime.datetime.now()
        chat_id = message.chat.id
        user = user_dict[chat_id]
        date = (now.year - 25, now.month)
        current_shown_dates[chat_id] = date
        markup = create_calendar(now.year - 25, now.month)
        bot.send_message(message.chat.id, lang_dict['ask_birthday'][user.lang], reply_markup=markup)
        birthday = message.text 
        user.birthday = birthday
        
    except Exception:
        bot.reply_to(message, 'Упс!')
    





@bot.callback_query_handler(func=lambda call: 'DAY' in call.data[0:13])
def handle_day_query(call):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    last_sep = call.data.rfind(';') + 1
    if saved_date is not None:
        user = user_dict[chat_id]
        day = call.data[last_sep:]
        date = datetime.datetime(int(saved_date[0]), int(saved_date[1]), int(day))
        msg = bot.send_message(chat_id=chat_id, text=str(date))
        birthday = call.data
        user.birthday = birthday       
        bot.answer_callback_query(call.id, text="")
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)      
        msg = bot.send_message(chat_id=chat_id, text=lang_dict['number'][user.lang])
        bot.register_next_step_handler(msg, ask_number)
    

@bot.callback_query_handler(func=lambda call: 'MONTH' in call.data)
def handle_month_query(call):
    info = call.data.split(';')
    month_opt = info[0].split('-')[0]
    year, month = int(info[1]), int(info[2])
    chat_id = call.message.chat.id
    user = user_dict[chat_id]

    if month_opt == 'PREV':
        month -= 1

    elif month_opt == 'NEXT':
        month += 1

    if month < 1:
        month = 12
        year -= 1

    if month > 12:
        month = 1
        year += 1

    date = (year, month)
    current_shown_dates[chat_id] = date
    markup = create_calendar(year, month)
    bot.edit_message_text(lang_dict['ask_birthday'][user.lang], call.from_user.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: 'YEAR' in call.data)
def handle_year_query(call):

    info = call.data.split(';')
    year_opt = info[0].split('-')[0]
    year, month = int(info[1]), int(info[2])
    chat_id = call.message.chat.id
    user = user_dict[chat_id]

    if year_opt == 'PREV':
        year -= 1

    elif year_opt == 'NEXT':
        year += 1

    date = (year, month)
    current_shown_dates[chat_id] = date
    markup = create_calendar(year, month)
    bot.edit_message_text(lang_dict['ask_birthday'][user.lang], call.from_user.id, call.message.message_id, reply_markup=markup)



@bot.callback_query_handler(func=lambda call: "IGNORE" in call.data)
def ignore(call):
    bot.answer_callback_query(call.id, text="Что-то пошло не так")





def ask_number(message):
    try:
        chat_id = message.chat.id
        number = message.text
        user = user_dict[chat_id]
        if(number=='/start'):
            process_start(message)
            return
        my_number = phonenumbers.parse(number, "UZ")
            
        if phonenumbers.is_valid_number(my_number)==False:
            msg = bot.reply_to(message, lang_dict['wrong_number'][user.lang])
            bot.register_next_step_handler(msg, ask_number)
            return
        if len(str(number))!=13:
            msg = bot.reply_to(message, lang_dict['wrong_number'][user.lang])
            bot.register_next_step_handler(msg, ask_number)
            return       

        user.number = number
        msg = bot.reply_to(message, lang_dict['adress'][user.lang])
        bot.send_message(message.chat.id, lang_dict['town'][user.lang], reply_markup=markup)
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
        if(town=='/start'):
            process_start(message)
            return  
        if not all(x.isalpha() or x.isspace() for x in town):
            msg = bot.reply_to(message, lang_dict['wrong_town'][user.lang])
            bot.register_next_step_handler(msg, ask_town) 
            return          
        user = user_dict[chat_id]
        user.town = town   
        msg = bot.reply_to(message, lang_dict['district'][user.lang]) 
        bot.register_next_step_handler(msg, ask_district)
    except Exception as e:
        bot.reply_to(message, 'Упс!')

def ask_district(message):
    try:
        chat_id = message.chat.id
        district = message.text
        user = user_dict[chat_id]
        if(district=='/start'):
            process_start(message)
            return
        if not all(x.isalpha() or x.isspace() for x in district):
            msg = bot.reply_to(message, lang_dict['wrong_district'][user.lang])
            bot.register_next_step_handler(msg, ask_district) 
            return        
            
        user.district = district  
        msg = bot.reply_to(message, lang_dict['quarter'][user.lang]) 
        bot.register_next_step_handler(msg, ask_quarter)
    except Exception as e:
        bot.reply_to(message, 'Упс!')

def ask_quarter(message):
    try:
        chat_id = message.chat.id
        quarter = message.text
        user = user_dict[chat_id]
        if(quarter=='/start'):
            process_start(message)
            return
        if not all(x.isalnum() or x.isspace() for x in quarter):
            msg = bot.reply_to(message, lang_dict['wrong_quarter'][user.lang])
            bot.register_next_step_handler(msg, ask_quarter) 
            return        
            
        user.quarter = quarter  
        msg = bot.reply_to(message, lang_dict['house'][user.lang]) 
        bot.register_next_step_handler(msg, ask_house)
    except Exception as e:
        bot.reply_to(message, 'Упс!')    

def ask_house(message):
    try:
        chat_id = message.chat.id
        house = message.text
        user = user_dict[chat_id]
        if(house=='/start'):
            process_start(message)
            return
        if not all(x.isalnum() or x.isspace() for x in house):
            msg = bot.reply_to(message, lang_dict['wrong_house'][user.lang])
            bot.register_next_step_handler(msg, ask_house) 
            return              
        user.house = house 
        education(message)
    except Exception as e: 
        bot.reply_to(message, 'Упс!')

@bot.message_handler(content_types = ['text'])
def education(message):  
    chat_id = message.chat.id
    user = user_dict[chat_id]
    markup1 = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton(lang_dict['higher'][user.lang], callback_data='Высшее')
    item2 = types.InlineKeyboardButton(lang_dict['incomplete_higher'][user.lang], callback_data='Неполное высшее')
    item3 = types.InlineKeyboardButton(lang_dict['secondary'][user.lang], callback_data='Среднее')
    item4 = types.InlineKeyboardButton(lang_dict['incomplete_secondary'][user.lang], callback_data='Неполное среднее')
    item5 = types.InlineKeyboardButton(lang_dict['secondary_special'][user.lang], callback_data='Среднее специальное')
    markup1.add(item1, item2, item3, item4, item5)
    bot.reply_to(message, lang_dict['education'][user.lang] , reply_markup=markup1)


   

    

@bot.message_handler(content_types = ['text'])
def uzb_language(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    markup2 = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton(lang_dict['great'][user.lang], callback_data='Отлично')
    item2 = types.InlineKeyboardButton(lang_dict['good'][user.lang], callback_data='Хорошо')
    item3 = types.InlineKeyboardButton(lang_dict['satisfactorily'][user.lang], callback_data='Удовлетворительно')
    markup2.add(item1, item2, item3)
    bot.reply_to(message, lang_dict['uzb_language'][user.lang], reply_markup=markup2)       
    
       
@bot.message_handler(content_types = ['text'])
def rus_language(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    markup3 = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton(lang_dict['great'][user.lang], callback_data='Отлично знаю')
    item2 = types.InlineKeyboardButton(lang_dict['good'][user.lang], callback_data='Хорошо знаю')
    item3 = types.InlineKeyboardButton(lang_dict['satisfactorily'][user.lang], callback_data='Удовлетворительно знаю')
    markup3.add(item1, item2, item3)
    bot.reply_to(message, lang_dict['rus_language'][user.lang] , reply_markup=markup3) 
 
@bot.message_handler(content_types = ['text'])
def about_work(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    msg = bot.reply_to(message, lang_dict['organization'][user.lang], reply_markup=markup)
    bot.register_next_step_handler(msg, about_organization)            
            
       
@bot.message_handler(content_types = ['text'])
def about_organization(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        organization = message.text
        if(organization =='/start'):
            process_start(message)
            return
        if not all(x.isalnum() or x.isspace() for x in organization):
            msg = bot.reply_to(message, lang_dict['wrong_organization'][user.lang])
            bot.register_next_step_handler(msg, about_organization) 
            return   
        user.organization = organization   
        msg = bot.reply_to(message, lang_dict['job_title'][user.lang]) 
        bot.register_next_step_handler(msg, about_job_title)
    except Exception as e:
        bot.reply_to(message, 'Упс!')
def about_job_title(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        job_title = message.text
        if(job_title =='/start'):
            process_start(message)
            return
        if not all(x.isalpha() or x.isspace() for x in job_title):
            msg = bot.reply_to(message, lang_dict['wrong_job_title'][user.lang])
            bot.register_next_step_handler(msg, about_job_title) 
            return   
        user.job_title = job_title   
        msg = bot.reply_to(message, lang_dict['work_start'][user.lang]) 
        bot.register_next_step_handler(msg, about_work_start)
    except Exception as e:
        bot.reply_to(message, 'Упс!')

def about_work_start(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        work_start = message.text
        today = date.today()
        if(work_start =='/start'):
            process_start(message)
            return
        if not work_start.isdigit() or not int(work_start) > 1970 or not int(work_start) <= today.year:
            msg = bot.reply_to(message, lang_dict['wrong_work_start'][user.lang])
            bot.register_next_step_handler(msg, about_work_start)
            return   
        user.work_start = work_start  
        msg = bot.reply_to(message, lang_dict['work_end'][user.lang]) 
        bot.register_next_step_handler(msg, about_work_end)
    except Exception as e:
        bot.reply_to(message, 'Упс!')
def about_work_end(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        work_end = message.text
        today = date.today()
        if(work_end =='/start'):
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
        msg = bot.reply_to(message, lang_dict['thank_you'][user.lang])   
        send_email(message)
        
    except Exception as e:
        bot.reply_to(message, 'Упс!')        



    


@bot.callback_query_handler(func=lambda call: True)
def edu(call):
    message = call.message
    try:
        if call.data == 'Высшее':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]
            bot.reply_to(message, lang_dict['higher'][user.lang] , reply_markup=markup)
            education = call.data
            if(education=='/start'):
                process_start(message)
                return  
            user.education = education
            uzb_language(message)
        if call.data == 'Неполное высшее': 
            chat_id = call.message.chat.id
            user = user_dict[chat_id]
            bot.reply_to(message, lang_dict['incomplete_higher'][user.lang], reply_markup=markup)
            education = call.data
            if(education=='/start'):
                process_start(message)
                return  
            user.education = education
            uzb_language(message)
        if call.data == 'Среднее': 
            chat_id = call.message.chat.id
            user = user_dict[chat_id]
            bot.reply_to(message, lang_dict['secondary'][user.lang], reply_markup=markup)
            education = call.data
            if(education=='/start'):
                process_start(message)
                return  
            user.education = education
            uzb_language(message)
        if call.data == 'Неполное среднее':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]
            bot.reply_to(message, lang_dict['incomplete_secondary'][user.lang], reply_markup=markup)
            education = call.data
            if(education=='/start'):    
                process_start(message)
                return      
            user.education = education
            uzb_language(message)
        if call.data == 'Среднее специальное':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]
            bot.reply_to(message, lang_dict['secondary_special'][user.lang], reply_markup=markup) 
            education = call.data
            if(education=='/start'):
                process_start(message)
                return  
            user.education = education
            uzb_language(message)            
        if call.data == 'Отлично':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]
            bot.reply_to(message, lang_dict['great'][user.lang], reply_markup=markup)
            uz_language = call.data
            if(uz_language=='/start'):
                process_start(message)
                return  
            user.uz_language = uz_language
            rus_language(message)           
        if call.data == 'Хорошо':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]
            bot.reply_to(message, lang_dict['good'][user.lang], reply_markup=markup)
            uz_language = call.data
            if(uz_language=='/start'):
                process_start(message)
                return  
            user.uz_language = uz_language
            rus_language(message)            
        if call.data == 'Удовлетворительно':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]
            bot.reply_to(message, lang_dict['satisfactorily'][user.lang], reply_markup=markup)
            uz_language = call.data
            if(uz_language=='/start'):
                process_start(message)
                return  
            user.uz_language = uz_language
            rus_language(message)            
        if call.data == 'Отлично знаю':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]
            bot.reply_to(message, lang_dict['great'][user.lang], reply_markup=markup)
            ru_language = call.data
            if(ru_language=='/start'):
                process_start(message)
                return  
            user.ru_language = ru_language
            about_work(message)
        if call.data == 'Хорошо знаю':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]
            bot.reply_to(message, lang_dict['good'][user.lang], reply_markup=markup)
            ru_language = call.data
            if(ru_language=='/start'):
                process_start(message)
                return  
            user.ru_language = ru_language
            about_work(message)
        if call.data == 'Удовлетворительно знаю':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]
            bot.reply_to(message, lang_dict['satisfactorily'][user.lang], reply_markup=markup)
            ru_language = call.data
            if(ru_language=='/start'):
                process_start(message)
                return  
            user.ru_language = ru_language
            about_work(message)

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
        bot.send_message(message.chat.id, lang_dict['again'][user.lang], reply_markup=markup)
        
    except Exception as e:
        bot.reply_to(message, "ERROR")




  



bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()        

bot.polling()



