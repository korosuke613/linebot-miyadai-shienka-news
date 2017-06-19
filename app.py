# encoding: utf-8

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
)

app = Flask(__name__)

line_bot_api = LineBotApi('xwRf0z0tymU9AxYSvtQ9doThh2IH95zcaFtQvpE3X6JAZYsVgKhFVa8uoOnC7Pbjx1XNdGfEUvl49aX8XcqVhk9jYnjUv4yJ3eGExx5rIEIwLs/9MN+ZEt/kRyQ8kOXpkPrTdel3h4Val7X2OHMDpAdB04t89/1O/w1cDnyilFU=') #Your Channel Access Token
handler = WebhookHandler('496310bb9167546bbbe34bc8cb0177c8') #Your Channel Secret

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
    txt = responseAI(text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=txt) #reply the same message from user


def responseAI(recv):
    recv_enc = urllib.parse.quote(recv)
#    url_start = "https://chatbot-api.userlocal.jp/api/chat?message="
#    url_end = "&key=e102948565f3c106b732"
#    url = url_start + recv_enc + url_end
#    html = urllib.request.urlopen(url).read().decode("utf-8")
#    pattern = re.compile(r"\"([^\"]*)\"")
#    iterator = pattern.finditer(html)
#    i = 0
#for match in iterator:
#        if i == 3:
#            return (match.group(1))
#        i += 1

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
