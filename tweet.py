# -*- coding:utf-8 -*-
import json
from requests_oauthlib import OAuth1Session

def tweet(txt):
	CK ="q4wnL1G8jdYzdt9o02opRuiIB"
	CS ="CzYTDMdGEY5AY7xkzWWKSCiPSBYt6FT6Pzz0DQKldquUBCRDWV"
	AT ="877612557074219015-ylFv6FcdhY6FzGhaa9pUNr5vtu936r1"
	ATS ="TE6zUxankjYnfeW4K9cOGBu6mKHjb9msir0pwapHRIk9j"

	twitter = OAuth1Session(CK, CS, AT, ATS)

	url = "https://api.twitter.com/1.1/statuses/update.json"

	tweet = txt

	params = {"status" : tweet}

	req = twitter.post(url, params = params)

	if req.status_code == 200:
	    print("Tweet Succeed!")
	    return 0
	else:
	    print("Tweet ERROR : %d"% req.status_code)
	    return 1