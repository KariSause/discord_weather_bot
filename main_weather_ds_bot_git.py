import datetime
import discord
from discord.ext import commands
import random
import requests
#here write ur token
token_per_bot = ""

open_weather_token = "36d85f3aedda9f13d84d43968d0197e2"
client = discord.Client()

@client.event

async def on_ready():
   print("We have logged in as {0.user}".format(client))
@client.event
async def on_message(message):
   if message.author == client.user:
         return
   messagelist = list(message.content)
   if messagelist[0] == "!":
      city = ""
      
      message.content = ''.join(message.content.split("!", 1))
      if message.content.lower() == "!погода":
         await message.channel.send("Привіт! Напиши мені назву міста і я пришлю погоду! (Назву міста пиши на английській, пример: !London, !Tokyo)")
      else:
         city = message.content
         print(city)
      code_to_smile = {
        "Clear": "Сонячно \U00002600",
        "Clouds": "Хмарно \U00002601",
        "Rain": "Дощ \U00002614",
        "Drizzle": "Невеликий дощ \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Сніг \U0001F328",
        "Mist": "Туман \U0001F32B"
      }
    
   try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.content}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Не знаю, що це за погода"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

        await message.reply(f"---{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}---\n"
        f"Погода в місті: {city}\nТемпература: {cur_weather}°C \n{wd}\n"
        f"Вологість: {humidity}%\nАтмосферний тиск: {pressure} мм.рт.ст\nВітер: {wind}м/с\n"
        f"Схід сонця: {sunrise}\nЗахід сонця {sunset}\nТривалість дня: {length_of_the_day} \nГарного дня!")
    
    
   except:
      if messagelist[0] == "!":
       await message.reply("\U00002620 Перевір назву міста \U00002620")
      else:
         print('Just chat')
    
    
     
      


client.run(token_per_bot)