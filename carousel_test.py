# encoding: utf-8

import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    TextSendMessage,
    CarouselTemplate, CarouselColumn, MessageTemplateAction, URITemplateAction,
    TemplateSendMessage)

line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))  # Your Channel Access Token
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))  # Your Channel Secret


def send_message_test():
    line_bot_api.push_message(os.environ.get('FUTA_ID'), TextSendMessage(text='send_message_test'))


def send_carousel_test():
    uriList = [
        'http://gakumu.of.miyazaki-u.ac.jp/gakumu/campuslifeinfo/campuslifeinfo/3459-2017-07-04-02-56-31.html',
        'http://gakumu.of.miyazaki-u.ac.jp/gakumu/campuslifeinfo/campuslifeinfo/3460-28-29.html']
    titleList = [
        '【重要】日本学生支援機構奨学金定期採用者へ書類配布のお知らせ',
        '平成28年熊本地震被災に伴う平成29年度後期授業料免除申請受付について']
    textList = ['2017年07月04日', '2017年07月04日']
    imageUrlList = ['https://pbs.twimg.com/media/DD3UMCcXUAA_dQs.jpg',
                    'https://pbs.twimg.com/media/DD3UNy-WsAEwH9g.jpg']

    carouselList = [
        CarouselColumn(
                thumbnail_image_url=imageUrlList[0],
                title=titleList[0],
                text=textList[0],
                actions=[
                    MessageTemplateAction(
                        label='画像を見る',
                        text='宮大' + str(r+1)
                    ),
                    URITemplateAction(
                        label='URLを開く',
                        uri=uriList[0]
                    )
                ]
            )
        for r in range(5)]

    carousel_template_message = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=carouselList
        )
    )

    line_bot_api.push_message(os.environ.get('FUTA_ID'), carousel_template_message)


if __name__ == "__main__":
    send_carousel_test()
