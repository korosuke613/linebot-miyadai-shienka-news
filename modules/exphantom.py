from PIL import Image
from selenium import webdriver


class ScreenShot:
    def __init__(self, file_name_: str = "screenshot.png"):
        """
        :type file_name_: str
        """
        self._filename = file_name_
        self._driver = webdriver.PhantomJS()
        self._driver.set_window_size(1024, 768)
        self._crop_margin = 0

    def screen_shot(self, url_: str) -> bool:
        """
        Take a screenshot of the specified url.
        :return: Success is True, Fail is False
        :param url_: the webpage to save screenshot
        """
        try:
            self._driver.get(url_)
            self._driver.save_screenshot(self._filename)
        except Exception as e:
            print(e)
            return False
        return True

    def screen_shot_crop(self, url_: str, search_element_name: str, search_element_type: str = "Id") -> bool:
        """
        Take a screenshot of the specified class of the specified url destination.
        :return: Success is True, Fail is False
        :param url_: the webpage to save screenshot
        :param search_element_name: search to element name
        :param search_element_type: search to element type
        """
        self.screen_shot(url_)
        before_script = """
                        var element = document.getElementBy""" + search_element_type + "('" + search_element_name + """');
                        var rect = element.getBoundingClientRect(); 
                        """
        try:
            left = self._driver.execute_script(before_script + "return rect.left;") - self._crop_margin
            top = self._driver.execute_script(before_script + "return rect.top;")
            right = self._driver.execute_script(before_script + "return rect.width;") + left + self._crop_margin
            bottom = self._driver.execute_script(before_script + "return rect.height;") + top + self._crop_margin
        except Exception as e:
            print(e)
            return False
        im = Image.open(self._filename)
        im = im.crop((left, top, right, bottom))
        im.save(self._filename)
        im.close()
        return True

    def set_file_name(self, filename_: str):
        self._filename = filename_

    def set_window_size(self, width_: int, height_: int):
        self._driver.set_window_size(width=width_, height=height_)

    def get_window_size(self) -> object:
        return self._driver.get_window_size()

    def set_crop_margin(self, crop_margin_: int):
        self._crop_margin = crop_margin_

    def ger_crop_margin(self) -> object:
        return self._crop_margin

    def __del__(self):
        self._driver.close()


if __name__ == "__main__":
    # スクリーンショットを撮るURLを指定
    screen_url = "http://gakumu.of.miyazaki-u.ac.jp/gakumu/campuslifeinfo/campuslifeinfo/3470-2017-07-06-07-36-07.html"
    # クロップする要素の属性を指定
    element_type = "Id"
    # クロップする要素名を指定
    element_name = "wrapper2"
    # インスタンスを生成するときに保存先ファイル名を指定
    ss = ScreenShot("screenshot.png")
    # screen_urlのスクリーンショットを保存
    ss.screen_shot(screen_url)
    # 保存先ファイル名を変更
    ss.set_file_name("screenshot_crop.png")
    # screen_urlのelement_type属性のelement_nameという要素のスクリーンショットを保存
    ss.screen_shot_crop(screen_url, element_name, element_type)
    # インスタンスの削除
    del ss
