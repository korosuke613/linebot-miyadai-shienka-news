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

line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN')) #Your Channel Access Token

handler = WebhookHandler(os.environ.get('CHANNEL_SECRET')) #Your Channel Secret

print("croning")

num = miyadai.miyadaiOshiraseCheck()
if(num != 0):
	rows = miyadai.getUsers()
	userList = []
	for row in rows:
		userList.append(row[0])
	
	line_bot_api.multicast(userList, TextSendMessage(text='【新着情報】\n' + miyadai.miyadaiOshirasePrint(num)))

print('new event = ' + num)