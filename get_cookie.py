# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import shutil
import datetime
from VNiao import domain
from WeGame import cookie_str_to_dict


class Driver:
    def __init__(self):
        self.cookie = {}
        self.cookie_str = ''
        self.file_name = 'wegame_cookies.txt'
        today = datetime.date.today().isoformat()

        try:
            date_str, self.cookie_str = self.read_data(self.file_name)
        except FileNotFoundError:
            date_str, self.cookie_str = None, None

        if not date_str or date_str != today:
            self.login()
        self.cookie = cookie_str_to_dict(self.cookie_str)
    def write_data(self, filename, data):
        today = datetime.date.today().isoformat()
        with open(filename, 'w') as file:
            file.write(f"{today}\n{data}")

    def read_data(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            if not lines or len(lines) < 2:
                return None, None
            date_str = lines[0].strip()
            data_str = lines[1].strip()
            return date_str, data_str

    def start_driver(self):
        # 设置 WebDriver 路径
        driver_path = './chromedriver-win64/chromedriver.exe'
        service = Service(executable_path=driver_path)
        chrome_options = Options()
        user_data_dir = r"user-data-dir=C:\Users\QingYuAn\Desktop\VniaoHelper\VNiao\chromedriver-win64\cache"
        chrome_options.add_argument(user_data_dir)
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

        self.write_data(self.file_name, self.cookie_str)

        # 关闭浏览器
        driver.close()

    def capcha(self):
        driver = self.start_driver()
        try:
            driver.get("https://www.wegame.com.cn/helper/lol/search/index.html")
            print("已打开网页")

            if self.cookie:
                print("开始添加cookie")
                for cookie_dict in self.cookie:
                    if 'value' in cookie_dict:  # 确保有value字段
                        # 创建一个只包含必要字段的新字典
                        cookie_to_add = {
                            'name': cookie_dict['name'],
                            'value': cookie_dict['value'],
                            # 如果需要的话，也可以添加domain等其他字段
                            # 'domain': cookie_dict.get('domain', ''),
                            # 'path': cookie_dict.get('path', '/'),
                            # ... 其他可能需要的字段
                        }
                        driver.add_cookie(cookie_to_add)
                    else:
                        print(f"Skipping cookie with name {cookie_dict['name']} because it has no value.")
                print("已添加cookie")

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
            )  # 最多等待5秒

            WebDriverWait(driver, 30).until(
                EC.invisibility_of_element_located((By.ID, "tcaptcha_transform_dy"))
            )  # 最多等待30秒
        except Exception as e:
            print("验证码消失发生异常:", e)
        finally:
            # 关闭浏览器
            try:
                driver.close()
                print("已关闭浏览器")
            except Exception as close_exception:
                print("关闭浏览器时发生异常:", close_exception)

def get_vniao_cookie():
    # 设置 WebDriver 路径
    driver_path = './chromedriver-win64/chromedriver.exe'
    service = Service(executable_path=driver_path)
    chrome_options = Options()
    user_data_dir = r"user-data-dir=C:\Users\QingYuAn\Desktop\VniaoHelper\VNiao\chromedriver-win64\cache"
    chrome_options.add_argument(user_data_dir)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    # 创建 WebDriver 实例
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.get(f"https://{domain}")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "card-title"))
    )  # 最多等待10秒
    # 转换 cookies 为字符串
    cookies = driver.get_cookies()
    cookie_str = '; '.join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])

    # 关闭浏览器
    driver.close()
    return cookie_str
