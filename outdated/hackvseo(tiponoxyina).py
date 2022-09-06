# -*- coding: utf-8 -*-
import asyncio,aiohttp,re
from aiohttp_proxy import ProxyConnector, ProxyType
from random import randint

cookies = {}

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"}


name = ["Вадим Шумило", "Андрій Васильчук", "Захарчук Валерія", "Віра Шевчук", "Микитюк Георгій", "Василенко Адам", "Денис Микитюк", "Анатолій Тарасович", "Всеволод Шевченко", "Олег Іванченко", "Лариса Пономарчук", "Олена Броваренко", "Анна Таращук", "Катерина Броварчук"]

async def GetQuestions(url: str):
    ses = aiohttp.ClientSession()
    print(1)
    mezhdy = re.findall(r"start/(.+)", url)
    if mezhdy == []:
        mezhdy = re.findall(r"code=(.+)", url)
        if mezhdy == []:
            return "NeVseOsvita"
    code = mezhdy[0]
    onereq = await ses.post(f"https://vseosvita.ua/test/start/{code}", cookies=cookies, headers=headers)
    print(onereq)
    check = re.search(r'vo.popup(.+)', await onereq.text())
    if check != None:
        return "TestEnded"
    await ses.post("https://vseosvita.ua/test/go-settings", cookies=cookies, headers=headers, data={"TestDesignerSettings[full_name]": name[randint(0,13)]}, params={"code": code})
    quests = await ses.get("https://vseosvita.ua/ext/test-go-pupil/init?isAjax=1", headers=headers, cookies=cookies)
    questsjson = await quests.json()
    placecookies = ses.cookie_jar.filter_cookies('https://vseosvita.ua/')
    lp = {} 
    for i,y in placecookies.items():
        lp.update({y.key: y.value})
#   await ses.close()
    return [questsjson["payload"]["quests"], lp]
async def ProxodTesta(quest, cookies2):
    ses = aiohttp.ClientSession(connector=connector,cookies=cookies2)
    url = "https://vseosvita.ua/ext/test-go-pupil/save-user-answer?isAjax=1"
    for i in quest:
        questid = i["id"]
        data = {f"answers[{questid}][0]": 0, "id_quest": questid}
        if i["quest_type"] == 1: #Одна правильная
            await ses.post(url, cookies=cookies, headers=headers, data=data) 
        elif i["quest_type"] == 2: #Несколько правильных
            await ses.post(url, cookies=cookies, headers=headers, data=data)
        elif i["quest_type"] == 3:  #Введи ответ
            await ses.post(url, cookies=cookies, headers=headers, data={f"answers[{questid}]": "AHCKED?", "id_quest": questid})
        elif i["quest_type"] == 4: # Відповідність
            await ses.post(url, cookies=cookies, headers=headers, data=data)
        elif i["quest_type"] == 6: # Ввести несколько ответов
            data = {}
            for x in i["answer_arr"]:
                data.update({f"answers[{questid}][{x}]": "AHCKED?"})
            data.update({"id_quest": questid})
            await ses.post(url, cookies=cookies, headers=headers, data=data)
        elif i["quest_type"] == 7: #Выбрать правильный ответ
            data = {}
            for x in i["answer_arr"]:
                value = ""
                for y in i["answer_arr"][x]["values"]:
                    value+=y["value"]
                    break
                data.update({f"answers[{questid}][{x}]": value})
            data.update({"id_quest": questid})
            await ses.post(url, cookies=cookies, headers=headers, data=data)
        elif i["quest_type"] == 8:
            data = {}
            for x in range(0, len(i['answer_arr'])):
                data.update({f"answers[{questid}][{x}]": x})
            for x in range(0, len(i['answer_arr'])):
                list = [x for x in range(0, len(i['answer_arr']))]
                data.update({f"answers[{questid}][@show-rules][]": list})
            data.update({"id_quest": questid})
            await ses.post(url, cookies=cookies, headers=headers, data=data)
        elif i["quest_type"] == 9:
            data = {f"answers[{questid}][0][]": [randint(1, int(i["answer_arr"][1])), randint(1, int(i["answer_arr"][2])),10], "id_quest": questid}
            await ses.post(url, cookies=cookies, headers=headers, data=data)
#        await ses.close()
async def GetAnswers(cookies2):
    ses = aiohttp.ClientSession(connector=connector,cookies=cookies2)
    response = await ses.post("https://vseosvita.ua/ext/test-go-pupil/show-answer-short?isAjax=1", cookies=cookies, headers=headers)
    htm = await response.json()
    html = htm["modal"]["html"].replace("\n", "")
    htmls = html.replace("<script>    vo.test_pupil.init_view_answer_short_go_pupil(0);</script>", "")
    htmlbody = f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Document</title></head><body>{htmls}'
    htmlbody+='    <script>document.querySelector(".v-test-result-new-head").remove(); for (let i of document.querySelectorAll(".v-test-count")) { i.remove(); } for (let i of document.getElementsByTagName("img")) { i.src = Object.assign({}, i.dataset).src; } for (let i of document.getElementsByTagName("image")) {i.href.animVal = Object.assign({}, i.dataset).src; i.href.baseVal = Object.assign({}, i.dataset).src;}for (let i of document.getElementsByTagName("ellipse")) {if (i.attributes.fill.textContent == "red") {i.remove()}}for (let i of document.querySelectorAll("div.v-correct-answer")) { i.remove(); } for (let i of document.querySelectorAll(".v-test-questions-radio-block")) { i.remove(); } for (let i of document.querySelectorAll(".v-test-questions-checkbox-block")) { i.remove(); } for (let i of document.querySelectorAll(".v-col-12.v-col-last")) { i.remove(); }for (let i of document.getElementsByTagName("li")) {if (i.outerHTML.match("<p>") == null) {i.innerText = i.innerText.replace(/;/g, "\\nили\\n");}}for (let i of document.querySelectorAll(".rk-selected__pair")) {i.innerText = i.innerText.replace(/\\n/g, " - ")}for (let i of document.querySelectorAll(".vr-control > strong")) {if (i.innerHTML.match(/color: red;/) == null) {if (i.innerHTML.match(\'<span style=\\"color:green;\\">(.+)</span>\') != null) {i.innerHTML = i.innerHTML.match(\'<span style=\\"color:green;\\">(.+)</span>\')[0]+" ";}} else {i.remove();}}for (let i of document.querySelectorAll(".v-block-answers-cross-block")) {i.children[0].innerHTML = i.children[0].innerText; i.children[0].innerHTML = i.children[0].innerHTML+i.children[1].innerHTML;i.children[1].remove();i.children[0].innerHTML = i.children[0].innerHTML.replace(/\\n/g, " ");var check = i.children[0].innerHTML.match("<p>(.+)</p>");if (check != null){i.children[0].innerHTML = i.children[0].innerHTML.replace(check[0], " - "+check[1]+"<br><br>");}}</script></body>'
#    await ses.close()
    return htmlbody