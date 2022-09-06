from dip import InlineKeyboardMarkup,InlineKeyboardButton,dp,types,bot,State, StatesGroup,Text,FSMContext,ReplyKeyboardMarkup,ReplyKeyboardRemove,KeyboardButton
import os,json,aiohttp,aiogram,datetime
from hack import autovseosvita
from hack.autovseosvita import autovseo
from utils import ChangeToMainMenu, CheckRefers, getman,getbalance,setbalance,insertuser,CheckEnabled,VozvratToMenu,AddLogs,c,conn,times,InsertAllBalance,minusallbalance
from hack import autonaurok, hackvseo,hacknaurok
from random import randint
from datetime import datetime, timedelta

Config = json.loads(open("configuration.json", "r", encoding="utf-8").read())


MainMenu = InlineKeyboardMarkup()

AddBalance = InlineKeyboardButton("💳Пополнить баланс💳", callback_data="AddBalance")
VseOsvita = InlineKeyboardButton("📘ВсеОсвита📘", callback_data="VseOsvita")
NaUrok = InlineKeyboardButton("📙НаУрок📙", callback_data="Naurok")
FAQ = InlineKeyboardButton("❓ЧаВо❓", callback_data="FAQ")
HELP = InlineKeyboardButton("👺Помощь👺", callback_data="HELP")
REFER = InlineKeyboardButton("✉️Реферальная система✉️", callback_data="REFER")
MainMenu.add(AddBalance)
MainMenu.row(VseOsvita,NaUrok)
MainMenu.add(REFER)
MainMenu.row(HELP)

nazad = InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️Назад", callback_data="NAZAD"))
#FAQMENU = InlineKeyboardMarkup().row(InlineKeyboardButton("ВсеОсвита", url="https://youtu.be/SIjLU-TO9po"), InlineKeyboardButton("НаУрок", url="https://youtu.be/PRRCbOOnsQY")).add(InlineKeyboardButton("⬅️Назад", callback_data="NAZAD"))

vseosvitahelp = InlineKeyboardButton("Помощь по ВсеОсвите", url="https://youtu.be/SIjLU-TO9po")
naurokhelp = InlineKeyboardButton("Помощь по НаУроку", url="https://youtu.be/wtrYyAuJ2Ck")
vvedkoda = InlineKeyboardMarkup().add(InlineKeyboardButton("Как пополнить баланс?", url="https://telegra.ph/Kak-popolnit-balans-v-A4U-BOT-08-03")).row(InlineKeyboardButton("Ввести код", callback_data="VvedKoda"), InlineKeyboardButton("Ввести промокод", callback_data="PromoCode")).add(InlineKeyboardButton("⬅️Назад", callback_data="NAZAD"))
stop = InlineKeyboardMarkup().add(InlineKeyboardButton("⛔️CТОП⛔️", callback_data="stop"))


vibornaurok = InlineKeyboardMarkup().add(InlineKeyboardButton("Обычное получение ответов", callback_data="TypicalNaurok")).add(InlineKeyboardButton("Авто-прохождение теста", callback_data="AutoProxodNaurok")).add(InlineKeyboardButton("⬅️Назад", callback_data="NAZAD"))

viborvseosvita = InlineKeyboardMarkup().add(InlineKeyboardButton("Обычное получение ответов", callback_data="TypicalVseOsvita")).add(InlineKeyboardButton("Авто-прохождение теста", callback_data="AutoProxodVseOsvita")).add(InlineKeyboardButton("⬅️Назад", callback_data="NAZAD"))

class Form(StatesGroup):
    oplata = State()
    promocode = State()
    vseosvita = State()
    naurok = State()
    OneStepAutoProxodNaUrok = State()
    TwoStepAutoProxodNaUrok = State()
    ThreeStepAutoProxodNaUrok = State()
    FinallyStepAutoProxodNaUrok = State()
    VseOsvita1Auto = State()
    VseOsvita2Auto = State()
    VseOsvita3Auto = State()
    VseOsvita4Auto = State()
    VseOsvita5Auto = State()
#NaUrok
OneStepAutoNaurok = InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️Назад", callback_data="OneStepAutoNaurokNAZAD"))
TwoStepAutoNaurok = InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️Назад", callback_data="TwoStepAutoNaurokNAZAD"))
ThreeStepAutoNaUrok = InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️Назад", callback_data="ThreeStepAutoNaurokNAZAD"))
FinallyStepAutoNaUrok = InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️Назад", callback_data="FinallyStepAutoNaurokNAZAD")).add(InlineKeyboardButton("⛔️CТОП⛔️", callback_data="stop"))
#VseOsvita
VseOsvita1AutoMarkup = InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️Назад", callback_data="VseOsvita1AutoNAZAD"))
VseOsvita2AutoMarkup = InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️Назад", callback_data="VseOsvita2AutoNAZAD"))
VseOsvita3AutoMarkup = InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️Назад", callback_data="VseOsvita3AutoNAZAD"))
VseOsvita4AutoMarkup = InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️Назад", callback_data="VseOsvita4AutoNAZAD"))
VseOsvita5AutoMarkup = InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️Назад", callback_data="VseOsvita5AutoNAZAD"))

@dp.callback_query_handler(lambda call: call.data, black_list=True)
async def callbackquery(call: types.CallbackQuery, state: FSMContext):
    messagecall = call.message.message_id
    if call.from_user.username == None:
        insertuser(call.from_user.id, None, call.from_user.first_name)
    else:
        insertuser(call.from_user.id, call.from_user.username, call.from_user.first_name)
    if call.data == "AddBalance": #Добавление балика
        enabled = await CheckEnabled(call.message.chat.id, messagecall)
        if enabled == "NoEnabled" and call.from_user.id not in [620038501, 1132697406]:
            return
        await bot.edit_message_text("Пополнение баланса\nК сожалению баланс можно пополнить только от 20 грн\!\nК сожалению подругому никак😫\n[Сайт для пополнения](https://bitobmen.pro/ua/)\n❗️Возврат средств не осуществляется❗️",call.message.chat.id, messagecall, reply_markup=vvedkoda, parse_mode="MarkDownV2", disable_web_page_preview=True)
    elif call.data == "VseOsvita": #ВсеОсвита
        enabled = await CheckEnabled(call.message.chat.id, messagecall)
        if enabled == "NoEnabled" and call.from_user.id not in [620038501, 1132697406]:
            return
        await bot.edit_message_text("Обычное получение ответов: Бот дает тебе ответы ты сам проходишь тест\nАвто-прохождение теста: Бот проходит за тебя тест(Дороже)",call.message.chat.id, messagecall, reply_markup=viborvseosvita)
    elif call.data == "AutoProxodVseOsvita": 
        enabled = await CheckEnabled(call.message.chat.id, messagecall)
        if enabled == "NoEnabled" and call.from_user.id not in [620038501, 1132697406]:
            return
        x = await bot.edit_message_text("Следующим сообщением отправьте ссылку на вход теста", call.message.chat.id, messagecall, reply_markup=VseOsvita1AutoMarkup)
        await Form.VseOsvita1Auto.set()
        async with state.proxy() as data:
            data["id"] = x.message_id  
    elif call.data == "TypicalVseOsvita":
        enabled = await CheckEnabled(call.message.chat.id, messagecall)
        if enabled == "NoEnabled" and call.from_user.id not in [620038501, 1132697406]:
            return
        await Form.vseosvita.set()
        await bot.edit_message_text("Следующим сообщением отправьте ссылку на первый вопрос теста", call.message.chat.id, messagecall, reply_markup=stop, parse_mode="HTML")
        async with state.proxy() as data:
            data["id"] = messagecall
    elif call.data == "Naurok": #NAUROK
        enabled = await CheckEnabled(call.message.chat.id, messagecall)
        if enabled == "NoEnabled" and call.from_user.id not in [620038501, 1132697406]:
            return
        await bot.edit_message_text("Обычное получение ответов: Бот дает тебе ответы ты сам проходишь тест\nАвто-прохождение теста: Бот проходит за тебя тест(Дороже)", call.message.chat.id, messagecall, reply_markup=vibornaurok)       
    elif call.data == "AutoProxodNaurok": 
        enabled = await CheckEnabled(call.message.chat.id, messagecall)
        if enabled == "NoEnabled" and call.from_user.id not in [620038501, 1132697406]:
            return
        x = await bot.edit_message_text("Следующим сообщением отправьте ссылку на первый вопрос теста", call.message.chat.id, messagecall, reply_markup=OneStepAutoNaurok)
        await Form.OneStepAutoProxodNaUrok.set()
        async with state.proxy() as data:
            data["id"] = x.message_id  
    elif call.data == "TypicalNaurok":
        enabled = await CheckEnabled(call.message.chat.id, messagecall)
        if enabled == "NoEnabled" and call.from_user.id not in [620038501, 1132697406]:
            return
        await Form.naurok.set()
        await bot.edit_message_text("Следующим сообщением отправьте ссылку на первый вопрос теста", call.message.chat.id, messagecall, reply_markup=stop, parse_mode="HTML")
        async with state.proxy() as data:
            data["id"] = messagecall
    elif call.data == "VvedKoda":
        enabled = await CheckEnabled(call.message.chat.id, messagecall)
        if enabled == "NoEnabled" and call.from_user.id not in [620038501, 1132697406]:
            return
        await Form.oplata.set()
        await bot.edit_message_text("Введите код который вы получили на BitObmen", call.message.chat.id,messagecall,reply_markup=stop)
        async with state.proxy() as data:
            data["id"] = messagecall
    elif call.data == "PromoCode":
        enabled = await CheckEnabled(call.message.chat.id, messagecall)
        if enabled == "NoEnabled" and call.from_user.id not in [620038501, 1132697406]:
            return
        await Form.promocode.set()
        await bot.edit_message_text("Введите код который вы получили от администраторов", call.message.chat.id,messagecall,reply_markup=stop)
        async with state.proxy() as data:
            data["id"] = messagecall     
    elif call.data == "FAQ":
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=messagecall, text="Помощь по функционалу бота", disable_web_page_preview=True)
    elif call.data == "HELP":
        await bot.edit_message_text(chat_id=call.message.chat.id,  message_id=messagecall, text="Ссылки на инфо канал: https://t.me/answers4you\nСсылка на канал для общения и <b>получения помощи</b>: https://t.me/answers4youchat\n\nНаурок - ответы приходят в виде файла который вам нужно открыть(файл откроется в браузере, телеграм может ругаться на файл так как к нему не привязан ip)\n\nВсеосвита - аналогично НаУроку", parse_mode="HTML", disable_web_page_preview=True, reply_markup=nazad)
    elif call.data == "REFER":
        referrs = CheckRefers(call.from_user.id)
        if referrs == None:
            await bot.edit_message_text("Вот ваша персональна реферальная ссылка:\n"+ f"<code>https://t.me/answers4youbot?start={call.from_user.id}</code>\nУсловия реферальной системы: За каждого человека которого вы пригласили и он пополнил 30 грн, вы получаете - 5 грн\nНа данный момент у вас: 0 рефералов", call.message.chat.id,messagecall,reply_markup=nazad, parse_mode="HTML")
        else:
            await bot.edit_message_text("Вот ваша персональна реферальная ссылка:\n"+ f"<code>https://t.me/answers4youbot?start={call.from_user.id}</code>\nУсловия реферальной системы: За каждого человека которого вы пригласили и он пополнил 30 грн, вы получаете - 5 грн\nНа данный момент у вас: {len(referrs)} реферал/-а/-ов", call.message.chat.id,messagecall,reply_markup=nazad, parse_mode="HTML")
    elif call.data == "stop": #Стоп решения тестов
        await ChangeToMainMenu(call.message.chat.id, messagecall)
    elif call.data == "NAZAD": #Кнопка чтобы вернутся к главному меню
        await ChangeToMainMenu(call.message.chat.id, messagecall)
    elif call.data == "OneStepAutoNaurokNAZAD" or call.data == "TwoStepAutoNaurokNAZAD" or call.data == "ThreeStepAutoNaurokNAZAD" or call.data == "FinallyStepAutoNaurokNAZAD" or call.data == "VseOsvita1AutoNAZAD" or call.data == "VseOsvita2AutoNAZAD" or call.data == "VseOsvita3AutoNAZAD" or call.data == "VseOsvita4AutoNAZAD":
        await ChangeToMainMenu(call.message.chat.id, messagecall)        
"""     elif call.data == "yes":
        c.execute("select * from action where id = 1")
        x = c.fetchall()
        if call.from_user.id in x[0][2]:
            toadd = list(x[0][1])
            toadd.append(call.from_user.id)
            todelete = list(x[0][2])
            todelete.remove(call.from_user.id)
            c.execute("update action set yes = %s where id = 1", (json.dumps(toadd),))
            c.execute("update action set no = %s where id = 1", (json.dumps(todelete),))
            conn.commit()
        elif call.from_user.id not in x[0][1]:
            toadd = list(x[0][1])
            toadd.append(call.from_user.id)
            c.execute("update action set yes = %s where id = 1", (json.dumps(toadd),))
            conn.commit()
    elif call.data == "no":
        c.execute("select * from action where id = 1")
        x = c.fetchall()
        if call.from_user.id in x[0][1]:
            toadd = list(x[0][2])
            toadd.append(call.from_user.id)
            todelete = list(x[0][1])
            todelete.remove(call.from_user.id)
            c.execute("update action set yes = %s where id = 1", (json.dumps(todelete),))
            c.execute("update action set no = %s where id = 1", (json.dumps(toadd),))
            conn.commit()
        elif call.from_user.id not in x[0][2]:
            toadd = list(x[0][2])
            toadd.append(call.from_user.id)
            c.execute("update action set no = %s where id = 1", (json.dumps(toadd),))
            conn.commit() """
@dp.callback_query_handler(lambda call: call.data, state="*") 
async def cancel_handler(call: types.CallbackQuery, state: FSMContext):
    if call.data == "stop":
            await ChangeToMainMenu(call.message.chat.id, call.message.message_id) 
            await state.finish()
    elif call.data == "OneStepAutoNaurokNAZAD":
        await bot.edit_message_text("Обычное получение ответов: Бот дает тебе ответы ты сам проходишь тест\nАвто-прохождение теста: Бот проходит за тебя тест(Дороже)", call.message.chat.id, call.message.message_id, reply_markup=vibornaurok)               
        await state.finish()
    elif call.data == "TwoStepAutoNaurokNAZAD":
        await bot.edit_message_text("Следующим сообщением отправьте ссылку на первый вопрос теста", call.message.chat.id, call.message.message_id, reply_markup=OneStepAutoNaurok)       
        await Form.OneStepAutoProxodNaUrok.set()
    elif call.data == "ThreeStepAutoNaurokNAZAD":
        async with state.proxy() as data:
            Questions = data["Questions"]
            await bot.edit_message_text(f"Укажите сколько неверных ответов должно быть(числом)\nВопросов в тесте: <b>{Questions['document']['questions']}</b>", call.message.chat.id, data["id"], reply_markup=TwoStepAutoNaurok, parse_mode="HTML")        
            await Form.TwoStepAutoProxodNaUrok.set()
    elif call.data == "FinallyStepAutoNaurokNAZAD":
        async with state.proxy() as data:
            Questions = data["Questions"]
            await bot.edit_message_text(f"Укажите сколько нужно времени потратить в целом на тест\nУказывать время с помощью приставок: s\\m\\h\nПример: 10m\ns - секунды, m - минуты\nМаксимум - 35 минут", call.message.chat.id, data["id"], reply_markup=ThreeStepAutoNaUrok)
            await Form.ThreeStepAutoProxodNaUrok.set()
    elif call.data == "VseOsvita1AutoNAZAD":
        await bot.edit_message_text("Обычное получение ответов: Бот дает тебе ответы ты сам проходишь тест\nАвто-прохождение теста: Бот проходит за тебя тест(Дороже)", call.message.chat.id, call.message.message_id, reply_markup=viborvseosvita)               
        await state.finish()
    elif call.data == "VseOsvita2AutoNAZAD":
        async with state.proxy() as data:
            await bot.edit_message_text("Следующим сообщением отправьте ссылку на вход теста", call.message.chat.id, data["id"], reply_markup=VseOsvita1AutoMarkup)
            await Form.VseOsvita1Auto.set()
    elif call.data == "VseOsvita3AutoNAZAD":
        async with state.proxy() as data:
            Init = data["Init"]
            await bot.edit_message_text(f"Укажите сколько неверных ответов должно быть(числом)\nВопросов в тесте: <b>{Init['execution']['count_quest']}</b>", call.message.chat.id, data["id"], reply_markup=VseOsvita2AutoMarkup, parse_mode="HTML")        
            await Form.VseOsvita2Auto.set()
    elif call.data == "VseOsvita4AutoNAZAD":
        async with state.proxy() as data:
            await bot.edit_message_text(f"Укажите какое имя использовать при прохождении теста", call.message.chat.id, data["id"], reply_markup=VseOsvita3AutoMarkup)
            await Form.VseOsvita3Auto.set()
    elif call.data == "VseOsvita5AutoNAZAD":
        async with state.proxy() as data:
            await bot.edit_message_text(f"Укажите сколько нужно времени потратить в целом на тест\nУказывать время с помощью приставок: s\\m\\h\nПример: 10m\ns - секунды, m - минуты\nМаксимум - 35 минут", call.message.chat.id, data["id"], reply_markup=VseOsvita4AutoMarkup)
            await Form.VseOsvita4Auto.set()
@dp.message_handler(state=Form.promocode)
async def promocode(message:type, state:FSMContext):
    try:
        await bot.delete_message(message.chat.id, message.message_id)
        c.execute("select * from promo where id = %s", (message.text.lower(),))
        x = c.fetchone()
        if x == None or message.from_user.id in list(x[2]):
            async with state.proxy() as data:
                await VozvratToMenu("Промокод не верный или был уже использован!", message.chat.id, data["id"], state)
        else:
            if x[3] == None:
                used = list(x[2])
                used.append(message.from_user.id)
                c.execute("update promo set used = %s where id = %s", (json.dumps(used), message.text.lower()))
                balance = getbalance(message.from_user.id)+x[1]
                c.execute("update users set balance = %s where id = %s", (balance,message.from_user.id))
                conn.commit()
                async with state.proxy() as data:
                    await VozvratToMenu(f"Промокод успешно пополнил ваш баланс на {x[1]} грн", message.chat.id, data["id"], state)
            else:
                used = list(x[2])
                used.append(message.from_user.id)
                c.execute("update promo set used = %s where id = %s", (json.dumps(used), message.text.lower()))
                c.execute("update promo set count = %s where id = %s", (x[3]-1, message.text.lower()))
                balance = getbalance(message.from_user.id)+x[1]
                c.execute("update users set balance = %s where id = %s", (balance,message.from_user.id))
                conn.commit()
                async with state.proxy() as data:
                    await VozvratToMenu(f"Промокод успешно пополнил ваш баланс на {x[1]} грн", message.chat.id, data["id"], state)
                c.execute("select * from promo where id = %s", (message.text.lower(),))
                x = c.fetchone()
                if x[3] == 0:
                    c.execute("delete from promo where id = %s", (message.text.lower(),))
                    conn.commit()
                    await bot.send_message(620038501, f"Промокод {x[0]} завершил свой цикл жизни!")
    except:
        await state.finish()

@dp.message_handler(state=Form.oplata)
async def oplata(message:type, state: FSMContext):
    try:
        async with aiohttp.ClientSession() as ses:
            px = await ses.post("https://bitobmen.pro/api/code-sum/", data={"code": message.text})
            if px.status == 200:
                activate = await ses.post("https://bitobmen.pro/api/code-buy/", data={"code": message.text, "email": "m3sckt@gmail.com", "instant": "False"})
                if activate.status == 200:
                    pxJSON = await px.json()
                    sum = pxJSON["sum"]
                    AddLogs(f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>({message.from_user.id}) успешно произвел оплату в {sum} грн")
                    balance = getbalance(message.from_user.id)
                    toadd = list(pxJSON["sum"])
                    toadd.remove(toadd[-3])
                    toadd.remove(toadd[-1])
                    toadd.remove(toadd[-1])
                    balance+=int(''.join(toadd))
                    setbalance(message.from_user.id, balance)
                    await bot.delete_message(message.chat.id, message.message_id)
                    async with state.proxy() as data:
                        await VozvratToMenu(f"Баланс успешно пополнен на {''.join(toadd)} грн!", message.chat.id, data["id"], state)
                    InsertAllBalance(message.from_user.id, int(''.join(toadd)))
                    man = getman(message.from_user.id)
                    if man[5] == 30 and man[4] != None:
                        balancereferer = getbalance(man[4])
                        setbalance(man[4], balancereferer+5)
                        minusallbalance(message.from_user.id)
                        try:
                            await bot.send_message(man[4], "Реферальная система пополнила ваш баланс на 5 грн!")
                        except:
                            pass
                    elif man[5] > 30 and man[4] != None:
                        toaddref = 0
                        balancereferer = getbalance(man[4])
                        for i in range(0,int(man[5]/30)):
                            toaddref+=5
                            minusallbalance(message.from_user.id)
                        setbalance(man[4], balancereferer+toaddref)
                        try:
                            await bot.send_message(man[4], f"Реферальная система пополнила ваш баланс на {toaddref} грн!")
                        except: 
                            pass
                # px["sum"] чтобы узнать сумму на которую платежку
                elif activate.status == 400:
                    await bot.delete_message(message.chat.id, message.message_id)
                    async with state.proxy() as data:
                        await bot.edit_message_text("Введите код еще раз", message.chat.id, data["id"])
            elif px.status == 404:
                await bot.delete_message(message.chat.id, message.message_id)
                async with state.proxy() as data:
                    await VozvratToMenu("Код не найден! Либо не верный!", message.chat.id, data["id"], state)
    except: 
        await state.finish()


@dp.message_handler(state=Form.vseosvita)
async def vseosvita(message: types.Message, state: FSMContext):
    try:
        balance = getbalance(message.from_user.id)
        if balance == None or balance < Config["PriceVseOsvita"]:
            await bot.delete_message(message.chat.id, message.message_id)
            async with state.proxy() as data:
                await VozvratToMenu("Недостаточно средств! Пополните баланс!", message.chat.id, data["id"], state)
        else:        
            async with state.proxy() as data:
                await bot.edit_message_text("Начинаю получать ответы с теста.....", message.chat.id, data["id"])
            AddLogs(f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>({message.from_user.id}) начал решение теста ВсеОсвиты! (списания средств-)(Текущий баланс: {getbalance(message.from_user.id)})")
            html = await hackvseo.HackVseo(message.text)
            if html == "NeVseOsvita":
                await bot.delete_message(message.chat.id, message.message_id)
                async with state.proxy() as data:
                    try:
                        await bot.edit_message_text("Не похоже на ВсеОсвиту\nПример: https://vseosvita.ua/test/start/dfg621",message.chat.id,data["id"], reply_markup=stop)
                    except:
                        return
            elif html == "TestEnded":
                await bot.delete_message(message.chat.id, message.message_id)
                async with state.proxy() as data:
                    await VozvratToMenu("Тест закончили", message.chat.id, data["id"], state)
            else:
                idfile = randint(1000, 9999)
                f = open(f"{idfile}.html", "w+", encoding='utf-8')
                f.write(html["HTMLANSWER"])
                f.close()
                await bot.send_document(message.chat.id, open(f"{idfile}.html", "rb"))
                os.remove(f"{idfile}.html")
                setbalance(message.from_user.id, balance-Config["PriceVseOsvita"])
                AddLogs(f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>({message.from_user.id}) получил ответы с теста ВсеОсвиты! (списание средств+ )(Текущий баланс: {getbalance(message.from_user.id)})")
                async with state.proxy() as data:
                    await ChangeToMainMenu(message.chat.id, data["id"])   
                await state.finish()             
    except: 
        await state.finish()
            

@dp.message_handler(state=Form.naurok)
async def naurok(message: types.Message, state: FSMContext):
    try:
        balance = getbalance(message.from_user.id) 
        if balance == None or balance < Config["PriceNaurok"]:
            await bot.delete_message(message.chat.id, message.message_id)
            async with state.proxy() as data:
                await VozvratToMenu("Недостаточно средств! Пополните баланс!", message.chat.id, data["id"], state)
        else:
            async with state.proxy() as data:
                try:
                    await bot.edit_message_text("Начинаю получать ответы с теста...\nЭто может занять несколько минут в зависимости от теста", message.chat.id, data["id"])
                except aiogram.utils.exceptions.MessageNotModified:
                    return
            sesid = await hacknaurok.GetSessiondId(message.text)
            if sesid == "NotNaurok":
                await bot.delete_message(message.chat.id, message.message_id)
                async with state.proxy() as data:
                    await bot.edit_message_text("Не похоже на НаУрок\nПример: https://naurok.com.ua/test/testing/160ff965-d7dd-4c04-9689-c71933784dff",message.chat.id, data["id"], reply_markup=stop)
            elif sesid == "TestEnded":
                await bot.delete_message(message.chat.id, message.message_id)
                async with state.proxy() as data:
                    await VozvratToMenu("Тест закончен", message.chat.id, data["id"], state)
            elif sesid == "WrongURL":
                await bot.send_message(message.chat.id, "Чаво? Обратись к админам")
                await state.finish()
            else:
                AddLogs(f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>({message.from_user.id}) начал решение теста НаУрок! (списания средств-)(Текущий баланс: {getbalance(message.from_user.id)})")
                quest = await hacknaurok.GetQuestions(sesid)
                if quest == "Up80":
                    async with state.proxy() as data:
                        await VozvratToMenu("Больше ста вопросов", message.chat.id, data["id"], state)
                    return
                itog = await hacknaurok.itog(quest)
                idfile = randint(1000, 9999)
                f = open(f"{idfile}.html", "w+", encoding='utf-8')
                f.write(itog)
                f.close()
                await bot.send_document(message.chat.id, open(f"{idfile}.html", "rb"))
                os.remove(f"{idfile}.html")
                setbalance(message.from_user.id, balance-Config["PriceNaurok"])  
                AddLogs(f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>({message.from_user.id}) получил ответы с теста Наурок! (списания средств+)(Текущий баланс: {getbalance(message.from_user.id)})")  
                async with state.proxy() as data:
                    await ChangeToMainMenu(message.chat.id, data["id"])            
                await state.finish()    
    except:
        await state.finish()
            
@dp.message_handler(state=Form.OneStepAutoProxodNaUrok)
async def OneStepAutoProxodNaUrok(message: types.Message, state: FSMContext):
        balance = getbalance(message.from_user.id) 
        if balance == None or balance < Config["PriceAutoNaurok"]:
            await bot.delete_message(message.chat.id, message.message_id)
            async with state.proxy() as data:
                await VozvratToMenu("Недостаточно средств! Пополните баланс!", message.chat.id, data["id"], state)
        else:
            await bot.delete_message(message.chat.id, message.message_id)
            SesId = await hacknaurok.GetSessiondId(message.text)
            if SesId == "NotNaurok":
                try:
                    async with state.proxy() as data:
                        await bot.edit_message_text("Не похоже на Наурок!\nПример: https://naurok.com.ua/test/testing/160ff965-d7dd-4c04-9689-c71933784dff", message.chat.id, data["id"], reply_markup=OneStepAutoNaurok)
                    return
                except aiogram.utils.exceptions.MessageNotModified:
                    return
            elif SesId == "TestEnded":
                async with state.proxy() as data:
                    await VozvratToMenu("Тест закончен!", message.chat.id, data["id"], state)
                return
            elif SesId == "WrongURL":
                async with state.proxy() as data:
                    bot.edit_message_text("Произошла непредвиденная ошибка! Обратись к администраторам", message.chat.id, data["id"])
                    await state.finish()
                return
            Questions = await hacknaurok.GetQuestions(SesId)
            if Questions == "Up80":
                async with state.proxy() as data:
                    await VozvratToMenu("Больше ста вопросов", message.chat.id, data["id"], state)
                return
            async with state.proxy() as data:
                data["SesId"] = SesId
                data["Questions"] = Questions
                data["Url"] = message.text
                await bot.edit_message_text(f"Укажите сколько неверных ответов должно быть(числом)\nВопросов в тесте: <b>{Questions['document']['questions']}</b>", message.chat.id, data["id"], reply_markup=TwoStepAutoNaurok, parse_mode="HTML")
                await Form.TwoStepAutoProxodNaUrok.set()
@dp.message_handler(state=Form.TwoStepAutoProxodNaUrok)
async def TwoStepAutoProxodNaUrok(message: types.message, state: FSMContext):
        await bot.delete_message(message.chat.id, message.message_id)
        try:
            async with state.proxy() as data:
                Questions = data["Questions"]
                MessageId = data["id"]
            if int(message.text) >= int(Questions["document"]["questions"]):
                try:
                    await bot.edit_message_text(f"Неправильных ответов больше чем вопросов!\nВопросов в тесте: <b>{Questions['document']['questions']}</b>", message.chat.id, MessageId, parse_mode="HTML", reply_markup=TwoStepAutoNaurok)
                    return
                except aiogram.utils.exceptions.MessageNotModified:
                    return
            async with state.proxy() as data:
                data["WrongAnswers"] = int(message.text)
                await bot.edit_message_text(f"Укажите сколько нужно времени потратить в целом на тест\nУказывать время с помощью приставок: s\\m\\h\nПример: 10m\ns - секунды, m - минуты\nМаксимум - 35 минут", message.chat.id, MessageId, reply_markup=ThreeStepAutoNaUrok)
                await Form.ThreeStepAutoProxodNaUrok.set()
        except ValueError:
            try:
                await bot.edit_message_text(f"<b>ЧИСЛОООМ!</b>\nКхм. . .\nУкажите сколько неверных ответов должно быть(<b>ЧИСЛОМ</b>)\nВопросов в тесте: <b>{Questions['document']['questions']}</b>", message.chat.id, MessageId, reply_markup=TwoStepAutoNaurok, parse_mode="HTML")
            except aiogram.utils.exceptions.MessageNotModified:
                return

@dp.message_handler(state=Form.ThreeStepAutoProxodNaUrok)
async def ThreeStepAutoProxodNaUrok(message: types.message, state: FSMContext):
        await bot.delete_message(message.chat.id, message.message_id)
        async with state.proxy() as data:
            MessageId = data["id"]
            Questions = data["Questions"]
        time = times(message.text)
        try:
            if time == None:
                await bot.edit_message_text(f"Что-то указано неверно!\nПример: 10m\ns - секунды, m - минуты\nМаксимум - 35 минут", message.chat.id, MessageId, reply_markup=ThreeStepAutoNaUrok)
                return
            elif time > 2220:
                await bot.edit_message_text(f"Пример: 10m\ns - секунды, m - минуты\nМаксимум - 35 минут", message.chat.id, MessageId, reply_markup=ThreeStepAutoNaUrok)
                return
            elif datetime.now()+timedelta(seconds=time+180) > datetime.fromtimestamp(Questions["session"]["start_at"])+timedelta(minutes=Questions["settings"]["duration"]) and Questions["settings"]["show_timer"] == 1:
                await bot.edit_message_text(f"Времени не хватит! Попробуй уменьшить время!\nПожалуйста берите в учет также таймер Наурока!", message.chat.id, MessageId, reply_markup=ThreeStepAutoNaUrok)
                return
        except aiogram.utils.exceptions.MessageNotModified:
            return
        async with state.proxy() as data:
            data["time"] = time
            data["CorrectTime"] = message.text
            await bot.edit_message_text(f"Это будет последний вопрос перед тем как начать прохождение теста!\nПолучить ответы в виде файлика?\nПросто ответьте <b>Да</b> или <b>Нет</b>", message.chat.id, MessageId, reply_markup=FinallyStepAutoNaUrok, parse_mode="HTML") 
            await Form.FinallyStepAutoProxodNaUrok.set()
@dp.message_handler(state=Form.FinallyStepAutoProxodNaUrok)
async def FinallyStepAutoProxodNaUrok(message: types.message, state: FSMContext):
        await bot.delete_message(message.chat.id, message.message_id)
        async with state.proxy() as data:
            MessageId = data["id"]
            Questions = data["Questions"]
            time = data["time"]
            Wrong = data["WrongAnswers"]
            Url = data["Url"]
        if message.text.lower() == "да":
            GetAnswers = True
        elif message.text.lower() == "нет":
            GetAnswers = False
        else:
            return
        await VozvratToMenu("Отлично! Приступаю к решению теста! Я оповещу когда я пройду тест", message.chat.id, MessageId)
        balance = getbalance(message.chat.id)
        setbalance(message.chat.id,balance-Config["PriceAutoNaurok"])
        AddLogs(f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>({message.from_user.id}) начал автоматически проходить тест НаУрок!")
        async with state.proxy() as data:
            text = f"Тест успешно выполнен!\nНеверных ответов - {Wrong}\nВремя - {data['CorrectTime']}"
        await state.finish()
        TrueAnsw = await autonaurok.GetTrueAnswers(Url, Wrong, GetAnswers)
        if GetAnswers == True:
            idfile = randint(1000, 9999)
            f = open(f"{idfile}.html", "w+", encoding='utf-8')
            f.write(TrueAnsw[3])
            f.close()
            await bot.send_document(message.chat.id, open(f"{idfile}.html", "rb"))
            os.remove(f"{idfile}.html")
        await autonaurok.avtoproxod(TrueAnsw, time)
        await bot.send_message(message.chat.id, text)
        AddLogs(f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>({message.from_user.id}) прошел автоматически тест НаУрок!")




@dp.message_handler(state=Form.VseOsvita1Auto)
async def VseOsvita1Auto(message: types.message, state: FSMContext):
    balance = getbalance(message.from_user.id) 
    if balance == None or balance < Config["PriceAutoVseOsvita"]:
        await bot.delete_message(message.chat.id, message.message_id)
        async with state.proxy() as data:
            await VozvratToMenu("Недостаточно средств! Пополните баланс!", message.chat.id, data["id"], state)
    else:
        await bot.delete_message(message.chat.id, message.message_id)
        async with state.proxy() as data:
            await bot.edit_message_text("Ожидайте. . .", message.chat.id, data["id"])
        Init = await hackvseo.HackVseo(message.text, CheckTest=True)
        if Init == "NeVseOsvita":
            try:
                async with state.proxy() as data:
                    await bot.edit_message_text("Не похоже на ВсеОсвиту!\nПример: https://vseosvita.ua/test/start/mef824", message.chat.id, data["id"], reply_markup=VseOsvita1AutoMarkup)
                    return
            except aiogram.utils.exceptions.MessageNotModified:
                    return
        elif Init == "TestEnded":
            async with state.proxy() as data:
                await VozvratToMenu("Тест закончен!", message.chat.id, data["id"], state)
                return
        async with state.proxy() as data:
            data["Url"] = message.text  
            data["Init"] = Init["payload"]
            await bot.edit_message_text(f"Укажите сколько неверных ответов должно быть(числом)\nВопросов в тесте: {Init['payload']['execution']['count_quest']}", message.chat.id, data["id"], reply_markup=VseOsvita2AutoMarkup)
            await Form.VseOsvita2Auto.set()
@dp.message_handler(state=Form.VseOsvita2Auto)
async def VseOsvita2Auto(message: types.message, state: FSMContext):
        await bot.delete_message(message.chat.id, message.message_id)
        try:
            async with state.proxy() as data:
                Init = data["Init"]
                MessageId = data["id"]
            if int(message.text) >= int(Init['execution']['count_quest']):
                try:
                    await bot.edit_message_text(f"Неправильных ответов больше чем вопросов!\nВопросов в тесте: <b>{Init['execution']['count_quest']}</b>", message.chat.id, MessageId, parse_mode="HTML", reply_markup=VseOsvita2AutoMarkup)
                    return
                except aiogram.utils.exceptions.MessageNotModified:
                    return
            async with state.proxy() as data:
                data["WrongAnswers"] = int(message.text)
                await bot.edit_message_text(f"Укажите какое имя использовать при прохождении теста", message.chat.id, MessageId, reply_markup=VseOsvita3AutoMarkup)
                await Form.VseOsvita3Auto.set()
        except ValueError:
            try:
                await bot.edit_message_text(f"<b>ЧИСЛОООМ!</b>\nКхм. . .\nУкажите сколько неверных ответов должно быть(<b>ЧИСЛОМ</b>)\nВопросов в тесте: <b>{Init['execution']['count_quest']}</b>", message.chat.id, MessageId, reply_markup=VseOsvita2AutoMarkup, parse_mode="HTML")
            except aiogram.utils.exceptions.MessageNotModified:
                return

@dp.message_handler(state=Form.VseOsvita3Auto)
async def VseOsvita4Auto(message: types.message, state: FSMContext):
    async with state.proxy() as data:
            await bot.delete_message(message.chat.id, message.message_id)
            MessageId = data["id"]
            data["Name"] = str(message.text)
            await bot.edit_message_text(f"Укажите сколько нужно времени потратить в целом на тест\nУказывать время с помощью приставок: s\\m\\h\nПример: 10m\ns - секунды, m - минуты\nМаксимум - 35 минут", message.chat.id, MessageId, reply_markup=VseOsvita4AutoMarkup)
            await Form.VseOsvita4Auto.set()
@dp.message_handler(state=Form.VseOsvita4Auto)
async def VseOsvita4Auto(message: types.message, state: FSMContext):
        await bot.delete_message(message.chat.id, message.message_id)
        async with state.proxy() as data:
            MessageId = data["id"]
            Init = data["Init"]
        time = times(message.text)
        try:
            if time == None:
                await bot.edit_message_text(f"Что-то указано неверно!\nПример: 10m\ns - секунды, m - минуты\nМаксимум - 35 минут", message.chat.id, MessageId, reply_markup=VseOsvita4AutoMarkup)
                return
            elif time > 2220:
                await bot.edit_message_text(f"Пример: 10m\ns - секунды, m - минуты\nМаксимум - 35 минут", message.chat.id, MessageId, reply_markup=VseOsvita4AutoMarkup)
                return
            elif timedelta(seconds=time+60) > datetime.fromtimestamp(Init["execution"]["time_end"])-datetime.fromtimestamp(Init["execution"]["time_start"]):
                await bot.edit_message_text(f"Времени не хватит! Попробуй уменьшить время!\nПожалуйста берите в учет также таймер ВсеОсвиты!", message.chat.id, MessageId, reply_markup=VseOsvita4AutoMarkup)
                return
        except aiogram.utils.exceptions.MessageNotModified:
            return
        async with state.proxy() as data:
            data["time"] = time
            data["CorrectTime"] = message.text
            await bot.edit_message_text(f"Это будет последний вопрос перед тем как начать прохождение теста!\nПолучить ответы в виде файлика?\nПросто ответьте <b>Да</b> или <b>Нет</b>", message.chat.id, MessageId, reply_markup=VseOsvita5AutoMarkup, parse_mode="HTML") 
            await Form.VseOsvita5Auto.set()
@dp.message_handler(state=Form.VseOsvita5Auto)
async def VseOsvita5Auto(message: types.message, state: FSMContext):
        await bot.delete_message(message.chat.id, message.message_id)
        async with state.proxy() as data:
            MessageId = data["id"]
            Init = data["Init"]
            time = data["time"]
            Wrong = data["WrongAnswers"]
            Url = data["Url"]
            Name = data["Name"]
        if message.text.lower() == "да":
            GetAnswers = True
        elif message.text.lower() == "нет":
            GetAnswers = False
        else:
            return
        await VozvratToMenu("Отлично! Приступаю к решению теста! Я оповещу когда я пройду тест", message.chat.id, MessageId)
        balance = getbalance(message.chat.id)
        setbalance(message.chat.id,balance-Config["PriceAutoVseOsvita"])
        AddLogs(f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>({message.from_user.id}) начал автоматически проходить тест ВсеОсвиты!")
        async with state.proxy() as data:
            text = f"Тест успешно выполнен!\nНеверных ответов - {Wrong}\nВремя - {data['CorrectTime']}"
        await state.finish()
        HtmlAnswer = await hackvseo.HackVseo(Url)
        if GetAnswers == True:
            idfile = randint(1000, 9999)
            f = open(f"{idfile}.html", "w+", encoding='utf-8')
            f.write(HtmlAnswer["HTMLANSWER"])
            f.close()
            await bot.send_document(message.chat.id, open(f"{idfile}.html", "rb"))
        await autovseosvita.autovseo(f"{idfile}.html", Name, Init["config"]["code"], Wrong, time)
        os.remove(f"{idfile}.html")
        await bot.send_message(message.chat.id, text)
        AddLogs(f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>({message.from_user.id}) прошел автоматически тест Всеосвиты!")

