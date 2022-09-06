# -*- coding: utf-8 -*-
import requests,asyncio
import re
import json

cookies = {}

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"}

ses = requests.Session()
testid="400657"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36"}
async def GetSessiondId(url: str): 
    uniquekey = re.search(r"test/testing/(.+)", url)
    if uniquekey == None:
        return "NotNaurok"
    body = requests.get(f"https://naurok.com.ua/{uniquekey.group()}", headers=headers, proxies=proxies, cookies=cfclearnance)
    if body.text.find("<div class=\"homework-result-head\">") != -1:
        return "TestEnded"
#    print(body.text)
    init = re.search(r'ng-init=\"init\((.+?)\)', body.text)
    if init == None:
        return "WrongURL"
    else:
        sessionid = re.split(r",", str(init.groups()[0]))
        return int(sessionid[1])


async def GetQuestions(sessionid: int):
    quest = requests.get(f"https://naurok.com.ua/api2/test/sessions/{sessionid}", headers=headers, proxies=proxies, cookies=cfclearnance)
    return quest.json()


async def GetAnswerQuestions(questid: int):
    headers= {'Content-Type': 'application/json',"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36","Referer":f"https://naurok.com.ua/test/builder/{testid}/"}
    data= {"id": questid, "document_id": testid}
    clonnedquest = requests.post("https://naurok.com.ua/api/test/questions/clone", headers=headers, json=data,cookies=cookies, proxies=proxies)
    ids = clonnedquest.json()["id"]
    requests.delete(f"https://naurok.com.ua/api/test/questions/{ids}", headers=headers,cookies=cookies, proxies=proxies)
    return clonnedquest.json()
    
async def itog(GetQuestions: str):
    questid = []
    itog = []
    for i in GetQuestions['questions']:
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

