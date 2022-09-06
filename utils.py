import psycopg2,asyncio,dip,logging,pytz,re,json
from datetime import datetime

Config = json.loads(open("configuration.json", "r", encoding="utf-8").read())

def dbConn():
    connect = psycopg2.connect() # коннект к базе данных
    return connect 
conn = dbConn()
c = conn.cursor()
    
timezone = pytz.timezone("Europe/Kiev")


def insertuser(id: int, firstname: str, username=None):
    global conn,c
    try:
        c.execute("insert into users (id, username, firstname) values (%s, %s, %s) on conflict (id) do update set username = %s, firstname = %s", (id, username, firstname,username,firstname))
        conn.commit()
    except:
        conn = dbConn()
        c = conn.cursor()
        logging.info("[DEF] Cursor reload!")

def GetAllMan():
    c.execute("select * from users")
    x = c.fetchall()
    return x
def DellMan(id: int):  
    c.execute("delete from users where id = %s", (id,))
    conn.commit()


def getbalance(id: int):
    c.execute("select * from users where id = %s", (id,))
    x = c.fetchone()
    return x[3] 
def getman(id: int):
    c.execute("select * from users where id = %s", (id,))
    x = c.fetchone()
    return x  
def setbalance(id: int, balance: int):
    c.execute("update users set balance = %s where id = %s", (balance, id))
    conn.commit()
def GetEnabled():
    c.execute("select * from bot")
    x = c.fetchall()
    return x[0][0]
def SetTrue():
    c.execute("update bot set enabled = true where enabled = false")
    conn.commit()
def SetFalse():
    c.execute("update bot set enabled = false where enabled = true")
    conn.commit()

def addviruchka(vir: int):
    c.execute("insert into viruchka (viruchka) values (%s)", (vir,))
    conn.commit()
def getviruchka():
    c.execute("select * from viruchka")
    x = c.fetchall()
    return x
def dellviruchka():
    c.execute("delete from viruchka")
    conn.commit()
async def ChangeToMainMenu(chatid: int, messageid: int):
    balance = getbalance(chatid)
    await dip.bot.edit_message_text(Config["LastChange"], chatid,messageid, parse_mode="HTML", reply_markup=MainMenu) 
async def VozvratToMenu(text: str, chatid: int, messageid: int, state=False, time=0.2):
        if state != False:
            await state.finish()
            for i in range(1, 6):
                if i / 2:
                    await dip.bot.edit_message_text(f"{text}\nПереношу вас в меню .", chatid, messageid)
                    await asyncio.sleep(time)
                if i / 4:
                    await dip.bot.edit_message_text(f"{text}\nПереношу вас в меню . .", chatid, messageid)
                    await asyncio.sleep(time)
                if i / 6 :
                    await dip.bot.edit_message_text(f"{text}\nПереношу вас в меню . . .", chatid, messageid)
                    await asyncio.sleep(time)
            await ChangeToMainMenu(chatid,messageid)
        else:
            for i in range(1, 6):
                if i / 2:
                    await dip.bot.edit_message_text(f"{text}\nПереношу вас в меню .", chatid, messageid)
                    await asyncio.sleep(time)
                if i / 4:
                    await dip.bot.edit_message_text(f"{text}\nПереношу вас в меню . .", chatid, messageid)
                    await asyncio.sleep(time)
                if i / 6 :
                    await dip.bot.edit_message_text(f"{text}\nПереношу вас в меню . . .", chatid, messageid)
                    await asyncio.sleep(time)
            await ChangeToMainMenu(chatid,messageid)
def DelLogs():
    c.execute("delete from log")
    conn.commit()
def AddLogs(text: str):
    c.execute("insert into log (time,text) values (%s,%s)", (datetime.now(tz=timezone).now(),text))
    conn.commit()
def GetLogs():
    c.execute("select * from log")
    x = c.fetchall()
    return x


def times(str):
    try:
        number = re.findall("\d+",str)
        letter = [i for i in str if not i.isdigit()]
        if letter[0] == "s":
             return int(number[0])
        elif letter[0] == "m":
            return 60 * int(number[0])
        elif letter[0] == "h":
            return 3600 * int(number[0])
        else:
            return None    
    except:
        return None

def InsertRef(id:int, firstname: str, RefId: int, username=None):
    c.execute("insert into users (id, username, firstname, refer) values (%s, %s, %s, %s)", (id, username,firstname,RefId))
    conn.commit()

def InsertAllBalance(id: int, sum: int):
    c.execute("select * from users where id = %s", (id,))
    x = c.fetchone()
    c.execute("update users set all_balance = %s where id = %s", (sum+x[5], id))
    conn.commit()

def minusallbalance(id: int):
    c.execute("select * from users where id = %s", (id,))
    x = c.fetchone()
    c.execute("update users set all_balance = %s where id = %s", (x[5]-30, id))
    conn.commit()
def CheckRefers(id: int):
    c.execute("select * from users where refer = %s", (id,))
    x = c.fetchall()
    return x



from inline_buttons import MainMenu