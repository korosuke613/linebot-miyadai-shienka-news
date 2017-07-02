# encoding: utf-8

import os
import re
import urllib.request

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent
)

import miyadai
from doco.client import Client

app = Flask(__name__)

HELP = "★宮大支援課お知らせBOT[非公式]\nこのBOTは非公式のものです。宮崎大学とは一切関係ありません。\n支援課からの新しいお知らせがあったときにこのBOTが教えてくれます\n・\'宮大\'を送信すると直近5" \
       "件のお知らせを表示します\n・\'help\'を送信するとこのメッセージを表示します\n・Twitterアカウントはこちら↓\nhttps://twitter.com/miya_330_bot "

line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))  # Your Channel Access Token
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))  # Your Channel Secret
c = Client(apikey=os.environ.get('DOCOMO_API_KEY'))
print_num = 0


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
            return match.group(1)
        i += 1


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    isMiyadaiPrintOnce = False
    isMiyadaiPrint = False
    text = event.message.text  # message from user
    profile = line_bot_api.get_profile(event.source.user_id)
    if '宮大' in text:
        # 正規表現
        pattern = r'([+-]?[0-9]+\.?[0-9]*)'
        if re.search(pattern, text):
            global print_num
            print_num = int(re.search(pattern, text).group(1))
            if 0 < print_num <= 5:
                txt = miyadai.oshirase_print_once(print_num-1)
                isMiyadaiPrintOnce = True
            else:
                txt = miyadai.oshirase_print(5)
        else:
            txt = miyadai.oshirase_print(5)
        isMiyadaiPrint = True
    elif "help" in text:
        txt = HELP
    else:
        user = {'nickname': profile.display_name}
        res = c.send(utt=text, apiname='Dialogue', **user)
        if c.last_response.status_code == 200:
            txt = res['utt']
        else:
            txt = response_ai(text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=txt))  # reply the same message from user
    if isMiyadaiPrintOnce:
        conn = miyadai.connect_psql()
        cur = conn.cursor()
        news_url = miyadai.oshirase_print_once_only_url(print_num-1)
        cur.execute("select media_url from image_tbl where url = %s", (news_url,))
        b = cur.fetchone()
        line_bot_api.reply_message(
            event.reply_token,
            # TextSendMessage(text=txt),  # reply the same message from user
            ImageSendMessage(original_content_url=b[0], preview_image_url=b[0])
        )
    print(event.source.user_id, profile.display_name, profile.status_message)
    print("Message =", text)
    print("Reply =", txt)
    conn = miyadai.connect_psql()
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM users WHERE user_id = %s ", (event.source.user_id,))
    b = cur.fetchone()
    print("SELECT %s FROM users WHERE user_id = 1", txt)
    if b[0] != 0:
        cur.execute("UPDATE users SET send_num = send_num + 1 WHERE user_id = %s", (event.source.user_id,))
    else:
        cur.execute("INSERT INTO users (user_id, display_name, status_message, send_num) VALUES (%s, %s, %s, %s)",
                    (event.source.user_id, profile.display_name, profile.status_message, '1',))
    if isMiyadaiPrint:
        txt = '宮大お知らせ'
    cur.execute("INSERT INTO msg_logs (days, times, user_id, user_send, bot_send) VALUES (CURRENT_DATE, CURRENT_TIME, "
                "%s, %s, %s) ", (event.source.user_id, text, txt,))
    conn.commit()
    cur.close()
    conn.close()


@handler.add(FollowEvent)
def handle_follow(event):
    txt = HELP
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=txt))  # reply the same message from user


@handler.add(JoinEvent)
def handle_join(event):
    txt = HELP
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=txt))  # reply the same message from user


@handler.add(UnfollowEvent)
def handle_unfollow():
    app.logger.info("Got Unfollow event")


@handler.add(LeaveEvent)
def handle_leave():
    app.logger.info("Got leave event")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ['PORT'])
