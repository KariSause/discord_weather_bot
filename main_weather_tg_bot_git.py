import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from pprint import pprint

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши мне название города и я пришлю сводку погоды! (Название города пиши на английском, пример: London, Tokyo)")


@dp.message_handler()
async def get_weather(message: types.Message):
    print(message["from"]["username"], ": ", message.text, "\nLanguage Code: ", message["from"]["language_code"], "\nБот: " ,message["from"]["is_bot"], "\n\n" )
    #print(message)
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Небольшой дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }
    
    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        #print(data)
        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что за погода"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

        await message.reply(f"---{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}---\n"
        f"Погода в городе: {city}\nТемпература: {cur_weather}°C \n{wd}\n"
        f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind}м/с\n"
        f"Восход солнца: {sunrise}\nЗакат солнца {sunset}\nПродолжительность дня: {length_of_the_day} \nХорошего дня!")
    
    
    except:
       await message.reply("\U00002620 Проверьте название города \U00002620")


if __name__ == "__main__":
    executor.start_polling(dp)