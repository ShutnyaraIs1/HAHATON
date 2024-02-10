import telebot
from telebot import types
import json
import random

locations = []
descriptions = []

token = "Тут Ваш токен! :0"

bot = telebot.TeleBot(token)

LOGIN_FILE = 'login.json'


@bot.message_handler(commands=['start'])
def start(message):
  keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
  button_1 = types.KeyboardButton("Басурман")
  button_2 = types.KeyboardButton("Герой сказки")
  keyboard.add(button_1, button_2)
  
  bot.send_message(message.chat.id, "Выберите, кем вы являетесь:", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "Басурман")  
def basurman(message):
  bot.send_message(message.chat.id, "Увы, басурманам дорога закрыта! Ступайте обратно себе в хоромы мусорные!")

@bot.message_handler(func=lambda message: message.text == "Герой сказки")
def geroy(message):
  bot.send_message(message.chat.id, "Добро пожаловать, путник! Ты встал на путь праведный и теперь желаешь помочь берегам Азовского моря избавиться от мусорного басурманства... Тогда тебе к нам! Поделись гео-локацией c нахождением мусорного басурманства или напиши команду /trash, чтобы посмотреть папирусы с дорогами крутыми до мусорных басурманств!")

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

    bot.send_message(message.chat.id, f"Вот тебе путник свет вездесущий! Путь до папируса с дорогами крутыми: {url} \nПисьмена, оставленные твоими братьями и сестрами: {description}")

@bot.message_handler(content_types=['location'])
def save_location(message):

  location = {
    "index": len(locations),
    "latitude": message.location.latitude,
    "longitude": message.location.longitude
  }

  locations.append(location)

  bot.send_message(message.chat.id, "Начеркайте письмена для большего понимания, сколько понадобиться Ваших братьев и сестер для зачистки сие войска мусорного басурманства:")

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

  bot.send_message(message.chat.id, "Письмена сохранены и будут переданы Вашим братья и сестрам!")


bot.polling()
