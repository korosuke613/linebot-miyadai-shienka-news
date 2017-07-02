# encoding: utf-8

import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    TextSendMessage, ImageSendMessage
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
    for r in reversed(range(num)):
        url = miyadai.oshirase_print_once_only_url(r)
        miyadai.screen_shot(url)
        miyadai.open_image(url)
        tweet.tweet_with_media(miyadai.oshirase_print_once(r), "send_img.png")
    line_bot_api.multicast(userList, TextSendMessage(text='【新着情報】\n' + txt))
    if num == 1:
        news_url = miyadai.oshirase_print_once_only_url(0)
        media_url = miyadai.oshirase_print_once_only_media_url(news_url)
        if media_url:
            line_bot_api.multicast(
                userList,
                ImageSendMessage(original_content_url=media_url, preview_image_url=media_url))

print("num =", num)
