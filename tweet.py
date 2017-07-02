# encoding: utf-8
import json
import os

from requests_oauthlib import OAuth1Session


def tweet(txt):
    CK = os.environ.get('TWITTER_CK')
    CS = os.environ.get('TWITTER_CS')
    AT = os.environ.get('TWITTER_AT')
    ATS = os.environ.get('TWITTER_ATS')

    twitter = OAuth1Session(CK, CS, AT, ATS)

    url = "https://api.twitter.com/1.1/statuses/update.json"

    tweet_msg = txt

    params = {"status": tweet_msg}

    req = twitter.post(url, params=params)

    if req.status_code == 200:
        print("Tweet Succeed!")
        return 0
    else:
        print("Tweet ERROR : %d" % req.status_code)
        return 1


def tweet_with_media(tweet_msg, file_name):
    CK = os.environ.get('TWITTER_CK')
    CS = os.environ.get('TWITTER_CS')
    AT = os.environ.get('TWITTER_AT')
    ATS = os.environ.get('TWITTER_ATS')

    twitter = OAuth1Session(CK, CS, AT, ATS)

    url_media = "https://upload.twitter.com/1.1/media/upload.json"
    url_text = "https://api.twitter.com/1.1/statuses/update.json"

    # 画像投稿
    files = {"media": open(file_name, 'rb')}
    req_media = twitter.post(url_media, files=files)

    # レスポンスを確認
    if req_media.status_code != 200:
        print("画像アップデート失敗: %s", req_media.text)
        return 1

    # Media ID を取得
    media_id = json.loads(req_media.text)['media_id']
    print("Media ID: %d" % media_id)

    # Media ID を付加してテキストを投稿
    params = {'status': tweet_msg, "media_ids": [media_id]}
    req_text = twitter.post(url_text, params=params)

    # 再びレスポンスを確認
    if req_text.status_code != 200:
        print("テキストアップデート失敗: %s", req_text.text)
        return 1
    else:
        return 0


if __name__ == "__main__":
    # tweet("テスト用ツイート")
    tweet_with_media("画像付きツイートテスト", "screen.png")
