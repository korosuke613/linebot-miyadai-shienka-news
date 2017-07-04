# encoding: utf-8

import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    CarouselTemplate, CarouselColumn, MessageTemplateAction, URITemplateAction,
    TemplateSendMessage)

import miyadai

line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))  # Your Channel Access Token
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))  # Your Channel Secret


def get_uri_list(offset: int=0):
    _uriList = [miyadai.oshirase_print_once_only_url(offset + r) for r in range(5)]
    return _uriList


def get_title_list(offset: int=0):
    _titleList = [miyadai.oshirase_print_once_only_title(offset + r) for r in range(5)]
    return _titleList


def get_carouselList(offset: int=0):
    conn = miyadai.connect_psql()
    cur = conn.cursor()

    cur.execute("SELECT * FROM miyadai WHERE id <= (SELECT max(id) FROM miyadai) - %s ORDER BY id DESC ", (offset,))

    _uriList = []
    _titleList = []
    _textList = []
    for r in range(5):
        b = cur.fetchone()
        _uriList.append(b[3])
        _titleList.append(b[2])
        _textList.append(b[1])

    _image_urlList = []
    cur.execute(
        "select media_url from image_tbl, miyadai WHERE miyadai.url = image_tbl.url "
        "AND id <= (SELECT max(id) FROM miyadai) - %s ORDER BY id DESC", (offset,))

    for r in range(5):
        b = cur.fetchone()
        if not b[0]:
            _image_urlList.append("https://www.kuaskmenkyo.necps.jp/miyazaki/UnivImages/宮崎大学画像.jpg")
        else:
            _image_urlList.append(b[0])
    cur.close()
    conn.close()
    print(_image_urlList)
    _sendList = [_titleList, _textList, _uriList, _image_urlList]
    return _sendList


def get_carousel(offset: int=0):
    newsList = get_carouselList(offset)
    titleList = newsList[0]
    textList = newsList[1]
    uriList = newsList[2]
    imageUrlList = newsList[3]
    print(imageUrlList)
    carouselList = [
        CarouselColumn(
                thumbnail_image_url=imageUrlList[r],
                title=titleList[r],
                text=textList[r],
                actions=[
                    MessageTemplateAction(
                        label='画像を見る',
                        text='宮大' + str(r+1)
                    ),
                    URITemplateAction(
                        label='URLを開く',
                        uri=uriList[r]
                    )
                ]
            )
        for r in range(5)]

    _send_carousel = TemplateSendMessage(
        alt_text='宮大お知らせ',
        template=CarouselTemplate(
            columns=carouselList
        )
    )
    return _send_carousel


if __name__ == "__main__":
    send_carousel = get_carousel()
    line_bot_api.push_message(os.environ.get('FUTA_ID'), send_carousel)