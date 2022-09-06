import re
import aiohttp,aiohttp
from dip import InlineKeyboardMarkup,InlineKeyboardButton,dp,types,bot,State, StatesGroup,Text,FSMContext
from aiogram.types.chat_member import ChatMember
from hack import hacknaurok,hackvseo
import aiogram,time,random,os,utils,logging,importlib,asyncio
from utils import AddLogs, DelLogs, DellMan, GetLogs, dellviruchka, getbalance,getman,setbalance,getviruchka,SetFalse,SetTrue,GetEnabled,c,conn


#SpecialAction = InlineKeyboardMarkup().add(InlineKeyboardButton("Первый вариант", callback_data="yes")).add(InlineKeyboardButton("Второй вариант", callback_data="no"))

@dp.message_handler(commands=["debug"], is_owner=True)
async def debug (message: type):
    try:
        if ''.join(message.text.split()[1:2]) == "file":
            await bot.send_document(message.chat.id, open("debugger.log", "rb"))
        else:
            f = open("debugger.log", "r")
            log = f.read()
            await bot.send_message(message.chat.id, log)
    except aiogram.utils.exceptions.MessageIsTooLong:
         await bot.send_document(message.chat.id, open("debugger.log", "rb"))

@dp.message_handler(commands=["setbalance"], is_owner=True)
async def set(message:type):
    try:
        id = message.text.split()[1]
        balance = message.text.split()[2]
        man = getman(id)
        if man == None:
            await bot.send_message(message.chat.id, "Такого челика не существует в базе данных!")
        else:
            setbalance(id, balance)
            await bot.send_message(message.chat.id, "Баланс успешно установлен!")
            newman = getman(id)
            await bot.send_message(id, f"Администратор установил ваш баланс на {str(newman[3])} грн")
            logging.info(f"[CMD:setbalance][ID:{message.from_user.id}] id - {id}, old balance - {man[3]}, new balance - {newman[3]}")
    except IndexError:
        await bot.send_message(message.chat.id, "Пример команды: /setbalance ID BALANCE")

@dp.message_handler(commands=["getbalance"], is_owner=True)
async def get(message:type):
    try:
        id = message.text.split()[1]
        man = getman(id)
        if man == None:
            await bot.send_mesasge(message.chat.id, "Такого челика нема в бд")
        else:
            await bot.send_message(message.chat.id, f"ID - {man[0]}\nUserName - @{man[1]}\nFirstName - {man[2]}\nBalance - {man[3]}")
        logging.info(f"[CMD:getbalance][ID:{message.from_user.id}] id - {id}")
    except IndexError:
        await bot.send_message(message.chat.id, "Пример команды: /getbalance ID ")

@dp.message_handler(commands=["reload"], is_owner=True)
async def reload(message:type):
    importlib.reload(utils)
    importlib.reload(hackvseo)
    await bot.delete_message(message.chat.id, message.message_id)
    logging.info("[CMD:reload] Cursor reload and hack vseo!")
@dp.message_handler(commands=["notify"], is_owner=True)
async def notify(message:type):
    c.execute("select * from users")
    x = c.fetchall()
    await bot.send_message(message.chat.id, "Запустил рассылку!")
    for p in x:
        try:
            await bot.send_message(p[0],' '.join(message.text.split()[1:]).replace("\\n", "\n"), parse_mode="HTML")
            await asyncio.sleep(1.5)
        except aiogram.utils.exceptions.BotBlocked:
            pass
        except aiogram.utils.exceptions.UserDeactivated:
            pass
        except:
            pass
    await bot.send_message(message.chat.id, "Рассылка закончена !")

@dp.message_handler(commands=["test"],is_owner=True)
async def test(message:type):
    utils.InsertAllBalance(message.from_user.id, 0+10)
@dp.message_handler(commands=["test2"],is_owner=True)
async def test2(message:type):
    await test(message)
@dp.message_handler(commands=["addpromo"], is_owner=True)
async def addpromo(message:type):
    try:
        if int(message.text.split()[3]) <= 0:
            c.execute("insert into promo (id,summa) values (%s,%s)", (message.text.split()[1].lower(),message.text.split()[2]))
            conn.commit()
            await bot.send_message(message.chat.id, F"ПРОМОКОД: {message.text.split()[1]} на {message.text.split()[2]} грн запущен до конца месяца! На бесконечно использований")
        else:
            c.execute("insert into promo (id,summa,count) values (%s,%s,%s)", (message.text.split()[1].lower(),message.text.split()[2],message.text.split()[3]))
            conn.commit()
            await bot.send_message(message.chat.id, F"ПРОМОКОД: {message.text.split()[1]} на {message.text.split()[2]} грн запущен до конца месяца! На {message.text.split()[3]} использований")
        logging.info(f"[CMD:addpromo][ID:{message.from_user.id}] Promo:{message.text.split[1]}, Usage:{message.text.split()[3]}, Money:{message.text.split()[2]} ")
    except:
        await bot.send_message(message.chat.id, f"/addpromo PROMO 1 (БЕЗ КОПЕЕК НАХУЙ ВСЕ СЛОМАЕТ!!!!!!!!!) использования")


@dp.message_handler(commands=["logs"], is_owner=True)
async def logs(message:type):
    try:
        stroka = ""
        logs = GetLogs()
        for i in logs:
            stroka+=f"[{str(i[0])[0:19]}] {i[1]}\n"
        if len(stroka) > 4096:
            for x in range(0, len(stroka), 4096):
                await bot.send_message(message.chat.id, stroka[x:x+4096], parse_mode="HTML")
        else:
            await bot.send_message(message.chat.id, stroka, parse_mode="HTML")
    except aiogram.utils.exceptions.MessageTextIsEmpty:
        await bot.send_message(message.chat.id, "Логи пусты!")
@dp.message_handler(commands=["clearlogs"], is_owner=True)
async def logs(message:type):
    DelLogs()
    await bot.send_message(message.chat.id, "Логи очищены!")
    logging.info(f"[CMD:clearlogs][ID:{message.from_user.id}] Successfully ")



@dp.message_handler(commands=["tex"], is_owner=True)
async def text(message:type):
    enabled = GetEnabled()
    if enabled == True:
        SetFalse()
        await bot.send_message(message.chat.id, "Бот отключен!")
    elif enabled == False:
        SetTrue()
        await bot.send_message(message.chat.id, "Бот включен")

@dp.message_handler(commands=["ban"], is_owner=True)
async def ban(message:type):
    try:
        if message.text.split()[1] in [620038501, 1132697406]:
            await bot.send_message(message.chat.id, "Пошел как ты нахуй кентик)))))")
            return 
        if len(message.text.split()) >= 3:
            c.execute("insert into blacklist (id,reason) values (%s,%s) on conflict (id) do update set reason = %s", (message.text.split()[1], ' '.join(message.text.split()[2:]), ' '.join(message.text.split()[2:])))
        else: 
            c.execute("insert into blacklist (id,reason) values (%s,%s) on conflict (id) do update set reason = %s", (message.text.split()[1], None, None))
        conn.commit()
        await bot.send_message(message.chat.id, "Человек успешно добавлен в блэклист!")
    except IndexError:
        await bot.send_message(message.chat.id, "/ban id reason")

@dp.message_handler(commands=["unban"], is_owner=True)
async def unban(message:type):
    try:
        c.execute("delete from blacklist where id = %s", (message.text.split()[1],))
        conn.commit()
        await bot.send_message(message.chat.id, "Человек успешно удален из блэклиста!")
    except IndexError:
        await bot.send_message(message.chat.id, "/unban id")

@dp.message_handler(commands=["fornikita"])
async def hacknauroks(message:type):
    if message.from_user.id in [1032987829, 2134067360]:
        try:
                sesid = await hacknaurok.GetSessiondId(message.text.split()[1])
                if sesid == "NotNaurok":
                    await bot.send_message(message.chat.id, "Не похоже на тест")
                elif sesid == "TestEnded":
                    await bot.send_message(message.chat.id, "Тест закончен")
                elif sesid == "WrongURL":
                    await bot.send_message(message.chat.id, "Чаво? Обратись к админам")
                else:
                    await bot.send_message(message.chat.id, "Начинаю решать тест.....")
                    quest = await hacknaurok.GetQuestions(sesid)
                    itog = await hacknaurok.itog(quest)
                    idfile = random.randint(1000, 9999)
                    f = open(f"{idfile}.html", "w+", encoding='utf-8')
                    f.write(itog)
                    f.close()
                    await bot.send_document(message.chat.id, open(f"{idfile}.html", "rb"))
                    os.remove(f"{idfile}.html")
        except IndexError:
            await bot.send_message(message.chat.id, "Неправильно! Пример: /fornikita URL - вместо URL, первая ссылка вопроса(Это надо зайти под своем именем и скинуть боту)")

