import os
import time
import re
from typing import Dict, List, Optional, Tuple
from urllib import parse
from bs4 import BeautifulSoup, ResultSet
from pydantic import BaseModel, ValidationError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, NoSuchWindowException
from src.domain import assignment
from src.domain.assignment import Assignment
from src.domain.course import Course
from src.usecase.driver.ScrapingDriver import ScrapeDriver
from src.settings import logger

# config
LOGIN_URL = "https://moodle.s.kyushu-u.ac.jp/login/index.php"
TARGET_URL = "https://moodle.s.kyushu-u.ac.jp/my/"
waitSelector = "#page-container-0 > div > div > div > a"
Selector = "div[id^=course-info-container] > div > div.w-100.text-truncate"
CategorySelector = "div > span.categoryname.text-truncate"
SubCategorySelector = "div > span.text-truncate"
AssignClasses = [
    "activity assign modtype_assign",
    "activity quiz modtype_quiz",
    "activity workshop modtype_workshop"]
date_pattern = r'([12]\d{3}[/\-年])?\s?(0?[1-9]|1[0-2])[/\-月]\s?(0?[1-9]|[12][0-9]|3[01])日?'
end_pattern = ['終了', '終了日時', '〆切']


class crude_course(BaseModel):
    course_title: str
    course_url: str


class crude_assignment(BaseModel):
    course_id: int
    assignment_title: str
    info: Optional[str]
    url: str


class ScrapeDriverImpl(ScrapeDriver):
    """moodleからスクレイピングするためのドライバー

    Args:
        ScrapeDriver (_type_): _description_
    """

    def __init__(self):
        # Selenium サーバーへ接続する。
        options = Options()
        options.add_experimental_option("w3c", False)
        self.driver = webdriver.Remote(
            command_executor=os.environ["SELENIUM_URL"],
            desired_capabilities=DesiredCapabilities.CHROME.copy(),
            options=options
        )

    class wait_for_all(object):
        """ターゲットが出現するまで待つ
            # 使い方
            # methods = []
            # for AssignClass in AssignClasses:
            #     methods.append(EC.presence_of_element_located((By.CLASS_NAME, AssignClass)))
            # method = wait_for_all(methods)
            # wait = WebDriverWait(driver, 10).until(method)
        """

        def __init__(self, methods):
            self.methods = methods

        def __call__(self, driver):
            try:
                for method in self.methods:
                    if not method(driver):
                        return False
                return True
            except StaleElementReferenceException:
                return False

    async def run(self, keywords: List[str] = []) -> Tuple[List[Assignment], List[Course]]:
        assignments: List[Assignment] = []
        courses: List[Course] = []
        moodle_id = os.getenv("MOODLE_ID")
        moodle_password = os.getenv("MOODLE_PASSWORD")
        try:
            curde_assis, crude_cors = await self.get_assignments(moodle_id, moodle_password, keywords)
            for key, crude in curde_assis.items():
                assignments.append(self.parse_assignment(key, crude))
            for key, crude in crude_cors.items():
                assignments.append(self.parse_course(key, crude))
        except ValidationError as e:
            logger.warning(e.json())
        # except Exception as e:
        #     logger.error(e)
        return assignments, courses

    def parse_course(course_id: int, crude: crude_course) -> Course:
        course = Course(
            course_id,
            crude.course_title,
            crude.course_url
        )
        return course

    def parse_assignment(assignment_id: int,
                         crude: crude_assignment) -> Assignment:
        assign = Assignment(
            assignment_id,
            crude.assignment_title,
            crude.assignment_title,
            crude.info
        )
        return assign

    async def login(self, url: str, mid: str, passwd: str):
        if not isinstance(mid, str) or not isinstance(passwd, str):
            raise Exception("moodle id or password not vaild.")
        # 任意のHTMLの要素が特定の状態になるまで待つ
        # ドライバとタイムアウト値を指定
        WebDriverWait(self.driver, 2)
        # ログインページにアクセス
        self.driver.get(url)
        title_element = self.driver.find_element(By.TAG_NAME, 'title')
        if "Maintenance" in getattr(title_element, "text", ""):
            logger.warning("Now Maintenance...")
            raise Exception("%s now in maintenace" % url)
        # ID/PASSを入力
        print([mid, passwd])
        id_element = self.driver.find_element_by_id("username")
        id_element.send_keys(mid)
        password_element = self.driver.find_element_by_id("password")
        try:
            id_element.send_keys(mid)
            password_element.send_keys(passwd)
            time.sleep(1)
            # ログインボタンをクリック
            login_button = self.driver.find_element_by_id("loginbtn")
            login_button.click()
        except Exception:
            raise

    async def get_assignments(self, userid: str, passwd: str, keywords: List[str] = ["2021"]) -> Tuple[Dict[int, crude_assignment], Dict[int, crude_course]]:
        """
        moodleのページからコースと課題を取ってくる
        params:
        userid -> int
        passwd -> int
        keywords -> list(string)
        keywords: ゲットしたい課題のタグの条件
        """
        # 保存するデータを格納する
        lectures: Dict[int, crude_course] = {}
        assignments: Dict[int, crude_assignment] = {}
        lec_cnt = 0

        res = await self.login(LOGIN_URL, userid, passwd)
        # ログイン後遷移
        self.driver.get(TARGET_URL)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, waitSelector))
        )

        # BeautifulSoup
        soup = BeautifulSoup(
            self.driver.page_source.encode('utf-8'),
            features="html.parser")
        courses: ResultSet = soup.select(Selector)
        logger.info("全コース数: %s" % len(courses))

        for lecture in courses:
            # カテゴリを抽出する
            category = ''
            if lecture.select_one(CategorySelector):
                category = lecture.select_one(CategorySelector).string
            elif lecture.select_one(SubCategorySelector):
                category = lecture.select_one(SubCategorySelector).string

            # カテゴリ（年別や期間など）で条件に合うものだけを探す
            conditions = any(key in category for key in keywords)
            if not conditions:
                continue

            # ターゲットの講義の課題情報を取り出す
            course_href = lecture.findAll("a")[0].get("href")
            param = dict(parse.parse_qsl(parse.urlsplit(course_href).query))
            lec_id = param['id']
            self.driver.get(course_href)
            WebDriverWait(self.driver, 10)
            # BeautifulSoup
            assigns_soup = BeautifulSoup(
                self.driver.page_source.encode('utf-8'),
                features="html.parser")
            assigns = assigns_soup.find_all("li", class_=AssignClasses)
            logger.info("このページの課題数: %s" % len(assigns))

            for assign in assigns:
                lec_cnt += 1
                logger.info("%s 個目の課題が見つかりました" % lec_cnt)

                # 課題があるページに移動
                assign_href = assign.findAll("a")[0].get("href")
                param = dict(
                    parse.parse_qsl(
                        parse.urlsplit(assign_href).query))
                assignment_id = param['id']
                self.driver.get(assign_href)

                # コース名と課題名をゲットする
                lec_title = self.driver.find_element(
                    By.TAG_NAME, "h1").text
                assign_title = self.driver.find_element(
                    By.TAG_NAME, "h2").text
                logger.info("コース名: %s" % lec_title)
                logger.info("課題名: %s" % assign_title)
                WebDriverWait(self.driver, 10)
                last_soup = BeautifulSoup(
                    self.driver.page_source, features="html.parser")

                # 締切時間をゲットする
                info = ''
                if last_soup.find("td", class_="cell c1 lastcol"):
                    info = last_soup.find(
                        "td", class_="cell c1 lastcol").string
                if not re.match(date_pattern, info):
                    dates = last_soup.find_all(re.compile(date_pattern))
                    for date in dates:
                        if any(ptn in date.string for ptn in end_pattern):
                            info = date.string
                    else:
                        info = None

                # データ格納
                assignments[int(assignment_id)] = crude_assignment(
                    int(lec_id),
                    assign_title,
                    info,
                    assign_href,
                )
                lectures[int(lec_id)] = crude_course(
                    lec_title,
                    course_href,
                )

        self.driver.quit()
        return assignments, lectures


if __name__ == '__main__':
    sd = ScrapeDriverImpl()
    sd.run()
