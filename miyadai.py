import urllib.request
from bs4 import BeautifulSoup

def miyadaiOshirase():
    
    # URLの指定
    html = urllib.request.urlopen("http://gakumu.of.miyazaki-u.ac.jp/gakumu/allnews")
    soup = BeautifulSoup(html, "html.parser")
    
    # テーブルを指定
    ul = soup.findAll('ul', class_='category-module')
    
    i = 0
    sendList = []
    for li_month in ul[0].findAll('li'):
        for li in li_month.findAll('li'):
            sendList2 = []
            for span in li.findAll('span'):
                if span.string is not None:
                    sendList2.append(span.string)
            for a in li.findAll('a'):
                if a.string is not None:
                    sendList2.append(a.string.strip())
                    sendList2.append('http://gakumu.of.miyazaki-u.ac.jp' + a.get('href'))
            send = "\n".join(sendList2)
            sendList.append(send)
            sendList.append("\n")
            i += 1 
            if i >= 5:
                send = " \n".join(sendList)
                return send

import os
if __name__ == "__main__":
    testStr = miyadaiOshirase()
    print(testStr)