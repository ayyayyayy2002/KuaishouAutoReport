import time

from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from datetime import datetime
import requests
import sys
import os


proxies = {'http': None, 'https': None}
base_dir = os.path.dirname(os.path.abspath(__file__))
uid_file = os.path.join(base_dir, '附加文件', '运行数据','uid.txt')
log_file = os.path.join(base_dir, '附加文件', '运行记录','错误记录.txt')
title_file = os.path.join(base_dir, '附加文件', '运行记录','标题记录.txt')
script_report = os.path.join(base_dir, '附加文件', '页面脚本', '举报.js')
success_directory = os.path.join(base_dir, '附加文件', '成功验证码')
fail_directory = os.path.join(base_dir, '附加文件', '失败验证码')
user_data_dir = os.path.join(base_dir, '附加文件', 'User Data')
chrome_binary_path = os.path.join(base_dir, '附加文件', 'chrome-win', 'chrome.exe')
chrome_driver_path = os.path.join(base_dir, '附加文件', '运行数据','chromedriver.exe')
os.makedirs(success_directory, exist_ok=True)



def log_error(message):
    with open(log_file, 'a', encoding='utf-8') as log:
        timestamp = datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
        log.write(f"\n\n{timestamp} {message}")


def remove_completed_uid(uid):
    try:
        with open(uid_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        with open(uid_file, 'w', encoding='utf-8') as f:
            for line in lines:
                if line.strip() != uid:
                    f.write(line)
        print(f"删除UID: {uid}")
    except Exception as e:
        print(f"删除UID时发生错误: {e}")


uids = []
with open(uid_file, 'r', encoding='utf-8') as f:  # 以读取模式打开文件
    for line in f:
        line = line.strip()  # 去掉行首尾的空白字符
        if line:  # 如果不是空行，则认为是UID
            uids.append(line)

if not uids:
    print("uid.txt 文件中没有可处理的UID，程序退出")
    log_error("uid.txt 文件中没有可处理的UID，程序退出")
    exit(0)

options = webdriver.ChromeOptions()
options.timeouts = { 'script': 500000 }
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(f'--user-data-dir={user_data_dir}')  # 设置用户数据目录
options.binary_location = chrome_binary_path  # 指定 Chrome 浏览器的可执行文件路径
options.add_argument('--proxy-server="direct://"')
options.add_argument('--proxy-bypass-list=*')
options.add_argument("--disable-gpu")
options.add_argument("--disable-sync")
options.add_argument("disable-cache")#禁用缓存
#options.add_argument("--headless")
options.add_argument('log-level=3')
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)  # 启动 Chrome 浏览器
driver.set_window_size(1000, 700)  # 设置浏览器窗口大小（宽度, 高度）
#driver.set_window_position(-850, 775)  # 设置浏览器窗口位置（x, y）
driver.set_window_position(-850, 1355)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

try:
    for uid in uids:

        try:
            url = f'https://www.kuaishou.com/profile/{uid}'
            print(url)
            driver.get(url)
            remove_completed_uid(uid)
            with open(script_report, "r", encoding="utf-8") as file:
                report = file.read()
            log = driver.execute_async_script(report)
            print(log)
            continue  # 使用 continue 继续下一个 UID
        except Exception as e:
            print(f"UID循环内发生错误,错误UID：{uid}，错误: {e}")
            time.sleep(200000)
            log_error(f"UID循环内发生错误,错误UID：{uid}，错误: {e}")
            sys.exit(f"UID循环内发生错误,错误UID：{uid}")


except Exception as e:
    print(f"从文件获取UID时发生错误,错误: {e}")
    log_error(f"从文件获取UID时发生错误,错误: {e}")
    sys.exit('从文件获取UID时发生错误')


finally:
    driver.quit()
    exit('hsfghsgh')