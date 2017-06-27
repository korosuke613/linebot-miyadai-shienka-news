# encoding: utf-8

import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    TextSendMessage
)

import miyadai
import tweet

line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))  # Your Channel Access Token

handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))  # Your Channel Secret

print("croling")
num = miyadai.oshirase_check()
if num != 0:
    rows = miyadai.get_users()
    userList = []
    for row in rows:
        userList.append(row[0])
    txt = miyadai.oshirase_print(num)
    line_bot_api.multicast(userList, TextSendMessage(text='【新着情報】\n' + txt))
    for r in reversed(range(num)):
        tweet.tweet(miyadai.oshirase_print_once(r))

print("num =", num)
