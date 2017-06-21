import urllib.request
from bs4 import BeautifulSoup
import psycopg2
import urllib
import os


def connect_psql():
	urllib.parse.uses_netloc.append("postgres")
	url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
	
	conn = psycopg2.connect(
	    database=url.path[1:],
	    user=url.username,
	    password=url.password,
	    host=url.hostname,
	    port=url.port
	)
	return conn

def miyadaiOshiraseInit():
    conn = connect_psql()
    cur = conn.cursor()
    
    # URLの指定
    html = urllib.request.urlopen("http://gakumu.of.miyazaki-u.ac.jp/gakumu/allnews")
    soup = BeautifulSoup(html, "html.parser")
    
    # テーブルを指定
    ul = soup.findAll('ul', class_='category-module')
    
    sendList = []
    for li_month in reversed(ul[0].findAll('li')):
        for li in reversed(li_month.findAll('li')):
            for span in li.findAll('span'):
                if span.string is not None:
                    day = span.string
            for a in li.findAll('a'):
                if a.string is not None:
                    menu = a.string.strip()
                    url = 'http://gakumu.of.miyazaki-u.ac.jp' + a.get('href')
            cur.execute("INSERT INTO miyadai (days, title, url) VALUES (%s, %s, %s)", (day, menu, url))   
    conn.commit()
    cur.close()
    conn.close()

    return "success"

def miyadaiOshirasePrint(i):
    conn = connect_psql()
    cur = conn.cursor()
    cur.execute("SELECT * FROM miyadai ORDER BY id DESC;")
    sendList = []
    for num in range(i):
        b = cur.fetchone()
        sendList2 = []
        sendList2.append(b[1])
        sendList2.append(b[2])
        sendList2.append(b[3])
        send = "\n".join(sendList2)
        sendList.append(send)
        sendList.append("\n")
    send = " \n".join(sendList)
    return send

def miyadaiOshiraseCheck():
    conn = connect_psql()
    cur = conn.cursor()
    
    # URLの指定
    html = urllib.request.urlopen("http://gakumu.of.miyazaki-u.ac.jp/gakumu/allnews")
    soup = BeautifulSoup(html, "html.parser")
    
    # テーブルを指定
    ul = soup.findAll('ul', class_='category-module')
    
    days = []
    menus = []
    urls = []
    cur.execute("SELECT * FROM miyadai ORDER BY id DESC;")
    b = cur.fetchone()
    i = 0
    loop_flag = 1
    for li_month in ul[0].findAll('li'):
        for li in li_month.findAll('li'):
            for span in li.findAll('span'):
                if span.string is not None:
                    days.append(span.string)
            for a in li.findAll('a'):
                if a.string is not None:
                    menus.append(a.string.strip())
                    urls.append('http://gakumu.of.miyazaki-u.ac.jp' + a.get('href'))
            if b[3] == urls[i]:
                loop_flag = 0
            if loop_flag == 0:
                break            
            i += 1
        if loop_flag == 0:
            break              
    if i != 0:
        for num in reversed(range(i)):
            cur.execute("INSERT INTO miyadai (days, title, url) VALUES (%s, %s, %s)", (days[num], menus[num], urls[num]))
    else:
        cur.close()
        conn.close()
        return 0
    conn.commit()
    cur.close()
    conn.close()
    return i

if __name__ == "__main__":
#    send = miyadaiOshirasePrint(1)
#    print(send)
#    miyadaiOshiraseInit()
    print(miyadaiOshiraseCheck())