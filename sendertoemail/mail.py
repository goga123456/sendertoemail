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

lang_dict = {'ask_name': {'Русский 🇷🇺': 'Как вас зовут: Имя', 'Oʻzbek tili 🇺🇿': 'Ismingiz nima: Ism' },
             'ask_surname': {'Русский 🇷🇺': 'Как вас зовут: Фамилия', 'Oʻzbek tili 🇺🇿': 'Ismingiz nima: Familiya' },
             'wrong_name': {'Русский 🇷🇺': 'Данные введены некорректно. Просим указать имя', 'Oʻzbek tili 🇺🇿': 'Maʻlumotlar notoʻgʻri kiritilgan. Iltimos, ismni koʻrsating' },
             'wrong_surname': {'Русский 🇷🇺': 'Данные введены некорректно. Просим указать фамилию', 'Oʻzbek tili 🇺🇿': 'Maʻlumotlar notoʻgʻri kiritilgan. Iltimos, familiyani koʻrsating' },
             'ask_birthday': {'Русский 🇷🇺': 'Дата Вашего рождения:', 'Oʻzbek tili 🇺🇿': 'Tugʻilgan yil, oy va sanangizni kiriting:' },
             'wrong_birthday': {'Русский 🇷🇺': 'Вы ввели неправильную дату!', 'Oʻzbek tili 🇺🇿': 'Siz notoʻgʻri sanani kiritdingiz!' },
             'number': {'Русский 🇷🇺': 'Укажите контактный номер, чтобы мы могли связаться с Вами:', 'Oʻzbek tili 🇺🇿': 'Siz bilan bogʻlana olishimiz uchun kontakt raqam kiriting:' },
             'wrong_number': {'Русский 🇷🇺': 'Неверный формат номера!', 'Oʻzbek tili 🇺🇿': 'Notoʻgʻri raqam formati!' },
             'adress': {'Русский 🇷🇺': 'Укажите адрес проживания', 'Oʻzbek tili 🇺🇿': 'Yashash manzilingizni kiriting:' },
             'town': {'Русский 🇷🇺': 'Откуда Вы?', 'Oʻzbek tili 🇺🇿': 'Qayerdan siz?' },
             'wrong_town_and_district': {'Русский 🇷🇺': 'Название города должно состоять из букв и может быть несколькими словами', 'Oʻzbek tili 🇺🇿': 'Shahar nomi harflardan iborat boʻlishi kerak va bir necha so‘z boʻlishi mumkin' },
             'district': {'Русский 🇷🇺': 'Выберите район:', 'Oʻzbek tili 🇺🇿': 'Tumanni tanlang:' },
             'town_and_district': {'Русский 🇷🇺': 'Напишите город и район:', 'Oʻzbek tili 🇺🇿': 'Shahar va tuman yozing:' },
             'wrong_town_and_district': {'Русский 🇷🇺': 'Название района и города должно состоять из букв и может быть несколькими словами', 'Oʻzbek tili 🇺🇿': 'Tuman va shahar nomi harflardan iborat boʻlishi kerak va bir necha so‘z boʻlishi mumkin' },
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
             'info':  {'Русский 🇷🇺': 'На следущие вопросы ответьте выбором одного из вариантов', 'Oʻzbek tili 🇺🇿': 'Quyidagi savollarga variantlardan birini tanlash bilan javob bering' },
             'secondary':  {'Русский 🇷🇺': 'Среднее', 'Oʻzbek tili 🇺🇿': 'Oʻrta' },
             'incomplete_secondary':  {'Русский 🇷🇺': 'Неполное среднее', 'Oʻzbek tili 🇺🇿': 'Tugallanmagan oʻrta' },
             'secondary_special':  {'Русский 🇷🇺': 'Среднее специальное', 'Oʻzbek tili 🇺🇿': 'Oʻrta maxsus' },
             'great':  {'Русский 🇷🇺': 'Отлично', 'Oʻzbek tili 🇺🇿': 'A‘lo' },
             'good':  {'Русский 🇷🇺': 'Хорошо', 'Oʻzbek tili 🇺🇿': 'Yaxshi' },
             'satisfactorily':  {'Русский 🇷🇺': 'Удовлетворительно', 'Oʻzbek tili 🇺🇿': 'Qoniqarli' },
             'ne_vladeyu':  {'Русский 🇷🇺': 'Не владею', 'Oʻzbek tili 🇺🇿': 'Egalik qilmaydi' },
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
             'wrong_work_experience':  {'Русский 🇷🇺': 'Неверные данные', 'Oʻzbek tili 🇺🇿': 'Notoʻgʻri maʻlumotlar' },
             'tashkent':  {'Русский 🇷🇺': 'Ташкент', 'Oʻzbek tili 🇺🇿': 'Toshkent' },
             'drugoi':  {'Русский 🇷🇺': 'Другой город', 'Oʻzbek tili 🇺🇿': 'Boshqa shahar' },
             'Olmazor':  {'Русский 🇷🇺': 'Алмазарский', 'Oʻzbek tili 🇺🇿': 'Олмазор' },
             'Bektemir':  {'Русский 🇷🇺': 'Бектемирский', 'Oʻzbek tili 🇺🇿': 'Bektemir' },
             'Mirabad':  {'Русский 🇷🇺': 'Мирабадский', 'Oʻzbek tili 🇺🇿': 'Mirobod' },
             'Mirzo_Ulugbek':  {'Русский 🇷🇺': 'Мирзо-Улугбекский', 'Oʻzbek tili 🇺🇿': 'Mirzo Ulugʻbek' },
             'Sergeli':  {'Русский 🇷🇺': 'Сергели', 'Oʻzbek tili 🇺🇿': 'Sirgali' },
             'Chilonzor':  {'Русский 🇷🇺': 'Чиланзарский', 'Oʻzbek tili 🇺🇿': 'Chilonzor' },
             'Shayhontohur':  {'Русский 🇷🇺': 'Шайхантаурский', 'Oʻzbek tili 🇺🇿': 'Shaihontohur' },
             'Yunusobod':  {'Русский 🇷🇺': 'Юнусабадский', 'Oʻzbek tili 🇺🇿': 'Yunusobod' },
             'Yakkosoroy':  {'Русский 🇷🇺': 'Яккасарайский', 'Oʻzbek tili 🇺🇿': 'Yakkosoroy' },
             'Yashnobod':  {'Русский 🇷🇺': 'Яшнабадский', 'Oʻzbek tili 🇺🇿': 'Yashnobod' },
             'Uchtepa':  {'Русский 🇷🇺': 'Учтепа', 'Oʻzbek tili 🇺🇿': 'Uchtepa' },
             'prodoljit':  {'Русский 🇷🇺': 'Продолжить', 'Oʻzbek tili 🇺🇿': 'Davom eting' },
             'otkazatsya':  {'Русский 🇷🇺': 'Отказаться', 'Oʻzbek tili 🇺🇿': 'Rad etish' },
             'resume_text':  {'Русский 🇷🇺': 'Текст ознакомления с вакансией', 'Oʻzbek tili 🇺🇿': 'Ish bilan tanishish matni' },
             'resume_question':  {'Русский 🇷🇺': 'Я помогу тебе сформировать резюме?', 'Oʻzbek tili 🇺🇿': 'Sizga rezyume yaratishda yordam beramanmi?' },
             'day':  {'Русский 🇷🇺': 'День', 'Oʻzbek tili 🇺🇿': 'kun' },
             'month':  {'Русский 🇷🇺': 'Месяц', 'Oʻzbek tili 🇺🇿': 'oy' },
             'year':  {'Русский 🇷🇺': 'Год', 'Oʻzbek tili 🇺🇿': 'yil' },
             'choose_day':  {'Русский 🇷🇺': 'Выберите день', 'Oʻzbek tili 🇺🇿': 'Kunni tanlang' },
             'choose_month':  {'Русский 🇷🇺': 'Выберите месяц', 'Oʻzbek tili 🇺🇿': 'Oyni tanlang' },
             'choose_year':  {'Русский 🇷🇺': 'Выберите год', 'Oʻzbek tili 🇺🇿': 'Yilni tanlang' },
             'january':  {'Русский 🇷🇺': 'Январь', 'Oʻzbek tili 🇺🇿': 'Yanvar' },
             'february':  {'Русский 🇷🇺': 'Февраль', 'Oʻzbek tili 🇺🇿': 'Fevral' },
             'march':  {'Русский 🇷🇺': 'Март', 'Oʻzbek tili 🇺🇿': 'Mart' },
             'april':  {'Русский 🇷🇺': 'Апрель', 'Oʻzbek tili 🇺🇿': 'Aprel' },
             'may':  {'Русский 🇷🇺': 'Май', 'Oʻzbek tili 🇺🇿': 'May' },
             'june':  {'Русский 🇷🇺': 'Июнь', 'Oʻzbek tili 🇺🇿': 'Iyun' },
             'july':  {'Русский 🇷🇺': 'Июль', 'Oʻzbek tili 🇺🇿': 'Iyul' },
             'august':  {'Русский 🇷🇺': 'Август', 'Oʻzbek tili 🇺🇿': 'Avgust' },
             'september':  {'Русский 🇷🇺': 'Сентябрь', 'Oʻzbek tili 🇺🇿': 'Sentyabr' },
             'october':  {'Русский 🇷🇺': 'Октябрь', 'Oʻzbek tili 🇺🇿': 'Oktyabr' },
             'november':  {'Русский 🇷🇺': 'Ноябрь', 'Oʻzbek tili 🇺🇿': 'Noyabr' },
             'december':  {'Русский 🇷🇺': 'Декабрь', 'Oʻzbek tili 🇺🇿': 'Dekabr' },
             'send':  {'Русский 🇷🇺': 'Отправить', 'Oʻzbek tili 🇺🇿': 'Yuborish' },
             'rejection':  {'Русский 🇷🇺': 'Вы отказались от составления резюме', 'Oʻzbek tili 🇺🇿': 'Siz rezyume yozishdan voz kechdingiz' }     
}



class User:
    def __init__(self, lang):
        self.lang = lang
        self.name = None
        self.surname = None
        self.day = None
        self.month = None
        self.year = None
        self.number = None
        self.town = None
        self.district = None
        self.town_and_district = None
        self.education = None
        self.uz_language = None
        self.ru_language = None
        self.en_language = None
        self.work = None
        self.work_experience = None
        
        
        



markupp = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
btn1 = types.KeyboardButton('Русский 🇷🇺')
btn2 = types.KeyboardButton('Oʻzbek tili 🇺🇿')
markupp.row(btn1, btn2)

#markups for calendar


markup_calendar_day = types.InlineKeyboardMarkup(row_width=7)
item1 = types.InlineKeyboardButton('1', callback_data='1')
item2 = types.InlineKeyboardButton('2', callback_data='2')
item3 = types.InlineKeyboardButton('3', callback_data='3')
item4 = types.InlineKeyboardButton('4', callback_data='4')
item5 = types.InlineKeyboardButton('5', callback_data='5')
item6 = types.InlineKeyboardButton('6', callback_data='6')
item7 = types.InlineKeyboardButton('7', callback_data='7')
item8 = types.InlineKeyboardButton('8', callback_data='8')
item9 = types.InlineKeyboardButton('9', callback_data='9')
item10 = types.InlineKeyboardButton('10', callback_data='10')
item11 = types.InlineKeyboardButton('11', callback_data='11')
item12 = types.InlineKeyboardButton('12', callback_data='12')
item13 = types.InlineKeyboardButton('13', callback_data='13')
item14 = types.InlineKeyboardButton('14', callback_data='14')
item15 = types.InlineKeyboardButton('15', callback_data='15')
item16 = types.InlineKeyboardButton('16', callback_data='16')
item17 = types.InlineKeyboardButton('17', callback_data='17')
item18 = types.InlineKeyboardButton('18', callback_data='18')
item19 = types.InlineKeyboardButton('19', callback_data='19')
item20 = types.InlineKeyboardButton('20', callback_data='20')
item21 = types.InlineKeyboardButton('21', callback_data='21')
item22 = types.InlineKeyboardButton('22', callback_data='22')
item23 = types.InlineKeyboardButton('23', callback_data='23')
item24 = types.InlineKeyboardButton('24', callback_data='24')
item25 = types.InlineKeyboardButton('25', callback_data='25')
item26 = types.InlineKeyboardButton('26', callback_data='26')
item27 = types.InlineKeyboardButton('27', callback_data='27')
item28 = types.InlineKeyboardButton('28', callback_data='28')
item29 = types.InlineKeyboardButton('29', callback_data='29')
item30 = types.InlineKeyboardButton('30', callback_data='30')
item31 = types.InlineKeyboardButton('31', callback_data='31')
markup_calendar_day.add(item1,item2,item3,item4,item5,item6,item7,item8,item9,item10,item11,item12,item13,item14,item15,item16,item17,item18,item19,item20,item21,item22,item23,item24,item25,item26,item27,item28,item29,item30,item31)






markup_calendar_year = types.InlineKeyboardMarkup(row_width=5)
item1 = types.InlineKeyboardButton('1970', callback_data='1970')
item2 = types.InlineKeyboardButton('1971', callback_data='1972')
item3 = types.InlineKeyboardButton('1973', callback_data='1973')
item4 = types.InlineKeyboardButton('1974', callback_data='1974')
item5 = types.InlineKeyboardButton('1975', callback_data='1975')
item6 = types.InlineKeyboardButton('1976', callback_data='1976')
item7 = types.InlineKeyboardButton('1977', callback_data='1977')
item8 = types.InlineKeyboardButton('1978', callback_data='1978')
item9 = types.InlineKeyboardButton('1979', callback_data='1979')
item10 = types.InlineKeyboardButton('1980', callback_data='1980')
item11 = types.InlineKeyboardButton('1981', callback_data='1981')
item12 = types.InlineKeyboardButton('1982', callback_data='1982')
item13 = types.InlineKeyboardButton('1983', callback_data='1983')
item14 = types.InlineKeyboardButton('1984', callback_data='1984')
item15 = types.InlineKeyboardButton('1985', callback_data='1985')
item16 = types.InlineKeyboardButton('1986', callback_data='1986')
item17 = types.InlineKeyboardButton('1987', callback_data='1987')
item18 = types.InlineKeyboardButton('1988', callback_data='1988')
item19 = types.InlineKeyboardButton('1989', callback_data='1989')
item20 = types.InlineKeyboardButton('1990', callback_data='1990')
item21 = types.InlineKeyboardButton('1991', callback_data='1991')
item22 = types.InlineKeyboardButton('1992', callback_data='1992')
item23 = types.InlineKeyboardButton('1993', callback_data='1993')
item24 = types.InlineKeyboardButton('1994', callback_data='1994')
item25 = types.InlineKeyboardButton('1995', callback_data='1995')
item26 = types.InlineKeyboardButton('1996', callback_data='1996')
item27 = types.InlineKeyboardButton('1997', callback_data='1997')
item28 = types.InlineKeyboardButton('1998', callback_data='1998')
item29 = types.InlineKeyboardButton('1999', callback_data='1999')
item30 = types.InlineKeyboardButton('2000', callback_data='2000')
item31 = types.InlineKeyboardButton('2001', callback_data='2001')
item32 = types.InlineKeyboardButton('2002', callback_data='2002')
item33 = types.InlineKeyboardButton('2003', callback_data='2003')
item34 = types.InlineKeyboardButton('2004', callback_data='2004')
item35 = types.InlineKeyboardButton('2005', callback_data='2005')
item36 = types.InlineKeyboardButton('2006', callback_data='2006')
item37 = types.InlineKeyboardButton('2007', callback_data='2007')
item38 = types.InlineKeyboardButton('2008', callback_data='2008')
item39 = types.InlineKeyboardButton('2009', callback_data='2009')
item40 = types.InlineKeyboardButton('2010', callback_data='2010')
markup_calendar_year.add(item1,item2,item3,item4,item5,item6,item7,item8,item9,item10,item11,item12,item13,item14,item15,item16,item17,item18,item19,item20,item21,item22,item23,item24,item25,item26,item27,item28,item29,item30,item31,item32,item33,item34,item35,item36,item37,item38,item39,item40)


#markups for calendar



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

        msg = bot.send_message(message.chat.id, lang_dict['number'][user.lang], reply_markup=markup) 
        bot.register_next_step_handler(msg, ask_number)
    except KeyError:
        msg = bot.reply_to(message, "Выберите один из вариантов 'Русский' или 'Ozbek tili'\n\n 'Русский' yoki 'Ozbek tili' parametrlaridan birini tanlang ")
        bot.register_next_step_handler(msg, ask_language)

    


@bot.message_handler(content_types = ['text'])
def ask_number(message):
    try:
        chat_id = message.chat.id
        number = message.text
        user = user_dict[chat_id]

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn = types.KeyboardButton(lang_dict['start'][user.lang])
        markup.row(btn) 


        markup__v1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_1 = types.KeyboardButton(lang_dict['start'][user.lang])
        btn_2 = types.KeyboardButton(lang_dict['back'][user.lang])
        markup__v1.row(btn_1, btn_2) 

        if(number == lang_dict['start'][user.lang] or number == '/start'):
            process_start(message)
            return   

        
        if not all(x.isascii() or x.isspace() or x.isalnum() for x in number):
            msg = bot.reply_to(message, lang_dict['wrong_number'][user.lang])
            bot.register_next_step_handler(msg, ask_number) 
            return                      

        user.number = number
        bot.send_message(message.chat.id, lang_dict['resume_text'][user.lang])
        ask_about_resume(message)

    except Exception:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        msg = bot.reply_to(message, lang_dict['wrong_number'][user.lang])
        bot.register_next_step_handler(msg, ask_number)

@bot.message_handler(content_types = ['text'])
def ask_about_resume(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        
        markup_resume = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton(lang_dict['prodoljit'][user.lang], callback_data='Продолжить')
        item2 = types.InlineKeyboardButton(lang_dict['otkazatsya'][user.lang], callback_data='Отказаться')
       
        markup_resume.add(item1, item2)   
        bot.send_message(message.chat.id, lang_dict['resume_question'][user.lang] , reply_markup=markup_resume)

    except Exception:
        msg = bot.reply_to(message, "Неверные данные")
        bot.register_next_step_handler(msg, ask_name) 


def between_resume_and_name(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]

    markup__v1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn_1 = types.KeyboardButton(lang_dict['start'][user.lang])
    btn_2 = types.KeyboardButton(lang_dict['back'][user.lang])
    markup__v1.row(btn_1, btn_2)
    msg = bot.send_message(message.chat.id, lang_dict['ask_name'][user.lang], reply_markup = markup__v1)
    bot.register_next_step_handler(msg, ask_name)
           
       
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

        if(name == lang_dict['back'][user.lang]):
            chat_id = message.chat.id
            user = user_dict[chat_id]
            ask_about_resume(message)
            return            
              
        if not all(x.isascii() or x.isspace() or x.isalnum() for x in name):
            msg = bot.reply_to(message, lang_dict['wrong_name'][user.lang])
            bot.register_next_step_handler(msg, ask_name) 
            return                     
        user.name = name

        
        msg = bot.send_message(message.chat.id, lang_dict['ask_surname'][user.lang])
        bot.register_next_step_handler(msg, ask_surname)
        
    except Exception as e:    
        msg = bot.reply_to(message, "Неверные данные")
        bot.register_next_step_handler(msg, ask_name)


def between_name_and_surname(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]

    markup__v1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn_1 = types.KeyboardButton(lang_dict['start'][user.lang])
    btn_2 = types.KeyboardButton(lang_dict['back'][user.lang])
    markup__v1.row(btn_1, btn_2)
    msg = bot.send_message(message.chat.id, lang_dict['ask_surname'][user.lang], reply_markup = markup__v1)
    bot.register_next_step_handler(msg, ask_surname)



@bot.message_handler(content_types = ['text'])
def ask_surname(message):
    try:
        chat_id = message.chat.id
        surname = message.text
        user = user_dict[chat_id]

        markup__v1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_1 = types.KeyboardButton(lang_dict['start'][user.lang])
        btn_2 = types.KeyboardButton(lang_dict['back'][user.lang])
        markup__v1.row(btn_1, btn_2)
        
        if(surname ==lang_dict['start'][user.lang] or surname == '/start'):
            process_start(message)
            return  

        if(surname == lang_dict['back'][user.lang]):
            chat_id = message.chat.id
            user = user_dict[chat_id]     
            between_resume_and_name(message)
            return            
              
        if not all(x.isascii() or x.isspace() or x.isalnum() for x in surname):
            msg = bot.reply_to(message, lang_dict['wrong_surname'][user.lang])
            bot.register_next_step_handler(msg, ask_surname) 
            return                     
        user.surname = surname    

        between_name_and_birthday(message)
        
    except Exception as e:    
        msg = bot.reply_to(message, "Неверные данные")
        bot.register_next_step_handler(msg, ask_surname)        

def between_name_and_birthday(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn = types.KeyboardButton(lang_dict['start'][user.lang])
    markup.row(btn)


    markup__v1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn_1 = types.KeyboardButton(lang_dict['start'][user.lang])
    btn_2 = types.KeyboardButton(lang_dict['back'][user.lang])
    markup__v1.row(btn_1, btn_2)

    markup_calendar_start = types.InlineKeyboardMarkup(row_width=3)
    item1 = types.InlineKeyboardButton(lang_dict['day'][user.lang], callback_data='День')
    item2 = types.InlineKeyboardButton(lang_dict['month'][user.lang], callback_data='Месяц')
    item3 = types.InlineKeyboardButton(lang_dict['year'][user.lang], callback_data='Год')
    item4 = types.InlineKeyboardButton(lang_dict['send'][user.lang], callback_data='Отправить')      
    item5 = types.InlineKeyboardButton(lang_dict['back'][user.lang], callback_data='bck_to_surname')
    markup_calendar_start.add(item1, item2, item3,item4,item5)      
    bot.send_message(message.chat.id, lang_dict['ask_birthday'][user.lang], reply_markup = markup_calendar_start)



        
def ask_town(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        markup_town = types.InlineKeyboardMarkup(row_width=3)
        item1 = types.InlineKeyboardButton(lang_dict['tashkent'][user.lang], callback_data='Ташкент')
        item2 = types.InlineKeyboardButton(lang_dict['drugoi'][user.lang], callback_data='Другой город')
        item3 = types.InlineKeyboardButton(lang_dict['back'][user.lang], callback_data='back_to_birthday')
        markup_town.add(item1, item2, item3)   
        bot.send_message(message.chat.id, lang_dict['town'][user.lang] , reply_markup=markup_town)
    except Exception:
        msg = bot.reply_to(message, 'Неверные данные!')
        bot.register_next_step_handler(msg, ask_town)

def choose_district(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id] 
        markup_regions = types.InlineKeyboardMarkup(row_width=4)
        item1 = types.InlineKeyboardButton(lang_dict['Olmazor'][user.lang], callback_data='Олмазарский')
        item2 = types.InlineKeyboardButton(lang_dict['Bektemir'][user.lang], callback_data='Бектемирский')
        item3 = types.InlineKeyboardButton(lang_dict['Mirabad'][user.lang], callback_data='Мирабадский')
        item4 = types.InlineKeyboardButton(lang_dict['Mirzo_Ulugbek'][user.lang], callback_data='Мирзо-Улугбекский')
        item5 = types.InlineKeyboardButton(lang_dict['Sergeli'][user.lang], callback_data='Сергелинский')
        item6 = types.InlineKeyboardButton(lang_dict['Chilonzor'][user.lang], callback_data='Чиланзарский')
        item7 = types.InlineKeyboardButton(lang_dict['Shayhontohur'][user.lang], callback_data='Шайхантаурский')
        item8 = types.InlineKeyboardButton(lang_dict['Yunusobod'][user.lang], callback_data='Юнусабадский')
        item9 = types.InlineKeyboardButton(lang_dict['Yakkosoroy'][user.lang], callback_data='Яккасарайский')
        item10 = types.InlineKeyboardButton(lang_dict['Yashnobod'][user.lang], callback_data='Яшнабадский')
        item11 = types.InlineKeyboardButton(lang_dict['Uchtepa'][user.lang], callback_data='Учтепинский')
        item12 = types.InlineKeyboardButton(lang_dict['back'][user.lang], callback_data='back_to_town')
        markup_regions.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, item11,item12)           
        bot.send_message(message.chat.id, lang_dict['district'][user.lang] , reply_markup=markup_regions)
    except Exception:
        msg = bot.reply_to(message, 'Неверные данные!')
        bot.register_next_step_handler(msg, ask_town)    


def ask_town_and_district(message):
    try:
        chat_id = message.chat.id
        town_and_district = message.text
        user = user_dict[chat_id]
        
        markup__v1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_1 = types.KeyboardButton(lang_dict['start'][user.lang])
        btn_2 = types.KeyboardButton(lang_dict['back'][user.lang])
        markup__v1.row(btn_1, btn_2)

        msg = bot.send_message(message.chat.id, lang_dict['town_and_district'][user.lang], reply_markup=markup__v1)

        if(town_and_district == lang_dict['back'][user.lang]):
            chat_id = message.chat.id
            user = user_dict[chat_id]
            bot.delete_message(message.chat.id, message.message_id-1)
            bot.delete_message(message.chat.id, message.message_id-2)
            ask_town(message)
            return
        if(town_and_district == lang_dict['start'][user.lang] or town_and_district == '/start'):
            process_start(message)
            return         
        if not all(x.isascii() or x.isspace() or x.isalnum() for x in town_and_district):
            msg = bot.reply_to(message, lang_dict['wrong_town_and_district'][user.lang])
            bot.register_next_step_handler(msg, ask_town_and_district) 
            return    


        user.town_and_district = town_and_district
        
        bot.register_next_step_handler(msg, education_1)   
        

    except Exception:    
        msg = bot.reply_to(message, "Неверные данные")
        bot.register_next_step_handler(msg, ask_town_and_district) 




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
    item6 = types.InlineKeyboardButton(lang_dict['back'][user.lang], callback_data='back_to_town')
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
    item4 = types.InlineKeyboardButton(lang_dict['ne_vladeyu'][user.lang], callback_data='Не владею узбекским языком')
    item5 = types.InlineKeyboardButton(lang_dict['back'][user.lang], callback_data='bck_edu')
    markup2.add(item1, item2, item3, item4, item5)
    bot.send_message(message.chat.id, lang_dict['uzb_language'][user.lang], reply_markup=markup2)       
    
       
@bot.message_handler(content_types = ['text'])
def rus_language(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    markup3 = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton(lang_dict['great'][user.lang], callback_data='Отлично знаю')
    item2 = types.InlineKeyboardButton(lang_dict['good'][user.lang], callback_data='Хорошо знаю')
    item3 = types.InlineKeyboardButton(lang_dict['satisfactorily'][user.lang], callback_data='Удовлетворительно знаю')
    item4 = types.InlineKeyboardButton(lang_dict['ne_vladeyu'][user.lang], callback_data='Не владею русским языком')
    item5 = types.InlineKeyboardButton(lang_dict['back'][user.lang], callback_data='bck_uz')
    markup3.add(item1, item2, item3, item4, item5)
    bot.send_message(message.chat.id, lang_dict['rus_language'][user.lang] , reply_markup=markup3) 

@bot.message_handler(content_types = ['text'])
def english_language(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    markup4 = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton(lang_dict['great'][user.lang], callback_data='Отлично владею')
    item2 = types.InlineKeyboardButton(lang_dict['good'][user.lang], callback_data='Хорошо владею')
    item3 = types.InlineKeyboardButton(lang_dict['satisfactorily'][user.lang], callback_data='Удовлетворительно владею')
    item4 = types.InlineKeyboardButton(lang_dict['ne_vladeyu'][user.lang], callback_data='Не владею английским языком')
    item5 = types.InlineKeyboardButton(lang_dict['back'][user.lang], callback_data='bck_ru')
    markup4.add(item1, item2, item3, item4, item5)
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
    markup__v1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn_1 = types.KeyboardButton(lang_dict['start'][user.lang])
    btn_2 = types.KeyboardButton(lang_dict['back'][user.lang])
    markup__v1.row(btn_1, btn_2)
    msg = bot.send_message(message.chat.id, lang_dict['work_experience'][user.lang], reply_markup = markup__v1)
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
            about_work(message)
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
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
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
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
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
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
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
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
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
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
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
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
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
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
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
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            rus_language(message) 

        if call.data == 'Не владею узбекским языком':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn = types.KeyboardButton(lang_dict['start'][user.lang])
            markup.row(btn)


            bot.reply_to(message, lang_dict['ne_vladeyu'][user.lang], reply_markup=markup)
            uz_language = call.data
            
            user.uz_language = uz_language
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
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
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
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
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
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
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            english_language(message)

        if call.data == 'Не владею русским языком':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn = types.KeyboardButton(lang_dict['start'][user.lang])
            markup.row(btn)

            bot.reply_to(message, lang_dict['ne_vladeyu'][user.lang], reply_markup=markup)
            ru_language = call.data
            
            user.ru_language = ru_language
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
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
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
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
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
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
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            about_work(message)
        
        if call.data == 'Не владею английским языком':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn = types.KeyboardButton(lang_dict['start'][user.lang])
            markup.row(btn)

            bot.reply_to(message, lang_dict['ne_vladeyu'][user.lang], reply_markup=markup)
            en_language = call.data
            
            user.en_language = en_language
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
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
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
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
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            say_thanks(message)
        
        if call.data == 'bck_edu': 
            chat_id = call.message.chat.id
            user = user_dict[chat_id]

            bot.send_message(call.message.chat.id, lang_dict['back'][user.lang])
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)         
            education_1(message)
                                             
        if call.data == 'bck_uz':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]


            bot.send_message(call.message.chat.id, lang_dict['back'][user.lang])
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            uzb_language(message)
            
        if call.data == 'bck_ru':
            chat_id = call.message.chat.id
            user = user_dict[chat_id] 

            bot.send_message(call.message.chat.id, lang_dict['back'][user.lang])
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)             
            rus_language(message)

        if call.data == 'bck_eng':
            chat_id = call.message.chat.id
            user = user_dict[chat_id] 

            bot.send_message(call.message.chat.id, lang_dict['back'][user.lang])
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            english_language(message) 

        if call.data == 'back_to_town':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]
            
            bot.send_message(call.message.chat.id, lang_dict['back'][user.lang])
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            ask_town(message) 

        

        if call.data == 'back_to_birthday':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]
            
            bot.send_message(call.message.chat.id, lang_dict['back'][user.lang])
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            between_name_and_birthday(message)    
            
    

        if call.data == 'Ташкент':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn = types.KeyboardButton(lang_dict['start'][user.lang])
            markup.row(btn)

            bot.reply_to(message, lang_dict['tashkent'][user.lang], reply_markup=markup)
            town = call.data            
            user.town = town
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            choose_district(message)                   
         
        if call.data == 'Другой город':
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)       
            ask_town_and_district(message)  

        
        if call.data == 'Олмазарский':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn = types.KeyboardButton(lang_dict['start'][user.lang])
            markup.row(btn)

            bot.reply_to(message, lang_dict['Olmazor'][user.lang], reply_markup=markup)
            district = call.data
            
            user.district = district
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            education_1(message)    

        if call.data == 'Бектемирский':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn = types.KeyboardButton(lang_dict['start'][user.lang])
            markup.row(btn)

            bot.reply_to(message, lang_dict['Bektemir'][user.lang], reply_markup=markup)
            district = call.data
            
            user.district = district
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            education_1(message)   

        if call.data == 'Мирабадский':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn = types.KeyboardButton(lang_dict['start'][user.lang])
            markup.row(btn)

            bot.reply_to(message, lang_dict['Mirabad'][user.lang], reply_markup=markup)
            district = call.data
            
            user.district = district
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            education_1(message)    

        if call.data == 'Мирзо-Улугбекский':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn = types.KeyboardButton(lang_dict['start'][user.lang])
            markup.row(btn)

            bot.reply_to(message, lang_dict['Mirzo_Ulugbek'][user.lang], reply_markup=markup)
            district = call.data
            
            user.district = district
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            education_1(message)  

        if call.data == 'Сергелинский':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn = types.KeyboardButton(lang_dict['start'][user.lang])
            markup.row(btn)

            bot.reply_to(message, lang_dict['Sergeli'][user.lang], reply_markup=markup)
            district = call.data
            
            user.district = district
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            education_1(message) 

        if call.data == 'Чиланзарский':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn = types.KeyboardButton(lang_dict['start'][user.lang])
            markup.row(btn)

            bot.reply_to(message, lang_dict['Chilonzor'][user.lang], reply_markup=markup)
            district = call.data
            
            user.district = district
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            education_1(message)  

        if call.data == 'Шайхантаурский':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn = types.KeyboardButton(lang_dict['start'][user.lang])
            markup.row(btn)

            bot.reply_to(message, lang_dict['Shayhontohur'][user.lang], reply_markup=markup)
            district = call.data
            
            user.district = district
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            education_1(message) 

        if call.data == 'Юнусабадский':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn = types.KeyboardButton(lang_dict['start'][user.lang])
            markup.row(btn)

            bot.reply_to(message, lang_dict['Yunusobod'][user.lang], reply_markup=markup)
            district = call.data
            
            user.district = district
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            education_1(message)                                           
        if call.data == 'Яккасарайский':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn = types.KeyboardButton(lang_dict['start'][user.lang])
            markup.row(btn)

            bot.reply_to(message, lang_dict['Yakkosoroy'][user.lang], reply_markup=markup)
            district = call.data
            
            user.district = district
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            education_1(message)    
        if call.data == 'Яшнабадский':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn = types.KeyboardButton(lang_dict['start'][user.lang])
            markup.row(btn)

            bot.reply_to(message, lang_dict['Yashnobod'][user.lang], reply_markup=markup)
            district = call.data
            
            user.district = district
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            education_1(message)  

        if call.data == 'Учтепинский':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn = types.KeyboardButton(lang_dict['start'][user.lang])
            markup.row(btn)

            bot.reply_to(message, lang_dict['Uchtepa'][user.lang], reply_markup=markup)
            district = call.data
            
            user.district = district
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            education_1(message) 


        if call.data == 'Продолжить':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]
            bot.send_message(message.chat.id, lang_dict['prodoljit'][user.lang])
            between_resume_and_name(message)
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)                   
         
        if call.data == 'Отказаться': 
            chat_id = call.message.chat.id
            user = user_dict[chat_id] 
            bot.send_message(message.chat.id, lang_dict['otkazatsya'][user.lang])     
            send_nothing(message)
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

        if call.data == 'День':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]
            msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=lang_dict['choose_day'][user.lang], parse_mode='Markdown')
            msg = bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=markup_calendar_day)



        if call.data == 'Месяц':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]
            markup_calendar_month = types.InlineKeyboardMarkup(row_width=4)
            item1 = types.InlineKeyboardButton(lang_dict['january'][user.lang], callback_data='01')
            item2 = types.InlineKeyboardButton(lang_dict['february'][user.lang], callback_data='02')
            item3 = types.InlineKeyboardButton(lang_dict['march'][user.lang], callback_data='03')
            item4 = types.InlineKeyboardButton(lang_dict['april'][user.lang], callback_data='04')
            item5 = types.InlineKeyboardButton(lang_dict['march'][user.lang], callback_data='05')
            item6 = types.InlineKeyboardButton(lang_dict['june'][user.lang], callback_data='06')
            item7 = types.InlineKeyboardButton(lang_dict['july'][user.lang], callback_data='07')
            item8 = types.InlineKeyboardButton(lang_dict['august'][user.lang], callback_data='08')
            item9 = types.InlineKeyboardButton(lang_dict['september'][user.lang], callback_data='09')
            item10 = types.InlineKeyboardButton(lang_dict['october'][user.lang], callback_data='10')
            item11 = types.InlineKeyboardButton(lang_dict['november'][user.lang], callback_data='11')
            item12 = types.InlineKeyboardButton(lang_dict['december'][user.lang], callback_data='12')
            markup_calendar_month.add(item1,item2,item3,item4,item5,item6,item7,item8,item9,item10,item11,item12) 
            msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=lang_dict['choose_month'][user.lang], parse_mode='Markdown')
            msg = bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=markup_calendar_month)
        

        if call.data == 'Год':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]
            msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=lang_dict['choose_year'][user.lang], parse_mode='Markdown')
            msg = bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=markup_calendar_year)    
        
        if call.data == 'bck_to_surname':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]


            bot.send_message(call.message.chat.id, lang_dict['back'][user.lang])
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            between_name_and_surname(message)
            

#Календарные 

        if call.data == '1' or call.data == '2' or call.data == '3' or call.data == '4' or call.data == '5' or call.data == '6' or call.data == '7' or call.data == '8' or call.data == '9' or call.data == '10' or call.data == '11' or call.data == '12' or call.data == '13' or call.data == '14' or call.data == '15' or call.data == '16' or call.data == '17' or call.data == '18' or call.data == '19' or call.data == '20' or call.data == '21' or call.data == '22' or call.data == '23' or call.data == '24' or call.data == '25' or call.data == '26' or call.data == '27' or call.data == '28' or call.data == '29' or call.data == '30' or call.data == '31':
        
            chat_id = call.message.chat.id
            user = user_dict[chat_id]

            day = call.data           
            user.day = day

            markup_calendar_start = types.InlineKeyboardMarkup(row_width=3)
            item1 = types.InlineKeyboardButton(lang_dict['day'][user.lang], callback_data='День')
            item2 = types.InlineKeyboardButton(lang_dict['month'][user.lang], callback_data='Месяц')
            item3 = types.InlineKeyboardButton(lang_dict['year'][user.lang], callback_data='Год')
            item4 = types.InlineKeyboardButton(lang_dict['send'][user.lang], callback_data='Отправить')      
            item5 = types.InlineKeyboardButton(lang_dict['back'][user.lang], callback_data='bck_to_name')
            markup_calendar_start.add(item1, item2, item3,item4,item5)       
            msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=lang_dict['ask_birthday'][user.lang], parse_mode='Markdown')
            msg = bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=markup_calendar_start)
        
        if call.data == '01' or call.data == '02' or call.data == '03' or call.data == '04' or call.data == '05' or call.data == '06' or call.data == '07' or call.data == '08' or call.data == '09' or call.data == '10' or call.data == '11' or call.data == '12':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]

            month = call.data           
            user.month = month

            markup_calendar_start = types.InlineKeyboardMarkup(row_width=3)
            item1 = types.InlineKeyboardButton(lang_dict['day'][user.lang], callback_data='День')
            item2 = types.InlineKeyboardButton(lang_dict['month'][user.lang], callback_data='Месяц')
            item3 = types.InlineKeyboardButton(lang_dict['year'][user.lang], callback_data='Год')
            item4 = types.InlineKeyboardButton(lang_dict['send'][user.lang], callback_data='Отправить')      
            item5 = types.InlineKeyboardButton(lang_dict['back'][user.lang], callback_data='bck_to_name')
            markup_calendar_start.add(item1, item2, item3,item4,item5)      
            msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=lang_dict['ask_birthday'][user.lang], parse_mode='Markdown')
            msg = bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=markup_calendar_start)

        if call.data == '1970' or call.data == '1971' or call.data == '1972' or call.data == '1973' or call.data == '1974' or call.data == '1975' or call.data == '1976' or call.data == '1977' or call.data == '1978' or call.data == '1979' or call.data == '1980' or call.data == '1981' or call.data == '1982' or call.data == '1983' or call.data == '1984' or call.data == '1985' or call.data == '1986' or call.data == '1987' or call.data == '1988' or call.data == '1989' or call.data == '1990' or call.data == '1991' or call.data == '1992' or call.data == '1993' or call.data == '1994' or call.data == '1995' or call.data == '1996' or call.data == '1997' or call.data == '1998' or call.data == '1999' or call.data == '2000' or call.data == '2001' or call.data == '2002' or call.data == '2003' or call.data == '2004' or call.data == '2005' or call.data == '2006' or call.data == '2007' or call.data == '2008' or call.data == '2009' or call.data == '2010':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]

            year = call.data           
            user.year = year

            markup_calendar_start = types.InlineKeyboardMarkup(row_width=3)
            item1 = types.InlineKeyboardButton(lang_dict['day'][user.lang], callback_data='День')
            item2 = types.InlineKeyboardButton(lang_dict['month'][user.lang], callback_data='Месяц')
            item3 = types.InlineKeyboardButton(lang_dict['year'][user.lang], callback_data='Год')
            item4 = types.InlineKeyboardButton(lang_dict['send'][user.lang], callback_data='Отправить')      
            item5 = types.InlineKeyboardButton(lang_dict['back'][user.lang], callback_data='bck_to_name')
            markup_calendar_start.add(item1, item2, item3,item4,item5)      
            msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=lang_dict['ask_birthday'][user.lang], parse_mode='Markdown')
            msg = bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=markup_calendar_start)

        if call.data == 'Отправить':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]
            if user.day == None or user.month == None or user.year == None:
                bot.send_message(message.chat.id, 'Вы не выбрали число, месяц или год')
            else:
                bot.send_message(message.chat.id, f'{user.day}/{user.month}/{user.year}')
                bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
                ask_town(message)    

           
          
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
    
        chat_id = message.chat.id
        user = user_dict[chat_id]
   
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        </head>
        <body>
        
        <h1>Заявка:</h1>

        <h2>Номер телефона: {user.number}</h2>    
        <h2>Имя: {user.name}</h2>
        <h2>Имя: {user.surname}</h2>
        <h2>День рождения: {user.day}/{user.month}/{user.year}</h2>
        <h2>Адресные данные:</h2>
        <h2>Город: {user.town}</h2>
        <h2>Район: {user.district}</h2>
        <h2>Город и район, если не в Ташкенте: {user.town_and_district}</h2>
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

        chat_id = message.chat.id
        user = user_dict[chat_id]

       
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        </head>
        <body>
        
        <h1>Заявка:</h1>
            
        <h2>Номер телефона: {user.number}</h2>    
        <h2>Имя: {user.name}</h2>
        <h2>Имя: {user.surname}</h2>
        <h2>День рождения: {user.day}/{user.month}/{user.year}</h2>
        <h2>Адресные данные:</h2>
        <h2>Город: {user.town}</h2>
        <h2>Район: {user.district}</h2>
        <h2>Город и район, если не в Ташкенте: {user.town_and_district}</h2>
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


def send_nothing(message):
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
    
    
    
        chat_id = message.chat.id
        user = user_dict[chat_id]
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        </head>
        <body>
        
        <h1>Заявка:</h1>
        <h2>Человек с номером телефона {user.number} отказался от формирования резюме</h2>
        
        

      
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
        bot.reply_to(message, lang_dict['rejection'][user.lang])
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




