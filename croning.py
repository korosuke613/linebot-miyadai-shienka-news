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

print("croling...")
# 何個新着情報があるか取得
num = 0
try:
    num = miyadai.oshirase_check()
except Exception as e:
    line_bot_api.push_message(os.environ.get('FUTA_ID'), e)
    print(e)

print("num =", num)
if num != 0:
    # 登録ユーザを確認
    rows = miyadai.get_users()
    userList = []
    for row in rows:
        userList.append(row[0])

    # お知らせの数だけツイート
    for r in reversed(range(num)):
        # お知らせURLを取得
        news_url = miyadai.oshirase_print_once_only_url(r)
        # スクショ撮影
        miyadai.screen_shot(news_url)
        # スクショをローカルに保持
        miyadai.open_image(news_url)
        # お知らせテキストの取得
        txt = miyadai.oshirase_print_once(r)
        # 画像付きツイート
        media_url = tweet.tweet_with_media(miyadai.oshirase_print_once(r), "send_img.png")
        tweet.media_insert_to_database(news_url, media_url)
        # お知らせテキストのline配信
        line_bot_api.multicast(userList, TextSendMessage(text='【新着情報】\n' + txt))
        # ツイートした画像のURL取得
        if not media_url == -1:
            line_bot_api.multicast(
                userList,
                ImageSendMessage(original_content_url=media_url, preview_image_url=media_url))
