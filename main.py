import telebot
from telebot import REPLY_MARKUP_TYPES, types
import config
import pyowm
from pyowm import OWM
from pyowm.utils.config import get_default_config
import requests
import bs4
from bs4 import BeautifulSoup
import lxml
bot=telebot.TeleBot("6719843100:AAFBC5Dl2KHDFm3sgdxk3pgaTWGjLgSIbzM", parse_mode=None)
@bot.message_handler(commands=['start'])
def start(message):
  hello=open('hello.webp', 'rb')
  bot.send_sticker(message.chat.id, hello)
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
  btn1 = types.KeyboardButton("Что ты умеешь?")
  markup.row(btn1)
  bot.send_message(message.from_user.id,'Привет,{0.first_name}, я бот {1.first_name}, который сделает твою жизнь легче😊'.format(message.from_user,bot.get_me()), reply_markup=markup)
  
  
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
  if message.text=='Что ты умеешь?':
    markup1 = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton('Узнавать для вас прогноз погоды', callback_data="weather")
    markup1.add(btn2)
    btn3 = types.InlineKeyboardButton('Актуальный курс доллара/евро к гривне', callback_data="kurs")
    markup1.add(btn3)
    btn4 = types.InlineKeyboardButton('Узнать год в какого животного ты родился ', callback_data="animal" )
    markup1.add(btn4)
    btn5 = types.InlineKeyboardButton('Узнать ваш ИМТ(Индекс Массы Тела)', callback_data="BMI")
    markup1.add(btn5)
    bot.send_message(message.from_user.id, 'Я умею:', reply_markup=markup1)
#
#
#task 1
#
#
@bot.callback_query_handler(func=lambda call: call.data =="weather")
def get_text_messages(message):
    msg=bot.send_message(message.from_user.id, 'Введите город')
    bot.register_next_step_handler(msg, get_weather)
def get_weather(message):
  try:
    config_dict = get_default_config()
    config_dict['language'] = 'ru'
    owm = OWM("58cac38d64542429da5f01183ce2f183", config_dict)
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(message.text)
    w = observation.weather

    w.detailed_status         # 'clouds'
    w.wind()                  # {'speed': 4.6, 'deg': 330}
    w.humidity                # 87
    w.temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
    w.rain                    # {}
    w.heat_index              # None
    w.clouds                  # 75
    t=round(w.temperature('celsius')['temp'])
    tmax=round(w.temperature('celsius')['temp_max'])
  
    bot.send_message(message.from_user.id, "облачность:"+ w.detailed_status + "\nтемпература сейчас:"+str(t)+ "°C" +"\nмаксимальная температура:" + str(tmax) + "°C" + "\nвлажность:" + str(w.humidity) + "%" + "\nветер:" + str(w.wind()['speed']) + "м/с")
  except:
    bot.send_message(message.from_user.id, "Город не найден")
#
#
#task 2
#
#
@bot.callback_query_handler(func=lambda call: call.data =="kurs")
def get_text_messages(message):

  url = 'https://www.bing.com/search?q=%d0%ba%d1%83%d1%80%d1%81+%d0%b4%d0%be%d0%bb%d0%bb%d0%b0%d1%80%d0%b0+%d0%ba+%d0%b3%d1%80%d0%b8%d0%b2%d0%bd%d0%b5&qs=SS&pq=%d0%ba%d1%83%d1%80%d1%81+%d0%b4%d0%be%d0%bb%d0%bb%d0%b0%d1%80%d0%b0+r+&sk=SS1&sc=10-15&cvid=F42D56C25AA34C43A0E89C8439DB9193&FORM=QBRE&sp=2&ghc=1&lq=0'
  headers ={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
  }
  full_page = requests.get(url, headers=headers)
  soup = BeautifulSoup(full_page.content, 'html.parser')
  convert = soup.find("div", class_ = "b_focusTextSmall curr_totxt").text
  c=convert.replace("Ukrainian Hryvnia", "")
  


  url1 = 'https://www.bing.com/search?pglt=675&q=%D0%BA%D1%83%D1%80%D1%81+%D0%B5%D0%B2%D1%80%D0%BE+%D0%BA+%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B5&cvid=b277330d0c0a4d7eb210262b12057530&gs_lcrp=EgZjaHJvbWUqBggEEAAYQDIGCAAQRRg5MgYIARAAGEAyBggCEAAYQDIGCAMQABhAMgYIBBAAGEAyBggFEAAYQDIGCAYQABhAMgYIBxAAGEAyBggIEAAYQNIBCTE1ODM2ajBqMagCALACAA&FORM=ANNTA1&adppc=EdgeStart&DAF0=1&PC=HCTS'
  headers1 ={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
  }
  full_page1 = requests.get(url1, headers=headers1)
  soup1 = BeautifulSoup(full_page1.content, 'html.parser')
  convert1 = soup1.find("div", class_ = "b_focusTextSmall curr_totxt").text
  c1=convert1.replace("Ukrainian Hryvnia", "")
  text = "Курс доллара: "+c+"грн"+ "\nКурс евро: "+c1+"грн"
  bot.send_message(message.from_user.id, text)
#
#
#task 3
#
#
@bot.callback_query_handler(func=lambda call: call.data =="animal")
def get_text_messages(message):
  msg2=bot.send_message(message.from_user.id, 'Веди свой год рождения')
  bot.register_next_step_handler(msg2, get_animal)
def get_animal(message):
  try:
    list1 = [2020, 2008, 1996, 1984, 1972, 1960, 1948, 1936]
    list2 = [2021, 2009, 1997, 1985, 1973, 1961, 1949, 1937]
    list3 = [2022, 2010, 1998, 1986, 1974, 1962, 1950, 1938]
    list4 = [2023, 2011, 1999, 1987, 1975, 1963, 1951, 1939]
    list5 = [2024, 2012, 2000, 1988, 1976, 1964, 1952, 1940]
    list6 = [2025, 2013, 2001, 1989, 1977, 1965, 1953, 1941]
    list7 = [2026, 2014, 2002, 1990, 1978, 1966, 1954, 1942]
    list8 = [2027, 2015, 2003, 1991, 1979, 1967, 1955, 1943]
    list9 = [2028, 2016, 2004, 1992, 1980, 1968, 1956, 1944]
    list10 = [2029, 2017, 2005, 1993, 1981, 1969, 1957, 1945]
    list11 = [2030, 2018, 2006, 1994, 1982, 1970, 1958, 1946]
    list12 = [2031, 2019, 2007, 1995, 1983, 1971, 1959, 1947]
    msg2 = int(message.text)
    if msg2 in list1:
      bot.send_message(message.from_user.id,"Ты родился(-ась) в год Крысы")
    elif msg2 in list2:
      bot.send_message(message.from_user.id,"Ты родился(-ась) в год Быка")
    elif msg2 in list3:
      bot.send_message(message.from_user.id,"Ты родился(-ась) в год Тигра")
    elif msg2 in list4:
      bot.send_message(message.from_user.id,"Ты родился(-ась) в год Кролика")
    elif msg2 in list5:
      bot.send_message(message.from_user.id,"Ты родился(-ась) в год Дракона")
    elif msg2 in list6:
      bot.send_message(message.from_user.id,"Ты родился(-ась) в год Змеи")
    elif msg2 in list7:
      bot.send_message(message.from_user.id,"Ты родился(-ась) в год Лошади")
    elif msg2 in list8:
      bot.send_message(message.from_user.id,"Ты родился(-ась) в год Козы")
    elif msg2 in list9:
      bot.send_message(message.from_user.id,"Ты родился(-ась) в год Обезьяны")
    elif msg2 in list10:
      bot.send_message(message.from_user.id,"Ты родился(-ась) в год Петуха")
    elif msg2 in list11:
      bot.send_message(message.from_user.id,"Ты родился(-ась) в год Собаки")
    elif msg2 in list12:
      bot.send_message(message.from_user.id,"Ты родился(-ась) в год Свиньи")
  except:
    bot.send_message(message.from_user.id,"я типя не паниме :(")
#
#
#4 tast
#
#
@bot.callback_query_handler(func=lambda call: call.data =="BMI")

def get_text_messages(message):
  markup2 = types.InlineKeyboardMarkup()
  btn1 = types.InlineKeyboardButton('Мужской', callback_data="men")
  btn2 = types.InlineKeyboardButton('Женский', callback_data="women")
  markup2.add(btn1, btn2)
  bot.send_message(message.from_user.id, 'Выберите пол', reply_markup=markup2)
@bot.callback_query_handler(func=lambda call: call.data =="men")
def get_text_messages(message):
  markup3 = types.InlineKeyboardMarkup()
  btn3 = types.InlineKeyboardButton('Мальчик 1-18лет(год)', callback_data="boy")
  btn4 = types.InlineKeyboardButton('Мужчина 18+ лет', callback_data="male")
  markup3.add(btn3, btn4)
  bot.send_message(message.from_user.id, 'Выберите возрастную категорию', reply_markup=markup3)

@bot.callback_query_handler(func=lambda call: call.data =="women")
def get_text_messages(message):
  markup3 = types.InlineKeyboardMarkup()
  btn3 = types.InlineKeyboardButton('Девочка 1-18лет(год)', callback_data="girl")
  btn4 = types.InlineKeyboardButton('Девушка 18+ лет', callback_data="female")
  markup3.add(btn3, btn4)
  bot.send_message(message.from_user.id, 'Выберите возрастную категорию', reply_markup=markup3)
@bot.callback_query_handler(func=lambda call: call.data =="male")
def get_text_messages(message):
  msg1 = bot.send_message(message.from_user.id, 'Введите свой вес(кг), рост(см) и возраст\n(через пробелы)')
  bot.register_next_step_handler(msg1, get_full_inf)
def get_full_inf(message):
  try:
    list = message.text.split()
    weight = list[0]
    height = list[1]
    age = list[2]

    url ="https://calculator-imt.com/cgi/bmi.pl?weight="+weight+"&height="+height+"&gender=male&age="+age
    headers ={
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
    }
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    bmi = soup.find("div", id="captureArea").text
    bmi =bmi.replace("© Copyright https://Calculator-IMT.com. All Rights Reserved", "").replace("is", "это")
    bot.send_message(message.from_user.id, bmi)
  except:
    bot.send_message(message.from_user.id, "Проверьте корректность введённых данных")


@bot.callback_query_handler(func=lambda call: call.data =="female")
def get_text_messages(message):
  msg1 = bot.send_message(message.from_user.id, 'Введите свой вес(кг), рост(см) и возраст\n(через пробелы)')
  bot.register_next_step_handler(msg1, get_full_inf1)
def get_full_inf1(message):
  try:
    list = message.text.split()
    weight = list[0]
    height = list[1]
    age = list[2]

    url ="https://calculator-imt.com/cgi/bmi.pl?weight="+weight+"&height="+height+"&gender=female&age="+age
    headers ={
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
    }
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    bmi = soup.find("div", id="captureArea").text
    bmi =bmi.replace("© Copyright https://Calculator-IMT.com. All Rights Reserved", "").replace("is", "это")
    bot.send_message(message.from_user.id, bmi)
  except:
    bot.send_message(message.from_user.id, "Проверьте корректность введённых данных")


@bot.callback_query_handler(func=lambda call: call.data =="boy")
def get_text_messages(message):
  msg1 = bot.send_message(message.from_user.id, 'Введите свой вес(кг), рост(см) и возраст\n(через пробелы)')
  bot.register_next_step_handler(msg1, get_full_inf2)
def get_full_inf2(message):
  try:
    list = message.text.split()
    weight = list[0]
    height = list[1]
    age = list[2]

    url ="https://calculator-imt.com/cgi/bmi_kids.pl?weight="+weight+"&height="+height+"&gender=boy&age="+age
    headers ={
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
    }
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    bmi = soup.find("div", id="captureArea").text
    bmi =bmi.replace("© Copyright https://Calculator-IMT.com. All Rights Reserved", "").replace("is", "это")
    bot.send_message(message.from_user.id, bmi)
  except:
    bot.send_message(message.from_user.id, "Проверьте корректность введённых данных")


@bot.callback_query_handler(func=lambda call: call.data =="girl")
def get_text_messages(message):
  msg1 = bot.send_message(message.from_user.id, 'Введите свой вес(кг), рост(см) и возраст\n(через пробелы)')
  bot.register_next_step_handler(msg1, get_full_inf3)
def get_full_inf3(message):
  try:
    list = message.text.split()
    weight = list[0]
    height = list[1]
    age = list[2]

    url ="https://calculator-imt.com/cgi/bmi_kids.pl?weight="+weight+"&height="+height+"&gender=girl&age="+age
    headers ={
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
    }
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    bmi = soup.find("div", id="captureArea").text
    bmi =bmi.replace("© Copyright https://Calculator-IMT.com. All Rights Reserved", "").replace("is", "это")
    bot.send_message(message.from_user.id, bmi)
  except:
    bot.send_message(message.from_user.id, "Проверьте корректность введённых данных")


bot.infinity_polling()