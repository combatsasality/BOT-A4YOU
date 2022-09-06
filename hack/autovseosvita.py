# -*- coding: utf-8 -*-
from random import randint
from aiohttp_socks import ProxyType, ProxyConnector, ChainProxyConnector
from bs4 import BeautifulSoup, Tag
import html,asyncio,aiohttp,re

cookies = {}
cock = {}

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"}

useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"

answerarrfor4type = {"а": 0, "б": 1, "в": 2, "г": 3, "д": 4, "е": 5, "є": 6, "ж": 7, "з": 8, "и": 9, "і": 10, "к": 11, "л": 12, "м": 13, "н": 14, "о": 15, "п": 16, "р": 17, "с": 18, "т": 19, "у": 20, "ф": 21, "х": 22, "ц": 23, "ч": 24, "ш": 25}
headerswithxrequest = {
    "user-agent":useragent,
    "content-type": "application/json; charset=UTF-8",
    "x-requested-with":"XMLHttpRequest"
    }
headerswithxrequestandxwww = {
    "user-agent":useragent,
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "x-requested-with":"XMLHttpRequest"
    }
async def autovseo(namefile: str, NameStudy: str, code: str, skip=0, wait=0):
    async with aiohttp.ClientSession() as ses:
        soup = BeautifulSoup(open(namefile, "r", encoding="utf-8"), 'html.parser')
        await ses.post(f"https://vseosvita.ua/test/start/{code}", headers={"user-agent":useragent,"content-type": "application/x-www-form-urlencoded"}, cookies=cock)
        await ses.post(f"https://vseosvita.ua/test/go-settings?code={code}", headers={"user-agent":useragent,"content-type": "application/x-www-form-urlencoded"}, data={"TestDesignerSettings[full_name]": NameStudy}, cookies=cock)
        await ses.post("https://vseosvita.ua/ext/test-go-pupil/init?isAjax=1&isAjaxUrl=https://vseosvita.ua/test/go-olp", headers=headerswithxrequest, cookies=cock)
        await ses.post("https://vseosvita.ua/ext/test-go-pupil/set-time-start?isAjax=1&isAjaxUrl=https://vseosvita.ua/test/go-olp", headers=headerswithxrequest, cookies=cock)
        await ses.post("https://vseosvita.ua/ext/site/time?isAjax=1&isAjaxUrl=https://vseosvita.ua/test/go-olp", headers=dict(headerswithxrequest).update({"content-type": "application/json, text/javascript, */*; q=0.01"}), cookies=cock)
        ss = await ses.get("https://vseosvita.ua/ext/test-go-pupil/init", headers=headerswithxrequest, cookies=cock)
        payload = (await ss.json())["payload"]
        countquests = payload["execution"]["count_quest"]
        quests = payload["quests"]
        QuestToSkip = []
        if skip != 0:
            skipped = 0
            for i in range(0,countquests):
                QuestToSkip.append(1)
            while True: 
                random = randint(0,len(QuestToSkip)-1)
                if skipped == skip:
                    break
                else:
                    if QuestToSkip[random] == 0:
                        continue
                    else:
                        QuestToSkip[random] = 0
                        skipped+=1
        try:
            for i in range(0,countquests):
                print(i+1)
                try:
                        if skip != 0 and QuestToSkip[i] == 0:
                            await ses.get("https://vseosvita.ua/ext/test-go-pupil/get-next-quest?isAjax=1&isAjaxUrl=https%3A%2F%2Fvseosvita.ua%2Ftest%2Fgo-olp", headers=headerswithxrequestandxwww, cookies=cock)
                            continue
                        if quests[i]["quest_type"] == 1:
                            Answer = soup.find('div', {"data-qnum": i+1}).find("span", class_="v-correct-answer").findParent().select("ul > li > p > img")
                            if Answer == []: 
                                Answer = soup.find('div', {"data-qnum": i+1}).find("span", class_="v-correct-answer").findParent().select("ul > li > p")[0]
                            else:
                                Answer = Answer[0]["data-src"]
                            for x in range(0,len(quests[i]["answer_arr"])):
                                if isinstance(Answer, str) : sas = BeautifulSoup(quests[i]["answer_arr"][x], 'html.parser').p.img["src"]
                                else: sas = quests[i]["answer_arr"][x]
                                print(type(sas))
                                print(type(str(Answer)))
                                print(str(Answer))
                                print(str(sas) == str(Answer))
                                if str(Answer) == str(sas):
                                    response = await ses.post("https://vseosvita.ua/ext/test-go-pupil/save-user-answer?isAjaxUrl=https://vseosvita.ua/test/go-olp", headers=headerswithxrequestandxwww, cookies=cock, data={f"answers[{quests[i]['id']}][{x}]": x, "id_quest": quests[i]["id"]})
                                    break
                        elif quests[i]["quest_type"] == 2:
                            jsonsend = {}
                            Answer = soup.find('div', {"data-qnum": i+1}).find("span", class_="v-correct-answer").findParent().select("ul > li > p")
                            for x in range(0,len(Answer)):
                                if Answer[x].img != None:
                                    Answer[x] = Answer[x].img["data-src"]
                            IndexTrueAnswers = []
                            for x in range(0,len(quests[i]["answer_arr"])):
                                for p in Answer:
                                    if isinstance(p, str) and BeautifulSoup(quests[i]["answer_arr"][x], "html.parser").img != None: sas = BeautifulSoup(quests[i]["answer_arr"][x], "html.parser").img["src"]
                                    else : sas = quests[i]["answer_arr"][x]
                                    if str(p) == sas:
                                        IndexTrueAnswers.append(x)
                                        break
                            for x in IndexTrueAnswers:
                                jsonsend.update({f"answers[{quests[i]['id']}][{x}]": x})
                            jsonsend.update({"id_quest": quests[i]["id"]})
                            response = await ses.post("https://vseosvita.ua/ext/test-go-pupil/save-user-answer?isAjaxUrl=https://vseosvita.ua/test/go-olp", headers=headerswithxrequestandxwww, cookies=cock, data=jsonsend)
                        elif quests[i]["quest_type"] == 3:
                            Answer = soup.find('div', {"data-qnum": i+1}).find("span", class_="v-correct-answer").findParent().select("ul > li")
                            Temp = re.search(r";",str(Answer[0].get_text()))
                            if Temp != None:
                                Answer = re.search(r"(.+);",str(Answer[0].get_text())).group().split(";")[0]
                            else: 
                                Answer = Answer[0].get_text()
                            response = await ses.post("https://vseosvita.ua/ext/test-go-pupil/save-user-answer?isAjaxUrl=https://vseosvita.ua/test/go-olp", headers=headerswithxrequestandxwww, cookies=cock, data={f"answers[{quests[i]['id']}]": Answer, "id_quest": quests[i]['id']})
                        elif quests[i]["quest_type"] == 4:
                            jsonsend = {}
                            Answer = soup.find('div', {"data-qnum": i+1}).find("span", class_="v-correct-answer").findParent().select("ul > li > div:last-of-type > i")
                            for x in range(0,len(quests[i]["answer_arr"]["cross"])):
                                jsonsend.update({f"answers[{quests[i]['id']}][{x}]": answerarrfor4type[Answer[x].get_text().lower()]})
                            jsonsend.update({"id_quest": quests[i]['id']})
                            response = await ses.post("https://vseosvita.ua/ext/test-go-pupil/save-user-answer?isAjaxUrl=https://vseosvita.ua/test/go-olp", headers=headerswithxrequestandxwww, cookies=cock, data=jsonsend)
                        elif quests[i]["quest_type"] == 6:
                            jsonsend = {}
                            for x in quests[i]["answer_arr"]:
                                Answer = soup.select(f'div[data-qnum="{i+1}"] > div.v-test-questions-block > div.v-test-questions-title > div.i-block-question-shorten > p:first-of-type > span[data-key="{x}"] > strong:last-of-type > span')  
                                jsonsend.update({f"answers[{quests[i]['id']}][{x}]": Answer[0].get_text().replace("\n", "")})
                            jsonsend.update({"id_quest": quests[i]['id']})
                            response = await ses.post("https://vseosvita.ua/ext/test-go-pupil/save-user-answer?isAjaxUrl=https://vseosvita.ua/test/go-olp", headers=headerswithxrequestandxwww, cookies=cock, data=jsonsend)
                        elif quests[i]["quest_type"] == 7: #TUT ERROR
                            jsonsend = {}
                            for x in quests[i]["answer_arr"]:
                                Answer = soup.select(f'div[data-qnum="{i+1}"] > div:first-of-type > div:first-of-type > div.i-block-question-shorten > p > span[data-key="{x}"] > strong:last-of-type > u > span')
                                if Answer == []:
                                    Answer = soup.select(f'div[data-qnum="{i+1}"] > div:first-of-type > div:first-of-type > div.i-block-question-shorten > p > span[data-key="{x}"] > strong:last-of-type > span')
                                jsonsend.update({f"answers[{quests[i]['id']}][{x}]": Answer[0].get_text()})
                            jsonsend.update({"id_quest": quests[i]['id']})
                            response = await ses.post("https://vseosvita.ua/ext/test-go-pupil/save-user-answer?isAjaxUrl=https://vseosvita.ua/test/go-olp", headers=headerswithxrequestandxwww, cookies=cock, data=jsonsend)
                        elif quests[i]["quest_type"] == 8:
                            jsonsend = {}
                            Answer = soup.find('div', {"data-qnum": i+1}).find("span", class_="v-correct-answer").findParent().select("ul > li > p > span")
                            for x in range(1,len(quests[i]["answer_arr"])+1):
                                jsonsend.update({f"answers[{quests[i]['id']}][{x-1}]": int(Answer[x-1].get_text())-1})
                            jsonsend.update({"id_quest": quests[i]['id']})
                            response = await ses.post("https://vseosvita.ua/ext/test-go-pupil/save-user-answer?isAjaxUrl=https://vseosvita.ua/test/go-olp", headers=headerswithxrequestandxwww, cookies=cock, data=jsonsend)
                        elif quests[i]["quest_type"] == 9: 
                            Answer = soup.select(f'div[data-qnum="{i+1}"] > svg > g')
                            Answer.pop(-1)
                            Image = soup.select(f'div[data-qnum="{i+1}"] > svg > image')
                            (ИзначальноеЗначениеХ, ИзначальноеЗначениеУ) = int(Image[0]["width"]),int(Image[0]["height"])
                            (УвеличенноеЗначениеХ, УвеличенноеЗначениеУ) = int(quests[i]["answer_arr"][1]),int(quests[i]["answer_arr"][2])
                            if ИзначальноеЗначениеХ == УвеличенноеЗначениеХ and ИзначальноеЗначениеУ == УвеличенноеЗначениеУ:
                                XYAnswer = []
                                for x in Answer:
                                    XYAnswer.append(re.search("translate(.+, .+)", str(x["transform"])).group().replace("translate", "").replace("(", "").replace(")", "").split(","))
                                datasend = ""
                                for count,x in enumerate(XYAnswer):
                                    try:
                                        for p in range(0,len(x)):
                                            if Answer[count].ellipse == None:
                                                if p == 0: #weight 
                                                    datasend+=f"answers%5B{quests[i]['id']}%5D%5B{count}%5D%5B%5D={int(x[p])+5}&"
                                                elif p == 1: #height
                                                    datasend+=f"answers%5B{quests[i]['id']}%5D%5B{count}%5D%5B%5D={int(x[p])+5}&"
                                            else:
                                                if p == 0: #weight 
                                                    datasend+=f"answers%5B{quests[i]['id']}%5D%5B{count}%5D%5B%5D={int(x[p])+int(Answer[count].ellipse['rx'])}&"
                                                elif p == 1: #height
                                                    datasend+=f"answers%5B{quests[i]['id']}%5D%5B{count}%5D%5B%5D={int(x[p])+int(Answer[count].ellipse['ry'])}&"
                                    finally:
                                        datasend+=f"answers%5B{quests[i]['id']}%5D%5B{count}%5D%5B%5D=3&"
                                datasend+=f"files%5B{quests[i]['id']}%5D=&id_quest={quests[i]['id']}"
                                response = await ses.post("https://vseosvita.ua/ext/test-go-pupil/save-user-answer?isAjaxUrl=https://vseosvita.ua/test/go-olp", headers=headerswithxrequestandxwww, cookies=cock, data=datasend)
                            else:
                                datasend = ""
                                XYAnswer = []
                                for x in Answer:
                                    XYAnswer.append(re.search("translate(.+, .+)", str(x["transform"])).group().replace("translate", "").replace("(", "").replace(")", "").split(","))
                                XПроцент = ((УвеличенноеЗначениеХ-ИзначальноеЗначениеХ)/ИзначальноеЗначениеХ)*100 # Процентное увеличения числа
                                YПроцент = ((УвеличенноеЗначениеУ-ИзначальноеЗначениеУ)/ИзначальноеЗначениеУ)*100 # Процентное увеличения числа
                                for count,x in enumerate(XYAnswer):
                                    try:
                                        for p in range(0,len(x)):
                                            if Answer[count].ellipse == None:
                                                if p == 0:
                                                    XCoords = (int(x[p])/100*int(XПроцент))+int(x[p])+5 # формула прибавления процента x - число, i - процент
                                                    datasend+=f"answers%5B{quests[i]['id']}%5D%5B{count}%5D%5B%5D={int(XCoords)}&"
                                                elif p == 1:
                                                    YCoords = (int(x[p])/100*int(YПроцент))+int(x[p])+5 # формула прибавления процента x - число, i - процент
                                                    datasend+=f"answers%5B{quests[i]['id']}%5D%5B{count}%5D%5B%5D={int(YCoords)}&"
                                            else:
                                                if p == 0:
                                                    XCoords = (int(x[p])/100*int(XПроцент))+int(x[p]) # формула прибавления процента x - число, i - процент
                                                    datasend+=f"answers%5B{quests[i]['id']}%5D%5B{count}%5D%5B%5D={int(XCoords)+int(Answer[count].ellipse['rx'])}&"
                                                elif p == 1:
                                                    YCoords = (int(x[p])/100*int(YПроцент))+int(x[p]) # формула прибавления процента x - число, i - процент
                                                    datasend+=f"answers%5B{quests[i]['id']}%5D%5B{count}%5D%5B%5D={int(YCoords)+int(Answer[count].ellipse['ry'])}&"                                    
                                    finally:
                                        datasend+=f"answers%5B{quests[i]['id']}%5D%5B{count}%5D%5B%5D=3&"
                                datasend+=f"files%5B{quests[i]['id']}%5D=&id_quest={quests[i]['id']}"
                                response = await ses.post("https://vseosvita.ua/ext/test-go-pupil/save-user-answer?isAjaxUrl=https://vseosvita.ua/test/go-olp", headers=headerswithxrequestandxwww, cookies=cock, data=datasend)
                finally:
                    if wait != 0:
                        await asyncio.sleep(wait/countquests)
        finally:
            await ses.get("https://vseosvita.ua/test/go-logout", headers={"user-agent":useragent}, cookies=cock)