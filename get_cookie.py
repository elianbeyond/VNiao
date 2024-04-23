# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import shutil


class Driver:
    def __init__(self):
        self.cookie = {}
        self.cookie_str = ''

    def start_driver(self):
        # 设置 WebDriver 路径
        driver_path = './chromedriver-win64/chromedriver.exe'
        service = Service(executable_path=driver_path)
        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        # 创建 WebDriver 实例
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        return driver

    def login(self):
        # 打开网页
        driver = self.start_driver()
        driver.get("https://www.wegame.com.cn/home/")  # 替换为你的实际网页 URL

        # # 等待元素可点击
        # wait = WebDriverWait(driver, 30)  # 最多等待10秒
        # login_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "wglogin")))
        #
        # # 点击登录按钮
        # login_button.click()

        wait = WebDriverWait(driver, 30)  # 最多等待30秒
        wait.until(EC.visibility_of_element_located((By.ID, "wglogin-box")))

        # 转换 cookies 为字符串
        cookies = driver.get_cookies()
        self.cookie = cookies
        self.cookie_str = '; '.join([f"{cookie['name']}={cookie['value']}" for cookie in self.cookie])
        # 关闭浏览器
        driver.close()
        

    def capcha(self):
        driver = self.start_driver()
        try:
            driver.get("https://www.wegame.com.cn/helper/lol/search/index.html")
            if self.cookie:
                for cookie in self.cookie:
                    driver.add_cookie(cookie)

            driver.refresh()

            search_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "search-input"))
            )

            # 发送文本
            search_input.send_keys("向晚Avavaava")

            # 找到搜索按钮并点击
            search_button = driver.find_element(By.CLASS_NAME, "search-submit")
            search_button.click()

            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.ID, "tcaptcha_transform_dy"))
            )  # 最多等待30秒

            WebDriverWait(driver, 30).until(
                EC.invisibility_of_element_located((By.ID, "tcaptcha_transform_dy"))
            ) # 最多等待30秒
        except Exception as e:
            print("发生异常:", e)
        finally:
            # 关闭浏览器
            try:
                driver.close()
            except:
                pass

def get_vniao_cookie():
    # 设置 WebDriver 路径
    driver_path = './chromedriver-win64/chromedriver.exe'
    service = Service(executable_path=driver_path)
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # 创建 WebDriver 实例
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://gt.xzlol.cn")
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "product")))  # 最多等待10秒
    # 转换 cookies 为字符串
    cookies = driver.get_cookies()
    cookie_str = '; '.join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])

    # 关闭浏览器
    driver.close()
    return cookie_str
