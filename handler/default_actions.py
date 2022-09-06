
from dip import dp,bot,type,InlineKeyboardMarkup,InlineKeyboardButton, logging
from utils import insertuser,getbalance,getman,InsertRef
from inline_buttons import MainMenu,nazad,nazadhelp
import json

Config = json.loads(open("configuration.json", "r", encoding="utf-8").read())

@dp.message_handler(commands=["start"])
async def start(message:type):
    man = getman(message.from_user.id)
    if man == None:
        id = message.text.split()
        if len(id) >= 2:
            if id[1] != message.from_user.id and getman(id[1]) != None:
                InsertRef(message.from_user.id, message.from_user.first_name, id[1], message.from_user.username)
    insertuser(message.from_user.id, message.from_user.first_name, message.from_user.username)
    balance = getbalance(message.chat.id)
    await bot.send_message(message.chat.id, Config["LastChange"], parse_mode="HTML", reply_markup=MainMenu)
@dp.message_handler(commands=["id"])
async def test(message:type):
    await bot.send_message(message.chat.id, f"ID: {message.from_user.id}")
@dp.message_handler(commands=["info"])
async def info(message:type):
    await bot.send_message(message.chat.id, Config["HelpMenu"], parse_mode="HTML", disable_web_page_preview=True, reply_markup=nazadhelp)