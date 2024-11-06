import logging
import time

from selenium.webdriver.chrome.service import Service

from selenium import webdriver
import requests
import datetime
import shutil
import os


proxies = {'http': None, 'https': None}
output_file = os.path.join(os.getcwd(), '附加文件/运行数据/uid.txt')
keywords_url = 'https://raw.kkgithub.com/ayyayyayy2002/KuaishouAutoReport/main/云端文件/keyword.txt'
keywords_filename = '附加文件/运行数据/keyword.txt'
whitelist_url = 'https://raw.kkgithub.com/ayyayyayy2002/KuaishouAutoReport/main/云端文件/whitelist.txt'
whitelist_filename = '附加文件/运行数据/whitelist.txt'
blacklist_url = 'https://raw.kkgithub.com/ayyayyayy2002/KuaishouAutoReport/main/云端文件/blacklist.txt'
blacklist_filename = '附加文件/运行数据/blacklist.txt'
cloud_whitelist_filename = '云端文件/whitelist.txt'
base_dir = os.path.dirname(os.path.abspath(__file__))
user_data_dir = os.path.join(base_dir, '附加文件', 'User Data')
chrome_binary_path = os.path.join(base_dir, '附加文件', 'chrome-win', 'chrome.exe')
chrome_driver_path = os.path.join(base_dir, '附加文件', '运行数据','chromedriver.exe')
script_search = os.path.join(base_dir, '附加文件', '页面脚本', '获取UID.js')
log_directory = os.path.join(base_dir, '附加文件', '运行记录')
os.makedirs(log_directory, exist_ok=True)
if os.path.exists(output_file):
    os.remove(output_file)
else:
    print(f"文件 {output_file} 不存在，无需删除。")


def fetch_keywords():  # 定义获取关键词的函数

    try:
        response = requests.get(keywords_url, proxies=proxies, timeout=(5, 10))
        if response.status_code == 200:
            with open(keywords_filename, 'wb') as f_out:
                f_out.write(response.content)
            print(f"成功下载关键词文件并保存为keyword")
        else:
            print(f"无法访问URL，状态码：{response.status_code}")
            return load_local_keywords(keywords_filename)  # 返回本地关键词
    except requests.exceptions.RequestException as e:
        print(f"下载关键词文件时发生请求异常：{e}")
        return load_local_keywords(keywords_filename)  # 返回本地关键词

    return load_local_keywords(keywords_filename)





def load_local_keywords(filename):  # 定义从本地文件加载关键词的函数
    keywords = []
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                stripped_line = line.strip()
                if stripped_line and not stripped_line.startswith('#'):  # 排除空行和以“#”开头的行
                    keywords.append(stripped_line)
    else:
        print(f"本地关键词文件不存在。")

    return keywords


def search_and_extract_uid(searchword):
    with open(script_search, "r", encoding="utf-8") as file:
        search = file.read()
    uid_list = driver.execute_async_script(search, searchword)
    process_uid_list(keyword, uid_list)



def process_uid_list(keyword, uid_list):  # 定义处理UID列表的函数（追加写入同一文件）
    print(f" \"{keyword}\" UID：\n", uid_list)

    # 将UID列表追加写入文件
    with open(output_file, 'a', encoding='utf-8') as f:
        f.write(f" \"{keyword}\" UID：\n")
        for uid in uid_list:
            f.write(uid + '\n')
        f.write('\n')  # 添加空行分隔每个关键词的UID列表



unique_uids = set()  # 使用集合存储唯一的 UID
keywords = fetch_keywords()  # 使用fetch_keywords函数替代原有的keywords定义
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(f'--user-data-dir={user_data_dir}')  # 设置用户数据目录
options.binary_location = chrome_binary_path  # 指定 Chrome 浏览器的可执行文件路径
options.add_argument('--proxy-server="direct://"')
options.add_argument('--proxy-bypass-list=*')
options.add_argument("--disable-gpu")
options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 禁用日志

preferences = {
    "webrtc.ip_handling_policy": "disable_non_proxied_udp",
    "webrtc.multiple_routes_enabled": False,
    "webrtc.nonproxied_udp_enabled": False
}
options.add_experimental_option("prefs", preferences)
options.add_argument("--disable-sync")
options.add_argument("disable-cache")  # 禁用缓存
options.add_argument("--headless")
options.add_argument('log-level=3')
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)  # 启动 Chrome 浏览器
# driver.set_window_size(1000, 700)  # 设置浏览器窗口大小（宽度, 高度）
# driver.set_window_position(-850, 775)  # 设置浏览器窗口位置（x, y）
# driver.set_window_position(-850, 1355)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
url = f"https://www.kuaishou.com/"
driver.get(url)


for keyword in keywords:  # 遍历关键词列表，进行搜索和处理
    search_and_extract_uid(keyword)
print('读取当前文件中所有的 UID，并添加到集合中去重')



with open(output_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        uid = line.strip()
        if uid and uid[0].isdigit():  # 检查 uid 是否非空且首字符是否为数字
            unique_uids.add(uid)

try:
    # 获取当前时间并格式化
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = os.path.join(log_directory, f'{timestamp}.txt')

    shutil.copy(output_file, backup_filename)
    print(f"成功保存备份：{backup_filename}")
except IOError as e:
    print(f"复制保存备份时发生错误：{e}")




try:
    response = requests.get(whitelist_url, proxies=proxies, timeout=(5, 10))
    if response.status_code == 200:
        with open(whitelist_filename, 'wb') as f_out:
            f_out.write(response.content)
        print(f"成功下载文件并保存为whitelist")
    else:
        print(f"无法访问URL，状态码：{response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"下载文件时发生请求异常：{e}")
except IOError as e:
    print(f"文件操作发生错误：{e}")
except Exception as e:
    print(f"发生未知错误：{e}")

with open(whitelist_filename, 'r', encoding='utf-8') as f:  # 处理 whitelist_file
    lines = f.readlines()
    for line in lines:
        uid = line.strip()
        if uid and uid[0].isdigit():
            unique_uids.add(uid)





try:
    response = requests.get(blacklist_url, proxies=proxies, timeout=(5, 10))
    if response.status_code == 200:
        with open(blacklist_filename, 'wb') as f_out:
            f_out.write(response.content)
        print(f"成功下载文件并保存为blacklist")
    else:
        print(f"无法访问URL，状态码：{response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"下载文件时发生请求异常：{e}")
except IOError as e:
    print(f"文件操作发生错误：{e}")
except Exception as e:
    print(f"发生未知错误：{e}")

exclude_uids = set()

with open(blacklist_filename, 'r', encoding='utf-8') as exclude_file:
    exclude_lines = exclude_file.readlines()
    for line in exclude_lines:
        exclude_uid = line.strip()
        if exclude_uid.isdigit():  # 假设 UID 是数字格式
            exclude_uids.add(exclude_uid)
unique_uids -= exclude_uids
with open(output_file, 'w', encoding='utf-8') as f:
    for uid in unique_uids:
        f.write(uid + '\n')
print('关键词搜索和UID全部处理完成')
exit(0)
