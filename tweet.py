# encoding: utf-8
import json
import os
import miyadaidb

from requests_oauthlib import OAuth1Session

myzk = miyadaidb.MiyadaiDatabaseControl()


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

    # Media ID を付加してテキストを投稿
    params = {'status': tweet_msg, "media_ids": [media_id]}
    req_text = twitter.post(url_text, params=params)
    media_url = json.loads(req_text.text)['entities']['media'][0]['media_url_https']
    # 再びレスポンスを確認
    if req_text.status_code != 200:
        print("テキストアップデート失敗: %s", req_text.text)
        return -1
    else:
        return media_url


def media_insert_to_database(news_url, media_url):
    myzk.cur.execute("UPDATE image_tbl SET media_url = %s WHERE url = %s", (media_url, news_url))
    myzk.conn.commit()


if __name__ == "__main__":
    # tweet("テスト用ツイート")
    # tweet_with_media("画像付きツイートテスト7", "screen.png")
    pass
