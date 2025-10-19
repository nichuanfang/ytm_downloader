import subprocess
import os
import shutil
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

os.environ["PYTHONUTF8"] = "1"

def init_env_file(env_path):
    """初始化默认的 .env 文件"""
    default_content = """# cookie文件名
COOKIES_FILE=music.youtube.com_cookies.txt
# 处理好的音频存储的目录
DIST_DIR=dist
# cookies文件的过期时间(小时)
COOKIE_FILE_EXPIRE_TIME=1
"""
    with open(env_path, "w", encoding="utf-8") as f:
        f.write(default_content)
    print(f"已创建默认 .env 文件: {env_path}")

def load_env():
    """加载 .env 文件，如果不存在则初始化"""
    env_path = os.path.join(os.getcwd(), ".env")
    if not os.path.exists(env_path):
        print(".env 文件不存在，正在初始化默认配置...")
        init_env_file(env_path)

    load_dotenv(env_path)
    cookies_file = os.getenv("COOKIES_FILE")
    dist_dir = os.getenv("DIST_DIR")
    cookie_expire_hours = float(os.getenv("COOKIE_FILE_EXPIRE_TIME", "1"))
    os.makedirs(dist_dir, exist_ok=True)
    return cookies_file, dist_dir, cookie_expire_hours

def check_yt_dlp():
    """检查 yt-dlp 是否安装并更新到最新版本"""
    try:
        subprocess.run(["yt-dlp", "--version"], check=True, capture_output=True)
    except FileNotFoundError:
        print("yt-dlp 未安装，正在安装...")
        subprocess.run(["pip", "install", "yt-dlp"], check=True)

    print("检查 yt-dlp 是否为最新版本...")
    subprocess.run(["pip", "install", "-U", "yt-dlp"], check=True)

def check_cookies_file(cookies_file, expire_hours):
    """检查 cookies 文件是否过期"""
    if not os.path.exists(cookies_file):
        print(f"Cookies 文件 {cookies_file} 不存在，请到 https://music.youtube.com 获取并保存。")
        return False

    last_modified = os.path.getmtime(cookies_file)
    expire_time = datetime.fromtimestamp(last_modified) + timedelta(hours=expire_hours)

    if datetime.now() > expire_time:
        print(f"Cookies 文件已过期（>{expire_hours}小时），请前往 https://music.youtube.com 使用插件 'Get cookies.txt LOCALLY' 更新。")
        return False
    return True

def run_command(command):
    """运行命令并返回输出"""
    result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    return result.stdout

def download_audio(url, format_code, cookies_file, dist_dir):
    """下载音频并移动到 dist 文件夹"""
    print(f"开始下载音轨 {format_code} ...")
    cmd = (
        f'yt-dlp --cookies {cookies_file} '
        f'-f {format_code} -x --audio-quality 0 --audio-format m4a '
        f'--add-metadata --embed-thumbnail --no-playlist "{url}"'
    )
    subprocess.run(cmd, shell=True, encoding="utf-8", errors="ignore")

    os.makedirs(dist_dir, exist_ok=True)
    for file in os.listdir(os.getcwd()):
        if file.endswith(".m4a"):
            shutil.move(file, os.path.join(dist_dir, file))
            print(f"已移动文件到: {os.path.join(dist_dir, file)}")

def main():
    check_yt_dlp()
    cookies_file, dist_dir, cookie_expire_hours = load_env()

    while True:
        if not check_cookies_file(cookies_file, cookie_expire_hours):
            input("请更新 cookies 文件后按回车继续...")
            continue

        url = input("请输入音乐 URL (或输入 q 退出): ").strip()
        if url.lower() == "q":
            print("程序结束。")
            break

        print("开始解析...")
        formats_url = f'yt-dlp --cookies {cookies_file} --no-playlist -F "{url}"'
        print(f'解析url：{formats_url}')
        formats_output = run_command(formats_url)
        print('解析完成')
        if "141 " in formats_output:
            download_audio(url, "141", cookies_file, dist_dir)
        else:
            print("该视频不支持 141 音轨。")
            choice = input("是否使用 251 音轨下载？(y/n): ").strip().lower()
            if choice == "y":
                download_audio(url, "251", cookies_file, dist_dir)
            else:
                print("跳过该视频下载。")

if __name__ == "__main__":
    main()
