import urllib.request
from bs4 import BeautifulSoup
import psycopg2
import urllib
import os


def connect_psql():
    urllib.parse.uses_netloc.append("postgres")
    database_url = urllib.parse.urlparse(os.environ["DATABASE_URL"])

    conn = psycopg2.connect(
        database=database_url.path[1:],
        user=database_url.username,
        password=database_url.password,
        host=database_url.hostname,
        port=database_url.port
    )
    return conn


def get_users():
    conn = connect_psql()
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def first_insert_database_to_miyadai():
    conn = connect_psql()
    cur = conn.cursor()
    global day, menu, url

    # URLの指定
    html = urllib.request.urlopen("http://gakumu.of.miyazaki-u.ac.jp/gakumu/allnews")
    soup = BeautifulSoup(html, "html.parser")

    # テーブルを指定
    ul = soup.findAll('ul', class_='category-module')

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


def oshirase_print(i):
    conn = connect_psql()
    cur = conn.cursor()
    cur.execute("SELECT * FROM miyadai ORDER BY id DESC;")
    sendList = []
    for r in range(i):
        b = cur.fetchone()
        sendList2 = [b[1], b[2], b[3]]
        send = "\n".join(sendList2)
        sendList.append(send)
        sendList.append("\n")
    send = " \n".join(sendList)
    return send


def oshirase_check():
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
        for r in reversed(range(i)):
            cur.execute("INSERT INTO miyadai (days, title, url) VALUES (%s, %s, %s)",
                        (days[r], menus[r], urls[r]))
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
    num = oshirase_check()
    if num != 0:
        print(oshirase_print(num))
    else:
        print(oshirase_print(5))
