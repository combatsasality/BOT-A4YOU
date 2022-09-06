import logging,os,time
from filter import BlackList, InGroupTest, InGroupTestCall, IsOwner, Tex
from aiogram import Bot, Dispatcher, types
from aiohttp import log
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton,ReplyKeyboardMarkup,KeyboardButton,ReplyKeyboardRemove
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

TOKEN = "INSERT HERE"
#log.client_logger.setLevel(logging.CRITICAL)
file_log = logging.FileHandler('debugger.log')
console_out = logging.StreamHandler()   
if os.name.lower() == "posix":   
    os.environ['TZ'] = 'Europe/Kiev'  
    time.tzset()
logging.basicConfig(handlers=(file_log, console_out),level=logging.INFO, format="[%(asctime)s][%(levelname)s] %(message)s",datefmt='%d-%m-%Y %H:%M:%S')


storage = MemoryStorage()
type = types.Message
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


dp.filters_factory.bind(IsOwner)
dp.filters_factory.bind(InGroupTest, event_handlers=[dp.message_handlers])
dp.filters_factory.bind(InGroupTestCall, event_handlers=[dp.callback_query_handlers])
dp.filters_factory.bind(BlackList, event_handlers=[dp.callback_query_handlers])
dp.filters_factory.bind(Tex, event_handlers=[dp.callback_query_handlers])