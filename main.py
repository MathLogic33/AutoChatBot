
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os

import datetime

import time

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = "WKo23RcJVx217vTrspQWAEoMJiyVSnXrRfcP14La9CrRt6Ut5Crm/hqpV8jjhwDoGI7oeGSWxAAb4at+Fs9AN7ZalJotjHl4v1ekMAxfF9k4ifywUWlNS8Y/B8mCUqhVtxUfVPDPeZKJIk6CC9h7/AdB04t89/1O/w1cDnyilFU="
YOUR_CHANNEL_SECRET = "20344a9bbc0c4f9aec0e58864bd552b0"

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "こんにちは":
       line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
    if event.message.text == "1から10までの数を全て足して":
       line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="55"))
    messageText = event.message.text
    messageList = ["日本", "アメリカ"]
    attributeList = ["時間"]
    japanList = [attributeList[0], messageList[0]]
    usaList = [attributeList[0], messageList[1]]
    totalList = [attributeList, messageList]
    n = 1
    memoryList = []
    for r in range(len(totalList)):
        for y in range(len(totalList[r])):
            for e in range(len(totalList[r][y])):
                for q in range(len(messageText)):
                    if totalList[r][y][e] == messageText[q]:
                        if len(totalList[r][y]) == n:
                            memoryList.append(totalList[r][y])
                            break
                        n += 1
            n = 1
    c = [1, 1]
    utcnow = datetime.datetime.utcnow()
    for o in range(len(memoryList)):
        for x in range(len(japanList)):
            if memoryList[o] == japanList[x]:
                if len(japanList) == c[0]:
                    time_dt_ja = datetime.timedelta(hours=9)
                    now = utcnow + time_dt_ja
                    line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=now.strftime('%Y年%m月%d日 %H:%M:%S')))
                    return
                c[0] += 1
        for k in range(len(usaList)):
            if memoryList[o] == usaList[k]:
                if len(usaList) == c[1]:
                    time_dt_us = datetime.timedelta(hours=5)
                    now = utcnow + time_dt_us
                    line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=now.strftime('%Y年%m月%d日 %H:%M:%S')))
                    return
                c[1] += 1
    if memoryList[0] == "時間":
        now = datetime.datetime.now()
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=now.strftime('%Y年%m月%d日 %H:%M:%S')))
        return

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)