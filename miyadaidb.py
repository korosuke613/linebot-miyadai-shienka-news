import os
import urllib.request

import psycopg2
from bs4 import BeautifulSoup

from modules.controldb import DatabaseControl
from modules.exphantom import ScreenShot


class MiyadaiDatabaseControl(DatabaseControl):
    def __init__(self):
        super().__init__(os.environ["DATABASE_URL"])

    def first_insert_database_to_miyadai(self):
        _day = _menu = _url = None

        # URLの指定
        html = urllib.request.urlopen("http://gakumu.of.miyazaki-u.ac.jp/gakumu/allnews")
        soup = BeautifulSoup(html, "html.parser")

        # テーブルを指定
        ul = soup.findAll('ul', class_='category-module')

        for li_month in reversed(ul[0].findAll('li')):
            for li in reversed(li_month.findAll('li')):
                for span in li.findAll('span'):
                    if span.string is not None:
                        _day = span.string
                for a in li.findAll('a'):
                    if a.string is not None:
                        _menu = a.string.strip()
                        _url = 'http://gakumu.of.miyazaki-u.ac.jp' + a.get('href')
                self.cur.execute("INSERT INTO miyadai (days, title, url) VALUES (%s, %s, %s)", (_day, _menu, _url))
        self.conn.commit()
        return "success"

    def first_insert_to_img_table(self):
        self.cur.execute("SELECT count(*) FROM miyadai;")
        col_count = self.cur.fetchone()
        print(col_count)
        self.cur.execute("SELECT url FROM miyadai ORDER BY id DESC;")
        for r in range(col_count[0]):
            b = self.cur.fetchone()
            print(b[0])
            self.screen_shot(b[0])

    def get_users(self):
        self.cur.execute("SELECT user_id FROM users")
        rows = self.cur.fetchall()
        return rows

    def oshirase_prints(self, i):
        self.cur.execute("SELECT * FROM miyadai ORDER BY id DESC;")
        sendList = []
        for r in range(i):
            b = self.cur.fetchone()
            sendList2 = [b[1], b[2], b[3]]
            send = "\n".join(sendList2)
            sendList.append(send)
            sendList.append("\n")
        send = " \n".join(sendList)
        return send

    def oshirase_print_once(self, i=0):
        self.cur.execute("SELECT * FROM miyadai WHERE id = (SELECT max(id) FROM miyadai) - %s", (i,))
        b = self.cur.fetchone()
        sendList2 = [b[1], b[2], b[3]]
        send = "\n".join(sendList2)
        return send

    def oshirase_print_once_only_url(self, i=0):
        self.cur.execute("SELECT * FROM miyadai WHERE id = (SELECT max(id) FROM miyadai) - %s", (i,))
        b = self.cur.fetchone()
        send = b[3]
        return send

    def oshirase_print_once_only_title(self, i=0):
        self.cur.execute("SELECT * FROM miyadai WHERE id = (SELECT max(id) FROM miyadai) - %s", (i,))
        b = self.cur.fetchone()
        send = b[2]
        return send

    def oshirase_print_once_only_media_url(self, news_url):
        self.cur.execute("SELECT media_url FROM image_tbl WHERE url = %s", (news_url,))
        b = self.cur.fetchone()
        if not b:
            send = 0
        elif not b[0]:
            send = 0
        else:
            send = b[0]
        return send

    def oshirase_check(self):
        # URLの指定
        html = urllib.request.urlopen("http://gakumu.of.miyazaki-u.ac.jp/gakumu/allnews")
        soup = BeautifulSoup(html, "html.parser")

        # テーブルを指定
        ul = soup.findAll('ul', class_='category-module')

        days = []
        menus = []
        urls = []
        self.cur.execute("SELECT * FROM miyadai ORDER BY id DESC;")
        b = self.cur.fetchone()
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
                self.cur.execute("SELECT count(*) FROM miyadai WHERE url = %s", (urls[r],))
                b = self.cur.fetchone()
                if b[0] == 0:
                    self.cur.execute("INSERT INTO miyadai (days, title, url) VALUES (%s, %s, %s)",
                                     (days[r], menus[r], urls[r]))
        else:
            return 0
        self.conn.commit()
        return i

    def screen_shot(self, screen_url):
        ss = ScreenShot('screen.png')
        ss.set_crop_margin(30)
        ss.screen_shot_crop(url_=screen_url, search_element_name="wrapper2", search_element_type="Id")
        del ss

        pic = open('screen.png', 'rb').read()
        self.cur.execute("INSERT INTO image_tbl (url, image) VALUES (%s, %s)",
                         (screen_url, psycopg2.Binary(pic)))
        self.conn.commit()

    def open_image(self, send_url: str) -> bool:
        self.cur.execute("SELECT image FROM image_tbl WHERE url = %s", (send_url,))
        row = self.cur.fetchone()
        if not row:
            return False

        pic = row[0]
        f = open('send_img.png', 'wb')
        f.write(pic)
        f.close()

        return True


if __name__ == "__main__":
    myzk = MiyadaiDatabaseControl()
    # print(myzk.get_users())
    # print(myzk.oshirase_prints(3))
    # print(myzk.oshirase_print_once(0))
    print(myzk.oshirase_print_once_only_title())
    url = myzk.oshirase_print_once_only_url()
    print(url)
    print(myzk.oshirase_print_once_only_media_url(
        "http://gakumu.of.miyazaki-u.ac.jp/gakumu/andsoon/andsoon/3428-20170613.html"))
    print(myzk.oshirase_print_once_only_media_url(
        "http://gakumu.of.miyazaki-u.ac.jp/gakumu/andsoon/andsoon/700-setuden.html"))
    print(myzk.open_image(url))
    #    print(myzk.oshirase_check())
    myzk.close_connect()
