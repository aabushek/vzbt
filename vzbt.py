#! /usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
from bs4 import BeautifulSoup
import datetime
import requests
import telebot

token = '286099721:AAEosVONIGX_DMoaxJIGiqSUEx296uFhhiI'
bot = telebot.TeleBot(token)

def log(message, answer):
    print('\nuser:',message.from_user.first_name, message.from_user.last_name,'\nuser_text:', message.text, '\nanswer: ',answer)

    # print('Сообщение от {0} {1}. (id = {2}) \n Текст - {3}'.format(message.from_user.first_name, message.from_user.last_name,str(message.from_user.id,message.text)))
    # print(answer)

def booking_now(url):

    url_request = urllib.request.urlopen(url)
    url_read = url_request.read()
    soup = BeautifulSoup(url_read, "html.parser")
    t = soup.find_all('script')
    dictionary = 'Перерыв :)'
    for i in range(len(t)):
        if (str(t[i])[0:51]=='<script>\n        VZ = VZ || {};\n        VZ.slots = '):
            text = (str(t[i])[str(t[i]).find('[')+1:str(t[i]).find(']')])
            l = text[1:-1].split('},{')
            for i in l:
                start_time = int(i[i.find('datetime')+11:i.find(',"datetime_no_tz"')-1])
                end_time = start_time+3600
                now = datetime.datetime.now().timestamp()
                if (now>start_time)&(now<end_time):
                    res = i.replace('null','"unknown"').split(',')
                    keys = []
                    values = []
                    for i in range(len(res)):
                        keys.append(res[i].split(':')[0].replace('"',''))
                        values.append(res[i].split(':')[1].replace('"',''))
                        dictionary = dict(zip(keys, values))
    if dictionary == 'Перерыв :)':
        responce = 'Перерыв :)'
        return responce
    else:
        date_from = datetime.datetime.fromtimestamp(int(dictionary['datetime'])).strftime('%Y-%m-%d %H:%M:%S')
        date_to = datetime.datetime.fromtimestamp(int(dictionary['datetime'])+3600).strftime('%Y-%m-%d %H:%M:%S')
        responce = 'Start: '+str(date_from)+' End: '+str(date_to)+' Status:'+dictionary['status']
        return responce


def booking_all(url):
    count = 0
    now = datetime.datetime.now().timestamp()
    url_request = urllib.request.urlopen(url)
    url_read = url_request.read()
    soup = BeautifulSoup(url_read, "html.parser")
    t = soup.find_all('script')
    for i in range(len(t)):
        if (str(t[i])[0:51]=='<script>\n        VZ = VZ || {};\n        VZ.slots = '):
            text = (str(t[i])[str(t[i]).find('[')+1:str(t[i]).find(']')])
            l = text[1:-1].split('},{')
            for i in l:
                start_time = int(i[i.find('datetime')+11:i.find(',"datetime_no_tz"')-1])
                start_day = datetime.datetime.fromtimestamp(int(start_time)).strftime('%Y-%m-%d')
                today = datetime.datetime.fromtimestamp(int(now)).strftime('%Y-%m-%d')
                if start_day == today:
                    if (i[i.find('status')+9:i.find('datetime')-3] != 'closed') & (i[i.find('status')+9:i.find('datetime')-3] != 'open'):
                        count+=1

    return count

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
    # bot.send_message(message.chat.id, message.text)
    # user_markup

    if message.text == 'crime':
        text = 'Идеальное преступление: ' + str(booking_now('http://vzaperti.com.ua/quest/crime'))
        log(message, text)
        bot.send_message(message.chat.id, text)
    elif message.text == 'empire':
        text = 'Подпольная империя: ' + str(booking_now('http://vzaperti.com.ua/quest/empire'))
        log(message, text)
        bot.send_message(message.chat.id, text)

    elif message.text =='count':
        text = 'Количество броней \nПодпольная империя: '+ str(booking_all('http://vzaperti.com.ua/quest/empire'))+'\nИдеальное преступление: '+str(booking_all('http://vzaperti.com.ua/quest/crime'))
        log(message, text)
        bot.send_message(message.chat.id, text)
    else:
        text = 'ну'
        log(message, text)
        bot.send_message(message.chat.id, text)
if __name__ == '__main__':
    bot.polling(none_stop=True)