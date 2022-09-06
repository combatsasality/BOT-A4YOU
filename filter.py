from aiogram import types
import asyncio
from aiogram.dispatcher.filters import BoundFilter
import dip,utils

class IsOwner(BoundFilter):
    key = "is_owner"
    def __init__(self, is_owner):
        self.is_owner = [620038501, 1132697406]
    async def check(self, message: types.Message):
        return message.from_user.id in self.is_owner

class InGroupTest(BoundFilter):
    key = "in_group_test"
    def __init__(self, in_group_test):
        self.in_group_test = -1001717970624
    async def check(self, message: types.Message):
        user = await dip.bot.get_chat_member(-1001717970624, message.from_user.id)
        if user != None and user.status != "left":
            return True
        else:
            await dip.bot.send_message(message.chat.id, "Для того чтобы пользоваться ботом вам нужно зайти в нашу группу!\nГруппа - @answers4youchannel")
            return False

class InGroupTestCall(BoundFilter):
    key = "in_group_test_call"
    def __init__(self, in_group_test_call):
        self.in_group_test_call = -1001717970624
    async def check(self, call: types.CallbackQuery):
        user = await dip.bot.get_chat_member(-1001717970624, call.from_user.id)
        if user != None and user.status != "left":
            return True
        else:    
            await dip.bot.send_message(call.message.chat.id, "Для того чтобы пользоваться ботом вам нужно зайти в нашу группу!\nГруппа - @answers4youchannel")
            return False

class BlackList(BoundFilter):
    key = "black_list"
    def __init__(self, black_list):
        pass
    async def check(self, call: types.CallbackQuery):
        utils.c.execute("select * from blacklist where id = %s", (call.from_user.id,))
        x = utils.c.fetchone()
        if x == None:
            return True
        else:
            if x[1] != None:
                await dip.bot.send_message(call.message.chat.id, f"Ты заблокирован в боте! Причина: {' '.join(x[1].split())}. Для разблокировки напиши - @A4YouHelp")
            else: 
                await dip.bot.send_message(call.message.chat.id, f"Ты заблокирован в боте! Для разблокировки напиши - @A4YouHelp")
            return False

WithoutTexData = ["HELP", "REFER", "stop", "NAZAD", "OneStepAutoNaurokNAZAD", "TwoStepAutoNaurokNAZAD", "ThreeStepAutoNaurokNAZAD", "FinallyStepAutoNaurokNAZAD", "VseOsvita1AutoNAZAD", "VseOsvita2AutoNAZAD", "VseOsvita3AutoNAZAD", "VseOsvita4AutoNAZAD"]
class Tex(BoundFilter):
    key = "tex"
    def __init__(self, tex):
        pass
    async def check(self, call: types.CallbackQuery):
        Enabled = utils.GetEnabled()
        if call.data in WithoutTexData:
            return False
        elif Enabled == False and call.from_user.id not in [620038501, 1132697406]:
            for i in range(1, 6):
                if i / 2:
                    await dip.bot.edit_message_text("Бот находится на тех обслуживании\nПереношу вас в меню .", call.from_user.id, call.message.message_id)
                    await asyncio.sleep(0.2)
                if i / 4:
                    await dip.bot.edit_message_text("Бот находится на тех обслуживании\nПереношу вас в меню . .", call.from_user.id, call.message.message_id)
                    await asyncio.sleep(0.2)
                if i / 6 :
                    await dip.bot.edit_message_text("Бот находится на тех обслуживании\nПереношу вас в меню . . .", call.from_user.id, call.message.message_id)
                    await asyncio.sleep(0.2)
            await utils.ChangeToMainMenu(call.from_user.id, call.message.message_id)
            return False
        else:
            return True