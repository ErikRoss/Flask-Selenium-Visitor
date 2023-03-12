import json
import logging
import time
import traceback

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


class Browser:
    """
    Объект браузера, выполняющего посещение страницы
    """
    def __init__(self):
        logging.basicConfig(filename='log.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

    @staticmethod
    def start_driver(useragent):
        """
        Установка параметров браузера и его запуск

        :param useragent: user agent пользователя, который будет эмулировать посещение

        :return: webdriver, готовый к дальнейшей работе
        """
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--remote-debugging-port=9222')
        options.add_argument('disable-infobars')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-setuid-sandbox')
        options.add_argument('--disable-web-security')
        options.add_argument('--disable-xss-auditor')
        options.add_argument('--disable-accelerated-2d-canvas')
        options.add_argument('--disable-accelerated-jpeg-decoding')
        options.add_argument('--disable-accelerated-mjpeg-decode')
        options.add_argument('--disable-app-list-dismiss-on-blur')
        options.add_argument('--disable-breakpad')
        options.add_experimental_option("excludeSwitches", ['enable-automation'])
        options.add_argument(f'user-agent={useragent}')
        service = ChromeService(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        return driver

    @staticmethod
    def set_cookies(driver, cookies_data):
        """
        Установка cookies, сохраненных за пользователем

        :param driver: запущенный ранее webdriver
        :param cookies_data: строка с сохранёнными cookies
        """
        driver.delete_all_cookies()
        cookies = json.loads(cookies_data)
        for cookie in cookies:
            driver.add_cookie(cookie)
        time.sleep(5)

    def visit_page(self, user_data, vmc, xcn):
        """
        Посещение страницы пользователем

        :param user_data: объект пользователя
        :param vmc: ключ vmc, полученный при запросе
        :param xcn: ключ xcn, полученный при запросе

        :return: True - посещение успешно выполнено, False - не удалось посетить страницу
        """
        visited = False
        logging.info(f"Got request with vmc: {vmc} and xcn: {xcn}")
        driver = self.start_driver(user_data.useragent)
        logging.info(f"Browser started")
        try:
            driver.get(f"https://{user_data.domain}")
            logging.info(f"Visited main page")
        except Exception:
            logging.critical(f"Got error visiting Main page: {traceback.format_exc()}")
            return False
        url = f"https://{user_data.domain}/MXpPH5?ocs=Bu001xPA20&rma={user_data.rma}&vmc={vmc}" \
              f"&fbclid={user_data.fbclid}&xcn={xcn}&_token={user_data.token}"
        for i in range(5):
            try:
                self.set_cookies(driver, user_data.cookies)
                logging.info(f"Cookies successfully set")
            except Exception:
                logging.critical(f"Got error setting cookies: {traceback.format_exc()}")
                time.sleep(3)
                continue
            try:
                driver.get(url)
                logging.info(f"Target page visited: {url}")
                print("Target page visited")
            except WebDriverException:
                visited = False
                logging.error(f"Error starting Chrome browser: {traceback.format_exc()}")
                print("Error starting Chrome browser")
            else:
                time.sleep(15)
                driver.quit()
                logging.info(f"Browser closed")
                print("Browser closed")
                visited = True
                break
        if visited is False:
            try:
                driver.quit()
            except Exception:
                pass
        return visited


if __name__ == '__main__':
    browser = Browser()
