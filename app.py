# encoding: utf-8

import os
import miyadai
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

HELP = "★宮大支援課お知らせBOT[非公式]" + "\n" + "このBOTは非公式のものです。宮崎大学とは一切関係ありません。" +  "\n" + "支援課からの新しいお知らせがあったときにこのBOTが教えてくれます" + "\n" + "・'宮大'を送信すると直近5件のお知らせを表示します" + "\n" + "・'help'を送信するとこのメッセージを表示します" + "\n" + "・Twitterアカウントはこちら↓" + "\n" + "https://twitter.com/miya_330_bot"

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
        txt = miyadai.miyadaiOshirasePrint(5)
    elif "help" in text:
        txt = HELP
    else:    
        txt = response_ai(text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=txt)) #reply the same message from user
    profile = line_bot_api.get_profile(event.source.user_id)
    print(event.source.user_id, profile.display_name, profile.status_message)
    print("Message =" , text)
    conn = miyadai.connect_psql()
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM users WHERE user_id = %s ", (event.source.user_id,))
    b = cur.fetchone()
    if b[0] != 0:
        cur.execute("UPDATE users SET send_num = send_num + 1 WHERE user_id = %s", (event.source.user_id,))
    else:
        cur.execute("INSERT INTO users (user_id, display_name, status_message, send_num) VALUES (%s, %s, %s, %s)", (event.source.user_id, profile.display_name, profile.status_message, '1',))  
    conn.commit()
    cur.close()
    conn.close() 

@handler.add(FollowEvent)
def handle_follow(event):
    txt = HELP
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=txt)) #reply the same message from user

@handler.add(JoinEvent)
def handle_join(event):
    txt = HELP
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
    url = urlStart + recvEnc + os.environ.get('CHATBOT_KEY')
    html = urllib.request.urlopen(url).read().decode("utf-8")
    pattern = re.compile(r"\"([^\"]*)\"")
    iterator = pattern.finditer(html)
    i = 0
    for match in iterator:
        if i == 3:
            return (match.group(1))
        i += 1


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
