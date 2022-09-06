# -*- coding: utf-8 -*-
import asyncio,aiohttp,re,os
from random import randint

cookies = {}

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"}

testid="400657"
async def GetSessiondId(url: str):
    async with aiohttp.ClientSession() as session:
        uniquekey = re.search(r"test/testing/(.+)", url)
        if uniquekey == None:
            return "NotNaurok"
        body = await session.get(f"https://naurok.com.ua/{uniquekey.group()}", headers=headers, cookies=cookies)
        bodytext = await body.text()
        if bodytext.find("<div class=\"homework-result-head\">") != -1:
                return "TestEnded"
        init = re.search(r'ng-init=\"init\((.+?)\)', bodytext)
        if init == None:
            return "WrongURL"
        else:
            sessionid = re.split(r",", str(init.groups()[0]))
            return int(sessionid[1])
async def GetQuestions(sessionid: int):
    async with aiohttp.ClientSession() as session:
        quest = await session.get(f"https://naurok.com.ua/api2/test/sessions/{sessionid}", headers=headers,cookies=cookies)
        return await quest.json()
async def GetAnswerQuestions(questid: int):
    async with aiohttp.ClientSession() as session:
        headers= {'Content-Type': 'application/json',"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36","Referer":f"https://naurok.com.ua/test/builder/{testid}/"}
        data= {"id": questid, "document_id": testid} 
        clonnedquest = await session.post("https://naurok.com.ua/api/test/questions/clone", headers=headers, json=data, cookies=cookies)
        ids = await clonnedquest.json()
        await session.delete(f"https://naurok.com.ua/api/test/questions/{ids['id']}", headers=headers, cookies=cookies)
        return await clonnedquest.json()
async def itog(GetQuestionss: str):
    questid = []
    itog = []
    for i in GetQuestionss['questions']:
        answer = await GetAnswerQuestions(i["id"])
        quest = re.sub(r'\<[^>]*\>', '', i["content"])
        itog.append(f"\nВОПРОС - {quest}")
        for x in answer["options"]:
            if int(x["correct"]) == 1:
                if x["image"] == None:
                    answers = re.sub(r'\<[^>]*\>', '', x["value"])
                    itog.append(f"ОТВЕТ - {answers}")
                else:
                    answers = re.sub(r'\<[^>]*\>', '', x["value"])
                    images = x["image"]
                    itog.append(f"ОТВЕТ - {answers}  {images}")
    return itog
questions = asyncio.run(GetQuestions(162484491))
p = asyncio.run(itog(questions))


for i in p:
    print(i)