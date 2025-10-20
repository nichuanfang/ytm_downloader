import subprocess
import os
import shutil
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests

from util import Logger, check_cookies_file  # 新增，用于检测网络

os.environ["PYTHONUTF8"] = "1"

# ======= 初始化 .env =======
def init_env_file(env_path):
    default_content = """# cookie文件名
COOKIES_FILE=music.youtube.com_cookies.txt
# 处理好的音频存储的目录
DIST_DIR=dist
# cookies文件的过期时间(分钟)
COOKIE_FILE_EXPIRE_TIME=20
# cookiecloud地址
COOKIE_CLOUD_URL=URL
# 用户唯一ID
COOKIE_CLOUD_UUID=UUID
# 用户key
COOKIE_CLOUD_KEY=KEY
"""
    with open(env_path, "w", encoding="utf-8") as f:
        f.write(default_content)
    Logger.success(f"已创建默认 .env 文件: {env_path}")

def load_env():
    env_path = os.path.join(os.getcwd(), ".env")
    if not os.path.exists(env_path):
        Logger.warning(".env 文件不存在，正在初始化默认配置...")
        init_env_file(env_path)

    load_dotenv(env_path)
    cookies_file = os.getenv("COOKIES_FILE")
    dist_dir = os.getenv("DIST_DIR")
    cookie_expire_minutes = float(os.getenv("COOKIE_FILE_EXPIRE_TIME", "20"))
    os.makedirs(dist_dir, exist_ok=True)
    cookiecloud_url = os.getenv("COOKIE_CLOUD_URL")
    cookiecloud_uuid = os.getenv("COOKIE_CLOUD_UUID")
    cookiecloud_key = os.getenv("COOKIE_CLOUD_KEY")
    return cookies_file, dist_dir, cookie_expire_minutes, cookiecloud_url, cookiecloud_uuid, cookiecloud_key

# ======= 检查 yt-dlp =======
def check_yt_dlp():
    try:
        subprocess.run(["yt-dlp", "--version"], check=True, capture_output=True)
        Logger.success("yt-dlp 已安装")
    except FileNotFoundError:
        Logger.warning("yt-dlp 未安装，正在为您安装...")
        subprocess.run(["pip", "install", "yt-dlp"], check=True)

    Logger.info("检查 yt-dlp 是否为最新版本...")
    subprocess.run(["pip", "install", "-U", "yt-dlp"], check=True)
    Logger.success("yt-dlp 已更新到最新版本")

# ======= 检查 YouTube 连接 =======
def check_youtube_connection():
    Logger.info("正在检测 YouTube 网络连接...")
    test_url = "https://www.youtube.com"
    try:
        start_time = time.time()
        response = requests.get(test_url, timeout=5)
        latency = (time.time() - start_time) * 1000  # 毫秒
        if response.status_code == 200:
            Logger.success(f"YouTube 连接正常 ✅ 延迟: {latency:.2f} ms")
            return True
        else:
            Logger.error(f"YouTube 返回异常状态码: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        Logger.error(f"无法连接 YouTube，请检查网络或代理设置。\n错误信息: {e}")
        return False

# ======= 执行命令 =======
def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    return result.stdout

# ======= 下载音频 =======
def download_audio(url, format_code, cookies_file, dist_dir):
    Logger.info(f"开始下载音轨 {format_code} ...")
    cmd = (
        f'yt-dlp --cookies {cookies_file} '
        f'-f {format_code} -x --audio-quality 0 --audio-format m4a '
        f'--add-metadata --embed-thumbnail --no-playlist "{url}"'
    )
    subprocess.run(cmd, shell=True, encoding="utf-8", errors="ignore")
    move_downloaded_files(dist_dir)

def download_soundcloud(url, dist_dir):
    Logger.info("检测到 SoundCloud 链接，使用专用命令下载（无需 Cookies）...")
    cmd = f'yt-dlp -x --audio-quality 0 --audio-format m4a --add-metadata --embed-thumbnail --no-playlist "{url}"'
    subprocess.run(cmd, shell=True, encoding="utf-8", errors="ignore")
    move_downloaded_files(dist_dir)

def move_downloaded_files(dist_dir):
    os.makedirs(dist_dir, exist_ok=True)
    moved_files = []
    for file in os.listdir(os.getcwd()):
        if file.endswith(".m4a"):
            shutil.move(file, os.path.join(dist_dir, file))
            moved_files.append(file)
    if moved_files:
        Logger.success(f"已移动文件到 {dist_dir}: {', '.join(moved_files)}")
    else:
        Logger.warning("未找到下载的音频文件，请检查 URL 是否正确。")

# ======= 主程序 =======
def main():
    Logger.info("🎵 音乐下载助手启动中...")
    
    # 检查 YouTube 网络连接
    if not check_youtube_connection():
        Logger.warning("YouTube 网络不可用，可能无法下载 YouTube 音乐。")
        
    # 检查 yt-dlp
    check_yt_dlp()
    
    cookies_file, dist_dir, cookie_expire_minutes, cookiecloud_url, cookiecloud_uuid, cookiecloud_key = load_env()
    
    # cookiecloud初始化 如果cookiecloud_url是有效URL 将获取cookiecloud服务器上的cookie 写入文件{cookies_file}中
    from cookiecloud import initCookieCloud,refreshCookie
    init_res = initCookieCloud(cookiecloud_url, cookiecloud_uuid,
                    cookiecloud_key, cookies_file,cookie_expire_minutes)
    if init_res:
        Logger.success("✨ cookiecloud初始化完成!")
    
    while True:
        url = input("\n请输入音乐 URL (或输入 q 退出): ").strip()
        if url.lower() == "q":
            Logger.info("程序已退出，再见！👋")
            break

        # SoundCloud 专用逻辑
        if "soundcloud.com" in url.lower():
            download_soundcloud(url, dist_dir)
            continue

        # YouTube Music 逻辑
        if not check_cookies_file(cookies_file, cookie_expire_minutes):
            if init_res:
                refreshCookie(cookiecloud_url, cookiecloud_uuid,
                                cookiecloud_key, cookies_file)
                Logger.success("⚡️cookies文件过期,已重新刷新cookie")
            else:
                choice = input("是否已导出cookies文件？(y/n): ").strip().lower()
                if choice == "n":
                    Logger.info("已跳过该视频下载。")
                    continue
                else:
                    #检测生成的文件是否存在
                    if not os.path.exists(cookies_file):
                        Logger.error("未找到cookie文件,已跳过该视频下载。")
                        continue
                    

        Logger.info("开始解析音轨信息，请稍候...")
        formats_url = f'yt-dlp --cookies {cookies_file} --no-playlist -F "{url}"'
        formats_output = run_command(formats_url)
        Logger.success("音轨解析完成！")

        if "141 " in formats_output:
            download_audio(url, "141", cookies_file, dist_dir)
        else:
            Logger.warning("该视频不支持 141 音轨。")
            choice = input("是否使用 251 音轨下载？(y/n): ").strip().lower()
            if choice == "y":
                download_audio(url, "251", cookies_file, dist_dir)
            else:
                Logger.info("已跳过该视频下载。")

if __name__ == "__main__":
    main()
