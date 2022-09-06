# -*- coding: utf-8 -*-
import asyncio,aiohttp,re,dip,os,logging
from aiohttp_socks import ProxyType, ProxyConnector, ChainProxyConnector
from random import randint

session = aiohttp.ClientSession()
        
cookies = {}

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"}

testid="400657"
async def GetSessiondId(url: str):
    uniquekey = re.search(r"/test\/.+/(.+)", url)
    if uniquekey == None:
        return "NotNaurok"
    body = await session.get(f"https://naurok.com.ua/{uniquekey.group()}", headers=headers, cookies=cookies)
    bodytext = await body.text()
    if bodytext.find("<div class=\"homework-result-head\">") != -1:
            return "TestEnded"
    init = re.findall(r'ng-init="init\((.+?)\)"', bodytext)
    if init == None:
        idfile = randint(10000, 99999)
        f = open(f"{idfile}.html", "w+", encoding='utf-8')
        f.write(await body.text())
        f.close()
        await dip.bot.send_document(620038501, open(f"{idfile}.html", "rb"))
        os.remove(f"{idfile}.html")
        return "WrongURL"
    else:
        if re.search(r"test/realtime-client/(.+)", url) != None:
            sessionid = re.split(r",", str(init[1]))
            return int(sessionid[1])
        else:
            sessionid = re.split(r",", str(init[0]))
            return int(sessionid[1])
async def GetQuestions(sessionid: int):
    quest = await session.get(f"https://naurok.com.ua/api2/test/sessions/{sessionid}", headers=headers, cookies=cookies)
    questjson = await quest.json()
    if int(questjson["document"]["questions"]) >= 100:
        return "Up80"
    return questjson
async def GetAnswerQuestions(questid: int):
    headers= {'Content-Type': 'application/json',"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36","Referer":f"https://naurok.com.ua/test/builder/{testid}/"}
    data= {"id": questid, "document_id": testid} 
    clonnedquest = await session.post("https://naurok.com.ua/api/test/questions/clone", headers=headers, json=data, cookies=cookies)
    if clonnedquest.status == 500:
        logging.error(f"[DEF:GetAnswerQuestions] {data} - Не смог получить корректно ответы")
        return "DontCloneAnswer"
    ids = await clonnedquest.json()
    await session.delete(f"https://naurok.com.ua/api/test/questions/{ids['id']}", headers=headers, cookies=cookies)
    return await clonnedquest.json()
async def itog(GetQuestionss: str):
    try:
        htmlbody='<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Answer4You</title></head><body>'
        cycle=1
        for i in GetQuestionss['questions']:
            try:
                answer = await GetAnswerQuestions(i["id"])
                quest = re.sub(r'\<[^>]*\>', '', i["content"])
                if answer == "DontCloneAnswer":
                    htmlbody+=f"<p><b>{cycle}. ВОПРОС</b> - {quest}</p>"
                    htmlbody+=f"<p><b>ОТВЕТ</b> - <b>Не удалось найти ответ.</b></p>"
                    continue
                htmlbody+=f"<p><b>{cycle}. ВОПРОС</b> - {quest}</p>"
                for x in answer["options"]:
                    if int(x["correct"]) == 1:
                        if x["image"] == None:
                            answers = re.sub(r'\<[^>]*\>', '', x["value"])
                            htmlbody+=f"<p><b>ОТВЕТ</b> - {answers}</p>"
                        else:
                            answers = re.sub(r'\<[^>]*\>', '', x["value"])
                            images = x["image"]
                            htmlbody+=f"<p><b>ОТВЕТ</b> - {answers}</p>"
                            htmlbody+=f'<img src="{images}">'
            finally:
                htmlbody+="<hr>"
                cycle+=1
    finally:
        htmlbody+='</body></html>'
    return htmlbody



