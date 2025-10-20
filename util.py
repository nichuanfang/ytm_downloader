import subprocess
import os
import shutil
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests  # 新增，用于检测网络

# ======= 颜色和日志工具 =======
class Logger:
    INFO = "\033[94m[INFO]\033[0m"
    SUCCESS = "\033[92m[SUCCESS]\033[0m"
    WARNING = "\033[93m[WARNING]\033[0m"
    ERROR = "\033[91m[ERROR]\033[0m"

    @staticmethod
    def info(msg): print(f"{Logger.INFO} {msg}")
    @staticmethod
    def success(msg): print(f"{Logger.SUCCESS} {msg}")
    @staticmethod
    def warning(msg): print(f"{Logger.WARNING} {msg}")
    @staticmethod
    def error(msg): print(f"{Logger.ERROR} {msg}")

# ======= 检查 Cookies 文件 =======
def check_cookies_file(cookies_file, expire_minutes=20):
    if not os.path.exists(cookies_file):
        Logger.error(
            f"Cookies 文件 {cookies_file} 不存在，请到 https://music.youtube.com 获取并保存。")
        return False

    last_modified = os.path.getmtime(cookies_file)
    expire_time = datetime.fromtimestamp(
        last_modified) + timedelta(minutes=expire_minutes)

    if datetime.now() > expire_time:
        Logger.warning(f"Cookies 文件已过期（>{expire_minutes}分钟）")
        return False
    Logger.success("Cookies 文件有效")
    return True

# ======= Cookiecloud检查 Cookies 文件 =======
def cc_check_cookies_file(cookies_file, expire_minutes=20):
    if not os.path.exists(cookies_file):
        return True

    last_modified = os.path.getmtime(cookies_file)
    expire_time = datetime.fromtimestamp(
        last_modified) + timedelta(minutes=expire_minutes)
    if datetime.now() > expire_time:
        return True
    return False
