#! /usr/bin/env python
# -*- coding: utf-8 -*-

from urllib import request
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import telebot
import time
from telebot import types

token = '286099721:AAEosVONIGX_DMoaxJIGiqSUEx296uFhhiI'
bot = telebot.TeleBot(token)

def booking_all(url):
    bl = []
    boking_list = []
    count = 0
    url_request = request.urlopen(url)
    url_read = url_request.read()
    soup = BeautifulSoup(url_read, "html.parser")
    t = soup.find_all('script')
    for i in range(len(t)):
        if (str(t[i])[0:51]=='<script>\n        VZ = VZ || {};\n        VZ.slots = '):
            text = (str(t[i])[str(t[i]).find('[')+1:str(t[i]).find(']')])
            l = text[1:-1].split('},{')
            for i in l:
                    if (i[i.find('status')+9:i.find('datetime')-3] != 'closed') & (i[i.find('status')+9:i.find('datetime')-3] != 'open'):
                        boking_list.append(i)
                        count+=1

    for i in range (len(boking_list)):
        ts = boking_list[i].split(',')[2].split(':')[1].replace('"','')
        ts = int(ts)+(3*60*60)
        bl.append(time.ctime(ts))
    return bl

# @bot.message_handler(content_types=["text"])
def text_case(message): # Название функции не играет никакой роли, в принципе

    if message.text =='Проверить количество броней':
        # str(booking_all('http://vzaperti.com.ua/quest/empire'))
        bokking_empire = str(booking_all('http://vzaperti.com.ua/quest/empire')).replace("2017'", '\n').replace("'", '').replace('[','').replace(', ', '').replace(']', '')
        bokking_crime = str(booking_all('http://vzaperti.com.ua/quest/crime')).replace("2017'", '\n').replace("'",'').replace('[', '').replace(', ', '').replace(']', '')
        text = '\nПодпольная империя:\n '+ bokking_empire+'\nИдеальное преступление:\n '+bokking_crime
        bot.send_message(message.chat.id, text)
    else:
        text = 'ну'
        bot.send_message(message.chat.id, text) 
    
# @bot.message_handler(commands=["start"]) 
@bot.message_handler(content_types=["text"])
def start(m):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Проверить количество броней']])
    msg = bot.send_message(m.chat.id, 'Количество броней:', reply_markup=keyboard)  
    bot.register_next_step_handler(msg, text_case)
    
    
bot.polling(none_stop=True)
    
    
    
