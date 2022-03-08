import os
import time
import re
from urllib import parse
from bs4 import BeautifulSoup, ResultSet
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, NoSuchWindowException


class wait_for_all(object):
    # ターゲットが出現するまで待つ
    # 使い方
    # methods = []
    # for AssignClass in AssignClasses:
    #     methods.append(EC.presence_of_element_located((By.CLASS_NAME, AssignClass)))
    # method = wait_for_all(methods)
    # wait = WebDriverWait(driver, 10).until(method)
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


def get_assignments(userid='', passwd='', keywords=["2021"]):
    """
    moodleのページからコースと課題を取ってくる
    params:
    userid -> int
    passwd -> int
    keywords -> list(string)
    keywords: ゲットしたい課題のタグの条件
    """
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
    # Selenium サーバーへ接続する。
    driver = webdriver.Remote(
        command_executor=os.environ["SELENIUM_URL"],
        desired_capabilities=DesiredCapabilities.CHROME.copy()
    )
    # 任意のHTMLの要素が特定の状態になるまで待つ
    # ドライバとタイムアウト値を指定
    WebDriverWait(driver, 10)
    # ログインページにアクセス
    driver.get(LOGIN_URL)
    if "Maintenance" in driver.find_element(By.TAG_NAME, 'title').text:
        print("Now Maintenance...")
        return {}, {}
    # ID/PASSを入力
    id = driver.find_element_by_id("username")
    id.send_keys(userid)
    password = driver.find_element_by_id("password")
    password.send_keys(passwd)
    time.sleep(1)
    # ログインボタンをクリック
    login_button = driver.find_element_by_id("loginbtn")
    login_button.click()

    # ログイン後遷移
    driver.get(TARGET_URL)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, waitSelector))
    )
    # BeautifulSoup
    soup = BeautifulSoup(
        driver.page_source.encode('utf-8'),
        features="html.parser")
    courses: ResultSet = soup.select(Selector)
    print("全コース数: %s" % len(courses))
    # 保存するデータを格納する
    lectures = {}
    assignments = {}
    lec_cnt = 0
    for lecture in courses:
        # カテゴリを抽出する
        if lecture.select_one(CategorySelector):
            category = lecture.select_one(CategorySelector).string
        elif lecture.select_one(SubCategorySelector):
            category = lecture.select_one(SubCategorySelector).string
        else:
            category = 'None'

        # カテゴリ（年別や期間など）で条件に合うものだけを探す
        conditions = any(key in category for key in keywords)
        if conditions:
            href = lecture.findAll("a")[0].get("href")
            param = dict(parse.parse_qsl(parse.urlsplit(href).query))
            lec_id = param['id']
            print()
            # ターゲットの講義の課題情報を取り出す
            driver.get(href)
            WebDriverWait(driver, 10)
            # BeautifulSoup
            assigns_soup = BeautifulSoup(
                driver.page_source.encode('utf-8'),
                features="html.parser")
            assigns = assigns_soup.find_all("li", class_=AssignClasses)
            print("このページの課題数: %s" % len(assigns))
            for assign in assigns:
                lec_cnt += 1
                print(" %s 個目の課題が見つかりました" % lec_cnt)
                # 課題があるページに移動
                assign_href = assign.findAll("a")[0].get("href")
                param = dict(
                    parse.parse_qsl(
                        parse.urlsplit(assign_href).query))
                assignment_id = param['id']
                driver.get(assign_href)
                # コース名と課題名をゲットする
                lec_title = driver.find_element(By.TAG_NAME, "h1").text
                assign_title = driver.find_element(By.TAG_NAME, "h2").text
                print("コース名: ", lec_title)
                print("課題名: ", assign_title)
                wait = WebDriverWait(driver, 10)
                last_soup = BeautifulSoup(
                    driver.page_source, features="html.parser")
                # 締切時間をゲットする
                end_at = ''
                if last_soup.find("td", class_="cell c1 lastcol"):
                    end_at = last_soup.find(
                        "td", class_="cell c1 lastcol").string
                if not re.match(date_pattern, end_at):
                    dates = last_soup.find_all(re.compile(date_pattern))
                    for date in dates:
                        if any(ptn in date.string for ptn in end_pattern):
                            end_at = date.string
                    else:
                        end_at = None
                lectures[int(lec_id)] = {
                    "course_title": lec_title,
                    "course_url": href,
                }
                assignments[int(assignment_id)] = {
                    "course_id": int(lec_id),
                    "assignment_title": assign_title,
                    "info": end_at,
                    "assignment_url": assign_href,
                }

    driver.quit()
    return lectures, assignments


if __name__ == '__main__':
    print(*get_assignments(), sep="\n")
