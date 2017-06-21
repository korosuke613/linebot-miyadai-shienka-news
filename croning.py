# encoding: utf-8

import os
import miyadai
import urllib.request

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
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

#line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN')) #Your Channel Access Token
line_bot_api = LineBotApi("xwRf0z0tymU9AxYSvtQ9doThh2IH95zcaFtQvpE3X6JAZYsVgKhFVa8uoOnC7Pbjx1XNdGfEUvl49aX8XcqVhk9jYnjUv4yJ3eGExx5rIEIwLs/9MN+ZEt/kRyQ8kOXpkPrTdel3h4Val7X2OHMDpAdB04t89/1O/w1cDnyilFU=") #Your Channel Access Token

#handler = WebhookHandler(os.environ.get('CHANNEL_SECRET')) #Your Channel Secret
handler = WebhookHandler("ddfc9f05c96e0d56a473112c57b8c316") #Your Channel Secret

print("croning")

line_bot_api.push_message('U64a243cd7b86df5261b788685e561a00', TextSendMessage(text='Hello World!'))

	