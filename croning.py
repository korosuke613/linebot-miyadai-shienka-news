# encoding: utf-8

import os
import miyadai
import urllib.request
import tweet

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

line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN')) #Your Channel Access Token

handler = WebhookHandler(os.environ.get('CHANNEL_SECRET')) #Your Channel Secret

print("croning")
txt = miyadai.miyadaiOshirasePrint(1)
tweet.tweet(txt)
num = miyadai.miyadaiOshiraseCheck()
if(num != 0):
	rows = miyadai.getUsers()
	userList = []
	for row in rows:
		userList.append(row[0])
	txt = miyadai.miyadaiOshirasePrint(num)
	line_bot_api.multicast(userList, TextSendMessage(text='【新着情報】\n' + txt))
	tweet.tweet(txt)

print("num =", num)
