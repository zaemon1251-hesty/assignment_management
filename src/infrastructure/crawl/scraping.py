# from datetime import datetime
import os
import time
import traceback
from typing import Dict, List, Optional, Tuple, Union
# from unicodedata import category
from urllib import parse
from pydantic import BaseModel, ValidationError
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException
from src.domain import Assignment
from src.domain.course import Course
from src.usecase.driver.ScrapingDriver import ScrapeDriver
from src.settings import logger

# config
LOGIN_URL = "https://moodle.s.kyushu-u.ac.jp/login/index.php"
TARGET_URL = "https://moodle.s.kyushu-u.ac.jp/my/"
COURSE_URL = "https://moodle.s.kyushu-u.ac.jp/course/view.php?id="
ASSIGNMENT_URL = "https://moodle.s.kyushu-u.ac.jp/mod/assign/view.php?id="

TargetLinkSelector = f'#nav-drawer a[href={TARGET_URL}]'
ItemLimitSelector = 'button[data-action=limit-toggle]'
ToggleCourseSelector = ".dropdown-menu a[data-limit]:last-child"

CourseSelector = "div[data-course-id]"
CategorySelector = "span.categoryname"
SubCategorySelector = "span.text-truncate"
AssignClasses = [
    "activity assign modtype_assign",
    "activity quiz modtype_quiz",
    "activity workshop modtype_workshop"
]
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

        # 遷移予定のリンクを保持
        self.courses_buffer = []
        self.assiginments_buffer = []

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

        print("START SCRAPING")

        t = await self.login_moodle()
        t = await self.move_to_mypage()
        t = await self.show_all_courses()
        crude_cors = await self._run_courses(keywords)
        curde_assis = await self._run_assignments()

        self.driver.quit()

        print("END SCRAPING")

        try:
            for key, crude in curde_assis.items():
                assignments.append(self.parse_assignment(key, crude))
            for key, crude in crude_cors.items():
                courses.append(self.parse_course(key, crude))
        except ValidationError as e:
            traceback.print_exc()
        return assignments, courses

    @classmethod
    def parse_course(cls, course_id: int, crude: crude_course) -> Course:
        course = Course(
            id=course_id,
            title=crude.course_title,
            url=crude.course_url
        )
        return course

    @classmethod
    def parse_assignment(
            cls,
            assignment_id: int,
            crude: crude_assignment) -> Assignment:
        assign = Assignment(
            id=assignment_id,
            title=crude.assignment_title,
            url=crude.url,
            info=crude.info
        )
        return assign

    async def login_moodle(self):
        userid = os.getenv("MOODLE_ID")
        passwd = os.getenv("MOODLE_PASSWORD")

        # moodleにログイン
        if not isinstance(userid, str) or not isinstance(passwd, str):
            raise Exception("moodle id or password not vaild.")
        # 任意のHTMLの要素が特定の状態になるまで待つ
        # ドライバとタイムアウト値を指定
        WebDriverWait(self.driver, 2)
        # ログインページにアクセス
        self.driver.get(LOGIN_URL)
        title_element = self.driver.find_element(By.TAG_NAME, 'title')
        if "Maintenance" in getattr(title_element, "text", ""):
            logger.warning("Now Maintenance...")
            raise Exception("%s now in maintenace" % LOGIN_URL)
        try:
            # ID/PASSを入力
            self.driver.find_element_by_id("username").send_keys(userid)
            self.driver.find_element_by_id("password").send_keys(passwd)
            # ログインボタンをクリック
            self.driver.find_element_by_id("loginbtn").click()
        except Exception:
            raise
        print("Logined in moodle!")
        print("current URL: {}".format(self.driver.current_url))
        return True

    async def move_to_mypage(self) -> None:
        # ログイン後遷移
        self.driver.get(TARGET_URL)
        try:
            if self.driver.current_url != TARGET_URL:
                target_link = self.driver.find_element_by_css_selector(
                    TargetLinkSelector)
                target_link.click()
        except BaseException:
            pass
        WebDriverWait(self.driver, 10) \
            .until(EC.presence_of_all_elements_located)
        time.sleep(2)

    async def show_all_courses(self) -> None:
        """全てのコースを表示する"""
        try:
            print("current URL: {}".format(self.driver.current_url))
            self.driver.find_element_by_css_selector(
                ItemLimitSelector).click()
            time.sleep(2)
            self.driver.find_element_by_css_selector(
                ToggleCourseSelector).click()
        except Exception as e:
            print("FAILED TOGGLE ALL COURSE")
            traceback.print_exc()
            pass
        WebDriverWait(self.driver, 10) \
            .until(EC.presence_of_all_elements_located)
        time.sleep(5)

    async def _extract_courses(self, lecture: Optional[WebElement], defalut_num=0) -> bool:
        """遷移予定の講義ページに移動"""
        try:
            course_href = lecture.find_elements_by_tag_name(
                "a")[0].get_attribute("href")
            lec_id = dict(
                parse.parse_qsl(
                    parse.urlsplit(course_href).query)).get("id", defalut_num)
            self.courses_buffer.append((lec_id, course_href))
            return True
        except Exception:
            print("COULDN'T GET LINK")
            return False

    async def _extract_assignments(self, assign: Optional[WebElement], lec_id=-1, deufault_num=-1):
        """遷移予定の課題ページを保存"""
        try:
            assign_href = assign.find_elements_by_tag_name(
                "a")[0].get_attribute("href")
            assignment_id = dict(
                parse.parse_qsl(
                    parse.urlsplit(assign_href).query)).get('id', deufault_num)
            self.assiginments_buffer.append(
                (lec_id, assignment_id, assign_href))

        except Exception:
            print("COUDN'T GET ASSIGNMENT LINK")

    def _get_category(
            self, element: Optional[WebElement], keywords: List[str] = None) -> Union[str, None]:
        """カテゴリを抽出する"""
        category = ''
        try:
            category = element.find_elements_by_css_selector(
                CategorySelector)[0].text
        except Exception:
            pass

        # カテゴリ（年別や期間など）で条件に合うものだけを探す
        conditions = True  # any(key in category for key in keywords)
        if not conditions:
            print(
                "this category:{} doesn't match the keywords:{}".format(
                    category, keywords))
            return None
        return category

    async def _insert_crude_course(self, course_href, lec_id, lectures):
        """講義ページからタイトルなどをスクレイピングして講義情報を作成する
        その後、配列に格納する"""
        lec_title = self.driver.find_element(
            By.TAG_NAME, "h1").text
        print("コース名: %s" % lec_title)
        print("current URL: {}".format(self.driver.current_url))

        # コースの保存
        try:
            lectures[int(lec_id)] = crude_course(
                course_title=lec_title,
                course_url=course_href
            )
            print("A COURSE GOT")
        except Exception as e:
            traceback.print_exc()
            print("A COURSE MISSED", [lec_id, lec_title, course_href])

    async def _insert_crude_assignment(self, assign_href, assignment_id, lec_id, assignments):
        """課題ページからタイトルなどをスクレイピングして課題情報を作成する
        その後、配列に格納する"""
        # コース名と課題名をゲットする
        assign_title = self.driver.find_element(
            By.TAG_NAME, "h2").text
        print("課題名: %s" % assign_title)
        WebDriverWait(self.driver, 10)
        # 情報をゲットする
        info = ''
        try:
            info = self.driver.find_element_by_css_selector(
                "td.cell,td.c1,td.lastcol").text
        except Exception:
            pass

        # 課題の保存
        try:
            assignments[int(assignment_id)] = crude_assignment(
                course_id=int(lec_id),
                assignment_title=assign_title,
                info=info,
                url=assign_href,
            )
            print("AN ASSIGNMENT GOT")
        except Exception:
            print("AN ASSIGNMENT MISSED")

    async def _run_courses(self, keywords) -> Dict[int, crude_course]:
        # 全コース取得
        courses: List[WebElement] = self.driver.find_elements_by_css_selector(
            CourseSelector)
        print("全コース数: %s" % len(courses))

        for i, lecture in enumerate(courses):

            if not self._get_category(lecture, keywords=keywords):
                continue
            if not self._extract_courses(lecture=lecture, defalut_num=i):
                continue

        lectures: Dict[int, crude_course] = {}

        while (self.courses_buffer):
            lec_id, course_href = self.courses_buffer.pop()

            # コース情報ページへ遷移
            self.driver.get(course_href)
            time.sleep(5)

            await self._insert_crude_course(course_href, lec_id, lectures)

            # コースにひもつく課題の取得
            assigns: List[WebElement] = self.driver.find_elements_by_css_selector(
                ",".join(AssignClasses))
            print("このページの課題数: %s" % len(assigns))

            # 課題のスクレイピング
            for j, assign in enumerate(assigns):
                self._extract_assignments(
                    assign=assign, lec_id=lec_id, deufault_num=j)
        return lectures

    async def _run_assignments(self) -> Dict[int, crude_assignment]:
        assignments: Dict[int, crude_assignment] = {}

        while (self.assiginments_buffer):
            lec_id, assignment_id, assign_href = self.assiginments_buffer.pop()

            # 課題情報ページに遷移
            self.driver.get(assign_href)
            time.sleep(5)
            print("current URL: {}".format(self.driver.current_url))

            await self._insert_crude_assignment(assign_href, assignment_id, lec_id, assignments)

        return assignments


if __name__ == '__main__':
    sd = ScrapeDriverImpl()
    sd.run().close()
