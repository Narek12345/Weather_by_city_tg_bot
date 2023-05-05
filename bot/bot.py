import requests

from aiogram import types, Bot
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher

import config


bot = Bot(token=config.tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def start_bot(message: types.Message):
	if message.text == '/help':
		await message.reply(f"Добро пожаловать! Я могу подсказать вам погоду в разных городах по всему миру, а ваша маленькая цель, это писать название городов правильно. Давайте проверим, как это работает. Введите название любого города: ")
	elif message.text == '/start':
		await message.answer("Добро пожаловать! Введите правильно название города: ")


@dp.message_handler()
async def takes_name_of_city(message: types.Message):
	"""Takes the name of the city, then finds information about it and sends."""

	city = message.text

	try:
		# Ссылка на сайт OpenWeather.
		link = "https://api.openweathermap.org/data/2.5/weather?"
		# Указываем параметры для ссылки.
		params = dict(q=city, appid=config.openweather_api_key, units='metric', lang='ru')

		# Делаем запрос.
		r = requests.get(link, params)

		# Обрабатываем полученные данные в формате json.
		data = r.json()

		# Получаем текущую температуру из json.
		current_temp = data['main']['temp']

		# Максимальная температура.
		max_temp = data['main']['temp_max']

		# Минимальная температура.
		min_temp = data['main']['temp_min']



		# Бот отправляет данные пользователю.
		await message.reply(f"Текущая температура: {current_temp}\n"\
							f"Максимальная температура: {max_temp}\n"\
							f"Минимальная температура: {min_temp}")

	except:
		await message.reply("К сожалению, я не смог найти такой город. Попробуйте проверить его название и ввести еще раз.")




if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)