# -*- coding: utf-8 -*-
from dip import dp,bot,type,types
import aiogram,random,os,aiohttp,json,asyncio
from hack import hacknaurok,hackvseo
from utils import setbalance,getman



@dp.message_handler(commands=["naurok"], is_owner=True)
async def naurok(message:type):
    sesid = await hacknaurok.GetSessiondId(message.text.split()[1])
    if sesid == "NotNaurok":
        await bot.send_message(message.chat.id, "Не похоже на тест")
    elif sesid == "TestEnded":
        await bot.send_message(message.chat.id, "Другалек, ты не успел(((")
    else:
        await bot.send_message(message.chat.id, "Начинаю решать...")
        quest = await hacknaurok.GetQuestions(sesid)
        itog = await hacknaurok.itog(quest)
        idfile = random.randint(1000, 9999)
        f = open(f"{idfile}.html", "w+", encoding='utf-8')
        f.write(itog)
        f.close()
        await bot.send_document(message.chat.id, open(f"{idfile}.html", "rb"))
        os.remove(f"{idfile}.html")

@dp.message_handler(commands=["vseosvita"], is_owner=True)
async def vseosvita(message:type):
    html = await hackvseo.HackVseo(message.text.split()[1])
    if html == "NeVseOsvita":
        await bot.send_message(message.chat.id, "Это не ВсеОсвита")
    elif html == "TestEnded":
        await bot.send_message(message.chat.id, "Тест закончился")
    else:
        idfile = random.randint(1000, 9999)
        f = open(f"{idfile}.html", "w+", encoding='utf-8')
        f.write(html["HTMLANSWER"])
        f.close()
        await bot.send_document(message.chat.id, open(f"{idfile}.html", "rb"))
        os.remove(f"{idfile}.html")
