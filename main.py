import telebot
from telebot import types
import json
import random

locations = []
descriptions = []

token = "6803079835:AAF8fpiTRyvrgzRfZTDtgf7SM9Q5AP_DdaE"

bot = telebot.TeleBot(token)

LOGIN_FILE = 'login.json'


@bot.message_handler(commands=['start'])  
def start(message):
  bot.send_message(message.chat.id, "Бот запущен")


@bot.message_handler(commands=['trash'])
def trash(message):
    with open('data.json') as f:
        data = json.load(f)
        locations = data["locations"]
        descriptions = data["descriptions"]

    random_location = random.choice(locations)

    index = random_location["index"]
    description = descriptions[index]["text"]

    latitude = random_location["latitude"]
    longitude = random_location["longitude"]

    url = f"https://yandex.ru/maps/-/CCUJ3z~n4B?ll={longitude},{latitude}&z=15"

    with open('data.json', 'w') as f:
        data = {
            "locations": locations,
            "descriptions": descriptions
        }
        json.dump(data, f)

    bot.send_message(message.chat.id, f"Локация удалена. Ссылка: {url}")
    bot.send_message(message.chat.id, f"Описание: {description}")

@bot.message_handler(content_types=['location'])
def save_location(message):

  location = {
    "index": len(locations),
    "latitude": message.location.latitude,
    "longitude": message.location.longitude
  }

  locations.append(location)

  bot.send_message(message.chat.id, "Отправьте описание")

@bot.message_handler(content_types=['text'])  
def save_description(message):

  last_location = locations[-1]  
  description = {
    "index": last_location["index"],
    "text": message.text
  }

  descriptions.append(description)

  with open('data.json', 'w') as f:
    data = {
      "locations": locations,
      "descriptions": descriptions
    }

    json.dump(data, f)

  bot.send_message(message.chat.id, "Описание сохранено")


bot.polling()
