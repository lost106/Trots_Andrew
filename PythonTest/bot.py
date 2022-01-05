import telebot
from urllib.request import urlopen
from bs4 import BeautifulSoup

bot = telebot.TeleBot("5094259825:AAGa382TG5IzAHTjV8kDi2WaTF0vPPlS4vo")

@bot.message_handler(commands=['start', 'hello'])
def start_message(message):
    bot.send_message(message.chat.id, "hello")

@bot.message_handler(commands=['update'])
def update_message(message):
    html = urlopen('https://kurs.onliner.by/')
    soup = BeautifulSoup(html)
    tag_list = soup.find_all('p', {'class':'value rise'})
    buy = tag_list[0].text
    sell = tag_list[1].text
    bot.send_message(message.chat.id, buy + ", " + sell)

bot.polling()

