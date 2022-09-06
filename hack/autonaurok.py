# -*- coding: utf-8 -*-
import json
import aiohttp,asyncio,random,re

from hack import hacknaurok

ses = aiohttp.ClientSession()

async def GetTrueAnswers(url: str, wrong=0, GetFile = False):
    help = {}
    TrueAnswers = {}
    htmlbody='<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Document</title></head><body>'
    cycle=1
    sesid = await hacknaurok.GetSessiondId(url)
    Questions = await hacknaurok.GetQuestions(sesid)
    if wrong >= Questions["document"]["questions"]:
        return "NotValid"
    for i in Questions["questions"]:
        x = await hacknaurok.GetAnswerQuestions(i["id"])
        temp = []
        if GetFile == False:
            try:
                for AnswerOptions in x["options"]:
                    if AnswerOptions["correct"] == "1":
                        for QuestionOptions in i["options"]:
                            if AnswerOptions["value"] == QuestionOptions["value"]:
                                    if i["type"] == "quiz":
                                        temp.append(QuestionOptions["id"])
                                    if i["type"] == "multiquiz":
                                        temp.append(QuestionOptions["id"])
            finally:
                TrueAnswers.update({QuestionOptions["question_id"]: [temp, i["type"], i["point"]]})
        elif GetFile == True:
            try:
                for AnswerOptions in x["options"]:
                    if AnswerOptions["correct"] == "1":
                        for QuestionOptions in i["options"]:
                            if AnswerOptions["value"] == QuestionOptions["value"]:
                                    if i["type"] == "quiz":
                                        temp.append(QuestionOptions["id"])
                                    if i["type"] == "multiquiz":
                                        temp.append(QuestionOptions["id"])
            finally:
                TrueAnswers.update({QuestionOptions["question_id"]: [temp, i["type"], i["point"]]})
            try:
                quest = re.sub(r'\<[^>]*\>', '', i["content"])
                if x == "DontCloneAnswer":
                    htmlbody+=f"<p><b>{cycle}. ВОПРОС</b> - {quest}</p>"
                    htmlbody+=f"<p><b>ОТВЕТ</b> - <b>Не удалось найти ответ.</b></p>"
                    continue
                htmlbody+=f"<p><b>{cycle}. ВОПРОС</b> - {quest}</p>"
                for x in x["options"]:
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
    help.update({"show_answer": Questions["settings"]["show_answer"]})
    help.update({"homeworkType": Questions["settings"]["type"]})
    if int(wrong) != 0:
        keystodelete = {}
        for i in range(0,int(wrong)):
            while True:
                intp = random.randint(1, len(TrueAnswers.keys()))-1
                key = list(TrueAnswers.keys())[intp]
                if key in keystodelete:
                    continue
                keystodelete.update({key: int(intp)})
                break
        for i in keystodelete:
            while True:
                p = Questions["questions"][keystodelete[i]]["options"][random.randint(1, len(Questions["questions"][keystodelete[i]]["options"]))-1]
                if TrueAnswers[i][0][0] == p["id"]:
                    continue
                TrueAnswers.update({i: [[p["id"]], Questions["questions"][keystodelete[i]]["type"], Questions["questions"][keystodelete[i]]["point"]]})
                break
    if GetFile == False:
        return [TrueAnswers, help, url]
    elif GetFile == True:
        htmlbody+='</body></html>'
        return [TrueAnswers, help, url, htmlbody]




async def avtoproxod(TrueAnsw: list, time=0):
    TrueAnswers = TrueAnsw[0]
    help = TrueAnsw[1]
    url = TrueAnsw[2]
    sesid = await hacknaurok.GetSessiondId(url)
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "referer": str(url),
        "content-type": "application/json;charset=UTF-8",
        "accept": "application/json, text/plain, */*"
    }
    for i in TrueAnswers:
        jsonsend = {"session_id":int(sesid),"answer":TrueAnswers[i][0],"question_id":str(i),"show_answer":int(help["show_answer"]),"type":str(TrueAnswers[i][1]),"point":str(TrueAnswers[i][2]),"homeworkType":help["homeworkType"],"homework":True}
        print(jsonsend)
        x = await ses.put("https://naurok.com.ua/api2/test/responses/answer", headers=headers, json=jsonsend)
        print(await x.json())
        print(x)
        if time != 0:
            await asyncio.sleep(time / len(TrueAnswers))
    await ses.put(f"https://naurok.com.ua/api2/test/sessions/end/{sesid}", headers=headers)
