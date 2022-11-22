import os.path
import re
import time
import random
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium_stealth import stealth
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class AutoParticipation:
    def __init__(self):
        self.options = webdriver.ChromeOptions()

        self.options.add_argument(r"user-data-dir=D:\User Data")
        self.options.add_argument("--start-maximized")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)

        # don't wait full load of page
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"

        self.driver = webdriver.Chrome(
            options=self.options,
            desired_capabilities=caps
        )
        self.url = 'https://zelenka.guru/forums/contests/'

        stealth(self.driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )
        self.all_contests = []
        self.create_files()
        self.done = []
        self.bad = []

    @staticmethod
    def create_files():
        if not os.path.exists('done.txt'):
            open('done.txt', 'w', encoding='utf-8').close()
        if not os.path.exists('bad.txt'):
            open('bad.txt', 'w', encoding='utf-8').close()

    def get_files_content(self):
        with open('done.txt', 'r', encoding='utf-8') as file:
            self.done = file.read().split('\n')
        with open('bad.txt', 'r', encoding='utf-8') as file:
            self.bad = file.read().split('\n')

    def run(self):
        self.driver.get(f"{self.url}")

    def scroll(self):
        while True:
            src = self.driver.page_source
            soup = BeautifulSoup(src, 'lxml')
            end_label = soup.find('div', class_='AllResultsShowing')
            if 'hidden' in end_label.attrs['class']:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            else:
                break

    def get_all_contests(self):
        src = self.driver.page_source
        # with open('index.html', 'w', encoding='utf-8') as file:
        #     file.write(src)
        # with open('index.html', 'r', encoding='utf-8') as file:
        #     src = file.read()
        soup = BeautifulSoup(src, 'lxml')
        all_contests = soup.find_all('div', class_='discussionListItem')
        for contest in all_contests:
            # contest_link = contest.find('a', class_='listBlock')['href'].split('/')[1]
            contest_id = contest.attrs['id'].replace('thread-', '')
            self.all_contests.append(contest_id)
        print(f'[+] FOUND {len(self.all_contests)} contests')

    def participate(self, contest_id: str):
        url = f'https://zelenka.guru/threads/{contest_id}/'
        self.driver.get(url)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            participate_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'LztContest--Participate')))
            time.sleep(5)
            participate_button.click()
            with open('done.txt', 'a', encoding='utf-8') as file:
                file.write(contest_id + '\n')
            print(f'[+] Принял участие в {url}')
        except:
            with open('bad.txt', 'a', encoding='utf-8') as file:
                file.write(contest_id + '\n')
            print(f'[-] Не можете принять участие в {url}')




if __name__ == '__main__':
    bot = AutoParticipation()
    bot.get_files_content()
    # get all
    bot.run()
    bot.scroll()
    bot.get_all_contests()

    # bot.get_all_contests()

    bad_contest = bot.bad + bot.done
    for contest_id in bot.all_contests:
        if contest_id not in bad_contest:
            bot.participate(contest_id)
            time.sleep(2)
    # time.sleep(100)
