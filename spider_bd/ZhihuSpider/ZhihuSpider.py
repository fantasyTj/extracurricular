# -*- coding: utf-8  -*-
"""
Module name: ZhihuSpider;
Author: Duguce;
Description: 抓取知乎某一问题下的所有回答（回答数量不超过800左右）
"""

import datetime
import time, json, re
import pandas as pd
import config
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import requests


def get_html(url):
    driver = get_driver(url)
    # 隐式等待
    driver.implicitly_wait(10)
    # 浏览器最大化
    driver.maximize_window()
    driver.get(url)
    time.sleep(random.uniform(1, 2))
    # 定位登录界面关闭按钮
    close_btn = driver.find_element(By.XPATH, "//button[@class='Button Modal-closeButton Button--plain']")
    # 点击登录界面关闭按钮
    close_btn.click()
    scroll_to_bottom(driver)
    answerElementList = driver.find_elements(By.CSS_SELECTOR, "#QuestionAnswers-answers .List-item .ContentItem")
    return answerElementList, driver

def get_user_html(df: pd.DataFrame, start: int):
    driver = get_driver('zhihu')
    # 隐式等待
    driver.implicitly_wait(10)
    # 浏览器最大化
    driver.maximize_window()
    count = 0

    for index, row in df[start: ].iterrows():
        if count >= 20:
            break
        count += 1
        if row['author_url'].split('/')[-1] == '':
            print('匿名')
            continue
        driver.get(row['author_url'])
        
        time.sleep(random.uniform(1, 2))
        # 定位登录界面关闭按钮
        # close_btn = driver.find_element(By.XPATH, "//button[@class='Button Modal-closeButton Button--plain']")
        # # 点击登录界面关闭按钮
        # close_btn.click()
        html = driver.page_source
        match = re.search(r'"ipInfo":"(.*?)"', html)

        if match:
            ip_info = match.group(1)

        if ip_info:
            df.at[index, 'author_ip'] = ip_info
            print(ip_info)
        else:
            print("未获取到ip信息")
        # with open('test.html', 'w', encoding='utf-8') as f:
        #     f.write(html)

    start += count
    driver.close()

    return start


def get_driver(url):
    # 输入需要爬取知乎回答的问题链接
    # url = input('请输入需要爬取知乎回答的问题链接：\n')
    # 禁止图片和CSS加载，减小抓取时间
    binary = FirefoxBinary(r'E:\Mozilla Firefox\firefox.exe')
    firefox_profile = webdriver.FirefoxOptions()
    firefox_profile.set_preference('permissions.default.image', 2)
    firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    firefox_profile.set_preference('permissions.default.stylesheet', 2)
    firefox_profile_dir = r"C:\Users\fantasy\AppData\Roaming\Mozilla\Firefox\Profiles\s4sqirx3.default-release-4"
    profile = webdriver.FirefoxProfile(firefox_profile_dir)
    firefox_profile.profile = profile
    # 打开浏览器
    try:
        s = Service("Driver/geckodriver.exe", log_path='geckodriver.log')
        driver = webdriver.Firefox(firefox_binary=binary, service=s, options=firefox_profile)
    except WebDriverException as e:
        print(f"Error occurred: {e}")
        driver = None
    return driver


def scroll_to_bottom(driver):
    # 获取当前窗口的总高度
    js = 'return action=document.body.scrollHeight'
    # 初始化滚动条所在的高度
    height = 0
    # 当前窗口总高度
    currHeight = driver.execute_script(js)
    # while height < currHeight:
    for _ in range(22):
        # 将滚动条调整至页面底端
        for i in range(height, currHeight, 100):
            driver.execute_script("window.scrollTo(0, {})".format(i))
            time.sleep(0.01)
        height = currHeight
        currHeight = driver.execute_script(js)
        time.sleep(0.2)

def get_ip(author_url):
    namespace = author_url.split('/')[-1]
    url = f'https://www.zhihu.com/api/v4/members/{namespace}'
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39', 
            'cookie': "_zap=58e97bab-ddc6-4ae0-a00c-863cffd8b45c; d_c0=\"AaDfoxbbWhSPTihYZ_Y3UwRFk8OKImNfSlw=|1642474614\"; q_c1=f96d2cd4db46454c883c62ce7fa8baea|1645077465000|1645077465000; _xsrf=3jhFFThvmR1WAcK9joh0G4gJWz8SWAAW; _9755xjdesxxd_=32; YD00517437729195%3AWM_TID=q7KqmwhXnQpFRRAQQReEHEzGqkDeBp3x; gdxidpyhxdE=gsoMo4iv1AqKhvQuwJtaiQzzoHz%2BpBTDm4b5jqiIRXrzL%5CX2aI%2BbqxZ%2BMYXRz6BE51xAw2JpBreJSXvWWI1CrudA1LvON60NXj%2BqvTeZXjeAqg3G9MkUlg9pN6slUAj%2Fz86Djg%2BpYjwq0y4GsBhNXm1RZ2fL4xkdZeic%5CNtDmvs4yZ2M%3A1662257553899; YD00517437729195%3AWM_NI=WARGE4Ak3wgtLFUCgx1mHe5La4wm3QWSels44%2FkAX4Wz4MJyLMC%2BAxIvDLjs%2BKFrStBYC0FESiGOAxSnLeRjLijFQTdCPrvcUl1AyaZMo71CXuMeWhMZ3912XyRLOcghNFU%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eeb4c84d94b8fba4b86e8b928bb7c85b938b9eadd844bc9ea1b5e9219abf88b4f32af0fea7c3b92a959f9ea8c84083b5fd98e680909a9ba4e674f3b38886b848a3ecb98eb25b958dab8df240f8f1a5a2db4095a6fcaec97390938dccc4748baa8cade979e9958a93d28082878dd1c54f91b789b0c47491b28486d16290b7a6a7d460a89da093f56997b4ffa2fc6b9a93a1d8b4499cab8386d6648f86fddab43a9ca79eadce69a5b882a7d837e2a3; z_c0=2|1:0|10:1699874575|4:z_c0|80:MS4xZVJib0JnQUFBQUFtQUFBQVlBSlZUU2J6T0dZZzVNelA1LW1YYW5jSjRqb083MEFBQjBrYTZnPT0=|16dec586b2524b45c85cfaf18d7c387bc6b52d9be3b05c0f928413fc56b01a5b; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1699874576,1700033296,1700212905; SESSIONID=XRbNZ1dukrKvmkwWTTu2IOpMMLzAh2snXY42iQxMp72; JOID=VVAXC0tAbQdGGdT8VE91UhJD35xFFzVvAETqkissEEY6fLiECQozaSwR0fxWbfsU4r_gKVAhOvU89fRxJaHmBys=; osd=U1gXA09GZQdOHdL0VEdxVBpD15hDHzVnBELikiMoFk46dLyCAQo7bSoZ0fRSa_MU6rvmIVApPvM09fx1I6nmDy8=; tst=r; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1701608613; KLBRSID=ed2ad9934af8a1f80db52dcb08d13344|1701608613|1701605860"
        }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response.encoding = 'utf-8'
        ip = response.json().get("ip_info", "IP属地未知")
        return ip
    return "IP属地未知"

def get_answers(answerElementList):
    # 定义一个存储回答中的信息的数据表格
    answerData = pd.DataFrame(
        columns=(
            'question_title', 'answer_url', 'author_name', 'author_url', 'author_ip', 'fans_count', 'created_time', 'updated_time',
            'comment_count',
            'voteup_count', 'content'))
    numAnswer = 0
    # 遍历每一个回答并获取回答中的信息
    for answer in answerElementList:
        # print(answer.get_attribute('outerHTML'))
        dictText = json.loads(answer.get_attribute('data-zop'))
        question_title = dictText['title']  # 问题名称
        answer_url = answer.find_element(By.XPATH,
                                         "meta[@itemprop='url' and contains(@content, 'answer')]").get_attribute(
            'content')  # 获取回答的链接
        author_name = dictText['authorName']  # 回答作者名称
        fans_count = answer.find_element(By.XPATH, "*//meta[contains(@itemprop, 'followerCount')]").get_attribute(
            'content')  # 获取粉丝数量
        created_time = answer.find_element(By.XPATH, "meta[@itemprop='dateCreated']").get_attribute(
            'content')  # 获取回答的创建时间
        updated_time = answer.find_element(By.XPATH, "meta[@itemprop='dateModified']").get_attribute(
            'content')  # 获取回答最近的编辑时间
        comment_count = answer.find_element(By.XPATH, "meta[@itemprop='commentCount']").get_attribute(
            'content')  # 获取该回答的评论数量
        voteup_count = answer.find_element(By.XPATH, "meta[@itemprop='upvoteCount']").get_attribute(
            'content')  # 获取回答的赞同数量
        author_url = answer.find_element(By.XPATH, ".//div[@itemprop='author']//meta[@itemprop='url']").get_attribute(
            'content')  # 获取作者的链接
        # content = answer.find_element(By.TAG_NAME, "span[itemprop='text']").text.replace("\n", "")  # 回答内容
        content = answer.find_element(By.CSS_SELECTOR, "span[itemprop='text']").text.replace("\n", "")  # 回答内容
        time.sleep(0.001)
        row = {'question_title': [question_title],
               'author_name': [author_name],
               'author_url': [author_url],
               'author_ip': [get_ip(author_url)],
               'answer_url': [answer_url],
               'fans_count': [fans_count],
               'created_time': [created_time],
               'updated_time': [updated_time],
               'comment_count': [comment_count],
               'voteup_count': [int(voteup_count)],
               'content': [content]
               }
        answerData = answerData.append(pd.DataFrame(row), ignore_index=True)
        numAnswer += 1
        print(f"[NORMAL] 问题：【{question_title}】 的第 {numAnswer} 个回答抓取完成...")
        time.sleep(0.2)

    answerData.sort_values(by='voteup_count', ascending=False, inplace=True)
    if len(answerData) > 120:
        answerData = answerData[:120]
    return answerData, question_title


if __name__ == '__main__':
    # for url in config.urls:
    #     try:
    #         answerElementList, driver = get_html(url)
    #         print("[NORMAL] 开始抓取该问题的回答...")
    #         answerData, question_title = get_answers(answerElementList)
    #         print(f"[NORMAL] 问题：【{question_title}】 的回答全部抓取完成...")
    #         time.sleep(random.uniform(1, 3))
    #         question_title = re.sub(r'[\W]', '', question_title)
    #         filename = str(f"result-{datetime.datetime.now().strftime('%Y-%m-%d')}-{question_title}")
    #         answerData.to_csv(f'{config.results_path}\{filename}.csv', encoding='utf-8', index=False)
    #         print(f"[NORMAL] 问题：【{question_title}】 的回答已经保存至 {filename}.xlsx...")
    #         time.sleep(random.uniform(1, 3))
    #         driver.close()
    #     except Exception as e:
    #         driver.close()
    #         print(f"[ERROR] 抓取失败... Error: {e}")
    
    df = pd.read_csv('zhihu_result_senta.csv')
    df_len = len(df)
    start = 532
    try :
        while start < df_len:
            start = get_user_html(df, start)
            print('new loop')
        # print(df['author_ip'])
    except Exception as e:
        # driver.close()
        print(f"[ERROR] 抓取失败... Error: {e}")
    # print(df['author_ip'])
    finally: 
        df.to_csv('zhihu_result_senta.csv', index=False, encoding='utf-8')

