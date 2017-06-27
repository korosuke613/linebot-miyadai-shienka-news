# encoding: utf-8
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


if __name__ == "__main__":
    tweet("テスト用ツイート")
