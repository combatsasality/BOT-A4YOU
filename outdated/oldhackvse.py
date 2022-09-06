# -*- coding: utf-8 -*-
import requests
import re,json,sys
from random import randint

cookies = {}

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"}

ses = requests.Session()
async def GetQuestions(url):
    mezhdy = re.search(r"start/(.+)", url)
    if mezhdy == None:
        return "NeVseOsvita"
    code = mezhdy.group().replace(r"start/", "")
    onereq = ses.post(f"https://vseosvita.ua/test/start/{code}", cookies=cookies, headers=headers)
    check = re.search('vo.popup(.+);', onereq.text)
    if check != None:
        return "TestEnded"
    ses.post("https://vseosvita.ua/test/go-settings", cookies=cookies, headers=headers, data={"TestDesignerSettings[full_name]":"YouAHCKED"}, params={"code": code})
    quests = ses.get("https://vseosvita.ua/ext/test-go-pupil/init?isAjax=1", headers=headers, cookies=cookies)
    return quests.json()["payload"]["quests"]

async def ProxodTesta(quest: dict):
    url = "https://vseosvita.ua/ext/test-go-pupil/save-user-answer?isAjax=1"
    for i in quest:
        questid = i["id"]
        data = {f"answers[{questid}][0]": 0, "id_quest": questid}
        if i["quest_type"] == 1: #Одна правильная
            ses.post(url, cookies=cookies, headers=headers, data=data) 
        elif i["quest_type"] == 2: #Несколько правильных
            ses.post(url, cookies=cookies, headers=headers, data=data)
        elif i["quest_type"] == 3:  #Введи ответ
            ses.post(url, cookies=cookies, headers=headers, data={f"answers[{questid}]": "AHCKED?", "id_quest": questid})
        elif i["quest_type"] == 4: # Відповідність
            ses.post(url, cookies=cookies, headers=headers, data=data)
        elif i["quest_type"] == 6: # Ввести несколько ответов
            data = {}
            for x in i["answer_arr"]:
                data.update({f"answers[{questid}][{x}]": "AHCKED?"})
            data.update({"id_quest": questid})
            ses.post(url, cookies=cookies, headers=headers, data=data)
        elif i["quest_type"] == 7: #Выбрать правильный ответ
            data = {}
            for x in i["answer_arr"]:
                value = ""
                for y in i["answer_arr"][x]["values"]:
                    value+=y["value"]
                    break
                data.update({f"answers[{questid}][{x}]": value})
            data.update({"id_quest": questid})
            ses.post(url, cookies=cookies, headers=headers, data=data)
        elif i["quest_type"] == 8:
            data = {}
            for x in range(0, len(i['answer_arr'])):
                data.update({f"answers[{questid}][{x}]": x})
            for x in range(0, len(i['answer_arr'])):
                list = [x for x in range(0, len(i['answer_arr']))]
                data.update({f"answers[{questid}][@show-rules][]": list})
            data.update({"id_quest": questid})
            ses.post(url, cookies=cookies, headers=headers, data=data)
        elif i["quest_type"] == 9:
            data = {f"answers[{questid}][0][]": [randint(1, int(i["answer_arr"][1])), randint(1, int(i["answer_arr"][2])),10], "id_quest": questid}
            ses.post(url, cookies=cookies, headers=headers, data=data)

async def GetAnswers():
    response = ses.post("https://vseosvita.ua/ext/test-go-pupil/show-answer-short?isAjax=1", cookies=cookies, headers=headers)
    html = response.json()["modal"]["html"].replace("\n", "")
    htmls = html.replace("<script>    vo.test_pupil.init_view_answer_short_go_pupil(0);</script>", "")
    return htmls
