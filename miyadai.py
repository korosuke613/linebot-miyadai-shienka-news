import urllib.request
from bs4 import BeautifulSoup
import psycopg2
import urllib
import os
from selenium import webdriver
from PIL import Image
import re

import tweet


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


def oshirase_print_once(i):
    conn = connect_psql()
    cur = conn.cursor()
    cur.execute("SELECT * FROM miyadai WHERE id = (SELECT max(id) FROM miyadai) - %s", (i,))
    b = cur.fetchone()
    sendList2 = [b[1], b[2], b[3]]
    send = "\n".join(sendList2)

    return send


def oshirase_print_once_only_url(i):
    conn = connect_psql()
    cur = conn.cursor()
    cur.execute("SELECT * FROM miyadai WHERE id = (SELECT max(id) FROM miyadai) - %s", (i,))
    b = cur.fetchone()
    send = b[3]

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


def screen_shot(screen_url):
    driver = webdriver.PhantomJS()
    driver.set_window_size(1024, 768)
    driver.get(screen_url)
    margin = 30
    left = driver.execute_script("""var element = document.getElementById('wrapper2');var rect = 
    element.getBoundingClientRect(); return rect.left;""") - margin
    top = driver.execute_script("""var element = document.getElementById('wrapper2');var rect = 
    element.getBoundingClientRect(); return rect.top;""")
    right = driver.execute_script("""var element = document.getElementById('wrapper2');var rect = 
    element.getBoundingClientRect(); return rect.width;""") + left + margin
    bottom = driver.execute_script("""var element = document.getElementById('wrapper2');var rect = 
        element.getBoundingClientRect(); return rect.height;""") + top + margin
    driver.save_screenshot('screen_origin.png')
    driver.close()

    im = Image.open('screen_origin.png')
    im = im.crop((left, top, right, bottom))  # defines crop points
    im.save('screen.png')  # saves new cropped image

    conn = connect_psql()
    cur = conn.cursor()
    pic = open('screen.png', 'rb').read()
    cur.execute("INSERT INTO image_tbl (url, image) VALUES (%s, %s)",
                (screen_url, psycopg2.Binary(pic)))
    conn.commit()
    cur.close()
    conn.close()


def first_insert_to_img_table():
    conn = connect_psql()
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM miyadai;")
    col_count = cur.fetchone()
    print(col_count)
    cur.execute("SELECT url FROM miyadai ORDER BY id DESC;")
    for r in range(col_count[0]):
        b = cur.fetchone()
        print(b[0])
        screen_shot(b[0])

    cur.close()
    conn.close()


def open_image(send_url):
    conn = connect_psql()
    cur = conn.cursor()
    cur.execute("SELECT image FROM image_tbl WHERE url = %s", (send_url,))

    row = cur.fetchone()
    pic = row[0]

    f = open('send_img.png', 'wb')
    f.write(pic)
    f.close()

    cur.close()
    conn.close()


if __name__ == "__main__":
    #    send = miyadaiOshirasePrint(1)
    #    print(send)
    #    miyadaiOshiraseInit()
    #    num = 2
    #    for _r in reversed(range(num)):
    #       print(oshirase_print_once(_r))
    #    screen_shot('http://gakumu.of.miyazaki-u.ac.jp/gakumu/campuslifeinfo/campuslifeinfo/3456-2017-06-30-00-14-32.html')
    #   first_insert_to_img_table()
    #   screen_shot('http://gakumu.of.miyazaki-u.ac.jp/gakumu/campuslifeinfo/campuslifeinfo/3413-2017-6-1.html')
    #   open_image('http://gakumu.of.miyazaki-u.ac.jp/gakumu/jobinfo/jobinfonews/3457-kamikou.html')
    # tweet.tweet_with_media(oshirase_print_once(0), "send_img.png")
    pattern = r'([+-]?[0-9]+\.?[0-9]*)'
    text = "宮大"
    if re.search(pattern, text):
        num = re.search(pattern, text).group(1)
