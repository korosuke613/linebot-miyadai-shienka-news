# encoding: utf-8

import miyadai
from password import *
import urllib.request
import re
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, URITemplateAction, PostbackTemplateAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent
)

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN')) #Your Channel Access Token
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET')) #Your Channel Secret

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
def handle_text_message(event):
    text = event.message.text #message from user
    if '宮大' in text:
        txt = miyadai.miyadaiOshirase()
    elif "help" in text:
        txt = "★宮大支援課お知らせBOT[非公式]" + "\n" + "このBOTは非公式のものです。宮崎大学とは一切関係ありません。" +  "\n" + "・'宮大'を送信すると直近5件のお知らせを表示します" + "\n" + "・'help'を送信するとこのメッセージを表示します"
    else:    
        txt = response_ai(text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=txt)) #reply the same message from user

@handler.add(FollowEvent)
def handle_follow(event):
    txt = "★宮大支援課お知らせBOT[非公式]" + "\n" + "このBOTは非公式のものです。宮崎大学とは一切関係ありません。" +  "\n" + "・'宮大'を送信すると直近5件のお知らせを表示します" + "\n" + "・'help'を送信するとこのメッセージを表示します"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=txt)) #reply the same message from user

@handler.add(JoinEvent)
def handle_join(event):
    txt = "★宮大支援課お知らせBOT[非公式]" + "\n" + "このBOTは非公式のものです。宮崎大学とは一切関係ありません。" +  "\n" + "・'宮大'を送信すると直近5件のお知らせを表示します" + "\n" + "・'help'を送信するとこのメッセージを表示します"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=txt)) #reply the same message from user

@handler.add(UnfollowEvent)
def handle_unfollow():
    app.logger.info("Got Unfollow event")


@handler.add(LeaveEvent)
def handle_leave():
    app.logger.info("Got leave event")



def response_ai(recv):
    recvEnc = urllib.parse.quote(recv)
    urlStart = "https://chatbot-api.userlocal.jp/api/chat?message="
    urlEnd = "&key=e102948565f3c106b732"
    url = urlStart + recvEnc + urlEnd
    html = urllib.request.urlopen(url).read().decode("utf-8")
    pattern = re.compile(r"\"([^\"]*)\"")
    iterator = pattern.finditer(html)
    i = 0
    for match in iterator:
        if i == 3:
            return (match.group(1))
        i += 1


import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
