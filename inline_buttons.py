from dip import InlineKeyboardMarkup,InlineKeyboardButton,dp,types,bot,State, StatesGroup,Text,FSMContext,ReplyKeyboardMarkup,ReplyKeyboardRemove,KeyboardButton
import os,json,aiohttp,aiogram,datetime
from aiogram.types import LabeledPrice
from aiogram.types.message import ContentTypes
from hack import autovseosvita
from utils import ChangeToMainMenu, CheckRefers, getman,getbalance,setbalance,insertuser,VozvratToMenu,AddLogs,c,conn,times,InsertAllBalance,minusallbalance
from hack import autonaurok, hackvseo,hacknaurok
from random import randint
from datetime import datetime, timedelta


Config = json.loads(open("configuration.json", "r", encoding="utf-8").read())

PAYMENTSTOKEN = "535936410:LIVE:5589410392_8ceaceda-a958-4ce6-b32d-25d1f242a6b6"

MainMenu = InlineKeyboardMarkup()

AddBalance = InlineKeyboardButton("💳Пополнить баланс💳", callback_data="AddBalance")
VseOsvita = InlineKeyboardButton("📘ВсеОсвита📘", callback_data="VseOsvita")
NaUrok = InlineKeyboardButton("📙НаУрок📙", callback_data="Naurok")
FAQ = InlineKeyboardButton("❓ЧаВо❓", callback_data="FAQ")
HELP = InlineKeyboardButton("👺Помощь👺", callback_data="HELP")
REFER = InlineKeyboardButton("✉️Реферальная система✉️", callback_data="REFER")
MainMenu.row(NaUrok)

nazadhelp = InlineKeyboardMarkup().add(InlineKeyboardButton("Что ты получаешь при покупки теста ВсеОсвита", url="https://youtu.be/tLvm6FVEnH4")).add(InlineKeyboardButton("Что ты получаешь при покупки теста НаУрок", url="https://youtu.be/0x8TOjQzzLY")).add(InlineKeyboardButton("⬅️Назад",callback_data="NAZAD"))

nazad = InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️Назад", callback_data="NAZAD"))
#FAQMENU = InlineKeyboardMarkup().row(InlineKeyboardButton("ВсеОсвита", url="https://youtu.be/SIjLU-TO9po"), InlineKeyboardButton("НаУрок", url="https://youtu.be/PRRCbOOnsQY")).add(InlineKeyboardButton("⬅️Назад", callback_data="NAZAD"))

vseosvitahelp = InlineKeyboardButton("Помощь по ВсеОсвите", url="https://youtu.be/SIjLU-TO9po")
naurokhelp = InlineKeyboardButton("Помощь по НаУроку", url="https://youtu.be/wtrYyAuJ2Ck")
vvedkoda = InlineKeyboardMarkup().add(InlineKeyboardButton("Пополнить баланс", callback_data="Oplata")).row(InlineKeyboardButton("Ввести промокод", callback_data="PromoCode"),InlineKeyboardButton("Помощь в пополнении", url="https://telegra.ph/Popolnenie-balansa-v-Answer4You-08-11")).add(InlineKeyboardButton("⬅️Назад", callback_data="NAZAD"))
stop = InlineKeyboardMarkup().add(InlineKeyboardButton("⛔️CТОП⛔️", callback_data="stop"))


vibornaurok = InlineKeyboardMarkup().add(InlineKeyboardButton("Обычное получение ответов", callback_data="TypicalNaurok")).add(InlineKeyboardButton("⬅️Назад", callback_data="NAZAD"))

viborvseosvita = InlineKeyboardMarkup().add(InlineKeyboardButton("Обычное получение ответов", callback_data="TypicalVseOsvita")).add(InlineKeyboardButton("Авто-прохождение теста", callback_data="Zaglushka")).add(InlineKeyboardButton("⬅️Назад", callback_data="NAZAD"))

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
VseOsvita5AutoMarkup = InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️Назад", callback_data="VseOsvita5AutoNAZAD")).add(InlineKeyboardButton("⛔️CТОП⛔️", callback_data="stop"))

stopnaurok = InlineKeyboardMarkup().add(InlineKeyboardButton("Помощь по НаУроку", url="https://youtu.be/0x8TOjQzzLY")).add(InlineKeyboardButton("⛔️CТОП⛔️", callback_data="stop"))
stopvseosvita = InlineKeyboardMarkup().add(InlineKeyboardButton("Помощь по ВсеОсвите", url="https://youtu.be/tLvm6FVEnH4")).add(InlineKeyboardButton("⛔️CТОП⛔️", callback_data="stop"))

@dp.callback_query_handler(lambda call: call.data, black_list=True, tex=True)
async def callbackquery(call: types.CallbackQuery, state: FSMContext):
    insertuser(call.from_user.id, call.from_user.first_name, call.from_user.username)
    messagecall = call.message.message_id
    if call.data == "AddBalance": #Добавление балика
        await bot.edit_message_text("Промокод можно получить от администраторов бота\n❗️Возврат средств не осуществляется❗️",call.message.chat.id, messagecall, reply_markup=vvedkoda, parse_mode="MarkDownV2", disable_web_page_preview=True)
    elif call.data == "VseOsvita": #ВсеОсвита
        await bot.edit_message_text("Обычное получение ответов: Бот дает тебе ответы ты сам проходишь тест\nАвто-прохождение теста: Бот проходит за тебя тест(Дороже)",call.message.chat.id, messagecall, reply_markup=viborvseosvita)
    elif call.data == "AutoProxodVseOsvita": 
        x = await bot.edit_message_text("Следующим сообщением отправьте ссылку на вход теста", call.message.chat.id, messagecall, reply_markup=VseOsvita1AutoMarkup)
        await Form.VseOsvita1Auto.set()
        async with state.proxy() as data:
            data["id"] = x.message_id  
    elif call.data == "TypicalVseOsvita":
        await Form.vseosvita.set()
        await bot.edit_message_text("Следующим сообщением отправьте ссылку на вход теста", call.message.chat.id, messagecall, reply_markup=stopvseosvita, parse_mode="HTML")
        async with state.proxy() as data:
            data["id"] = messagecall
    elif call.data == "NaurokNotValid": #NAUROK
        await bot.edit_message_text("Обычное получение ответов: Бот дает тебе ответы ты сам проходишь тест", call.message.chat.id, messagecall, reply_markup=vibornaurok)       
    elif call.data == "AutoProxodNaurok": 
        x = await bot.edit_message_text("Следующим сообщением отправьте ссылку на первый вопрос теста", call.message.chat.id, messagecall, reply_markup=OneStepAutoNaurok)
        await Form.OneStepAutoProxodNaUrok.set()
        async with state.proxy() as data:
            data["id"] = x.message_id  
    elif call.data == "Naurok":
        await Form.naurok.set()
        await bot.edit_message_text("Следующим сообщением отправьте ссылку на первый вопрос теста", call.message.chat.id, messagecall, reply_markup=stopnaurok, parse_mode="HTML")
        async with state.proxy() as data:
            data["id"] = messagecall
    elif call.data == "Oplata":
        await Form.oplata.set()
        await bot.edit_message_text("Введите сумму на которую хотите пополнить баланс", call.message.chat.id,messagecall,reply_markup=stop)
        async with state.proxy() as data:
            data["id"] = messagecall
    elif call.data == "PromoCode":
        await Form.promocode.set()
        await bot.edit_message_text("Введите код который вы получили от администраторов", call.message.chat.id,messagecall,reply_markup=stop)
        async with state.proxy() as data:
            data["id"] = messagecall  
@dp.callback_query_handler(lambda call: call.data) #ЕСЛИ ДОБАЛВЯТЬ СЮДА НОВУЮ КНОПКУ ЕЕ ТАКЖЕ НАДО ДОБАВЛЯТЬ В МАССИВ WithoutTexData в filter
async def withouttex(call: types.CallbackQuery):
    insertuser(call.from_user.id, call.from_user.first_name, call.from_user.username)
    messagecall = call.message.message_id
    if call.data == "HELP":
        await bot.edit_message_text(chat_id=call.message.chat.id,  message_id=messagecall, text=Config["HelpMenu"], parse_mode="HTML", disable_web_page_preview=True, reply_markup=nazadhelp)
    elif call.data == "REFER":
        referrs = CheckRefers(call.from_user.id)
        if referrs == None:
            await bot.edit_message_text("Вот ваша персональна реферальная ссылка:\n"+ f"<code>https://t.me/answers4youbot?start={call.from_user.id}</code>\nУсловия реферальной системы: За каждого человека которого вы пригласили и он пополнил 30 грн, вы получаете - 5 грн\nНа данный момент у вас: 0 рефералов", call.message.chat.id,messagecall,reply_markup=nazad, parse_mode="HTML")
        else:
            await bot.edit_message_text("Вот ваша персональна реферальная ссылка:\n"+ f"<code>https://t.me/answers4youbot?start={call.from_user.id}</code>\n\nУсловия реферальной системы: За каждого человека которого вы пригласили и он пополнил 30 грн, вы получаете - 5 грн\n\nНа данный момент у вас: {len(referrs)} реферал/-а/-ов", call.message.chat.id,messagecall,reply_markup=nazad, parse_mode="HTML")
    elif call.data == "stop": #Стоп решения тестов
        await ChangeToMainMenu(call.message.chat.id, messagecall)
    elif call.data == "NAZAD": #Кнопка чтобы вернутся к главному меню
        await ChangeToMainMenu(call.message.chat.id, messagecall)
    elif call.data == "OneStepAutoNaurokNAZAD" or call.data == "TwoStepAutoNaurokNAZAD" or call.data == "ThreeStepAutoNaurokNAZAD" or call.data == "FinallyStepAutoNaurokNAZAD" or call.data == "VseOsvita1AutoNAZAD" or call.data == "VseOsvita2AutoNAZAD" or call.data == "VseOsvita3AutoNAZAD" or call.data == "VseOsvita4AutoNAZAD":
        await ChangeToMainMenu(call.message.chat.id, messagecall)

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
    await bot.delete_message(message.chat.id, message.message_id)
    async with state.proxy() as data:
        messageid = data["id"]
    try:
        if str(message.text).isdigit():
            await bot.edit_message_text("Снизу⬇️", message.chat.id, messageid)
            await bot.send_invoice(message.chat.id, f"Баланс", "Пополнение баланса", "str23", provider_token=PAYMENTSTOKEN, currency="UAH", prices=[LabeledPrice('Сумма', int(str(message.text)+"0"+"0"))], reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Оплатить", pay=True)))
            await state.finish()
        else:
            await bot.edit_message_text("Укажите сумму цифрой!", message.chat.id, messageid, reply_markup=nazad)
    except: 
        await state.finish()
@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def SUCCESSFUL(message: types.message):
    toadd = list(str(message.successful_payment.total_amount))
    toadd.remove(toadd[-1])
    toadd.remove(toadd[-1])
    toadd = int(''.join(toadd))
    balance = getbalance(message.from_user.id)
    setbalance(message.from_user.id, balance+toadd)
    AddLogs(f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>({message.from_user.id}) успешно произвел оплату в {toadd} грн")
    await bot.send_message(message.chat.id, Config["LastChange"], parse_mode="HTML", reply_markup=MainMenu)
    InsertAllBalance(message.from_user.id, toadd)
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
@dp.pre_checkout_query_handler(lambda query: True)
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True, error_message="Обратитесь к администраторам !")
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
        if message.text.lower() in ["да", "da", "yes"]:
            GetAnswers = True
        elif message.text.lower() in ["нет", "net", "no"]:
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
        idfile = randint(1000, 9999)
        f = open(f"{idfile}.html", "w+", encoding='utf-8')
        f.write(HtmlAnswer["HTMLANSWER"])
        f.close()
        if GetAnswers == True:
            await bot.send_document(message.chat.id, open(f"{idfile}.html", "rb"))
        await autovseosvita.autovseo(f"{idfile}.html", Name, Init["config"]["code"], Wrong, time)
        os.remove(f"{idfile}.html")
        await bot.send_message(message.chat.id, text)
        AddLogs(f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>({message.from_user.id}) прошел автоматически тест Всеосвиты!")

