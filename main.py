# -*- coding: utf-8 -*-
import psycopg2,utils,importlib,asyncio
try:
	from dip import dp,bot
	from aiogram import executor
	import inline_buttons
	import logging
	import filter
	import handler
	if __name__ == '__main__':
		executor.start_polling(dp, skip_updates=True)
finally:
	open("debugger.log", "w").close()