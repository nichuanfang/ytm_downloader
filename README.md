# 🎵 Music Downloader for **YouTube Premium**
> 一款简洁高效的音乐下载工具，支持 YouTube Premium & SoundCloud，让你轻松保存喜爱的音频！  

---

## 🚀 前置条件（Prerequisites）
- 🐍 **Python** 3.8+（必须安装在本地）
- 🌍 **魔法上网环境**（用于访问相关服务）

---

## 📥 使用指南（How to Use）
1. **首次运行初始化**  
   直接打开可执行文件，自动生成 `.env` 配置文件并创建音频存放目录。  
   
2. **自定义配置**  
   根据需求修改 `.env` 文件，可参考示例文件 [`.env.example`](https://github.com/nichuanfang/ytm_downloader/blob/main/.env.example)。  

3. **CookieCloud 支持**  
   如果已安装 [CookieCloud](https://github.com/easychen/CookieCloud)，只需在 `.env` 中设置相关参数，无需手动导出 cookies 文件。  

4. **开始下载**  
   完成以上步骤后，运行可执行文件，并按命令行提示操作，即可下载音乐。 🎧

---

## 💻 开发指南（Development）
1. **Fork & Clone** 项目到本地  
2. 创建虚拟环境：  
   ```bash
   python -m venv venv
   ```
3. 安装依赖：  
   ```bash
   pip install -r requirements.txt
   ```
4. 编码完成后构建可执行文件（输出在 `dist/` 目录,可以通过环境变量配置）：  
   ```bash
   pyinstaller --onefile main.py
   ```

---

## 📅 项目进度（Plan）

- [x] CookieCloud 集成
- [x] SoundCloud 支持
- [ ] dns解锁支持
- [ ] 容器化部署
- [ ] webdav集成
- [ ] 发布到到pypi
- [ ] 通过GithubAction自动化发布
- [ ] 多平台支持
- [ ] n8n和telegram集成
---

## 项目目录迁移计划

```
ytm_downloader/
├── README.md
├── .gitignore
├── requirements.txt
├── .env.example
├── .env
├── temp                             # 临时文件夹
├── dist                             # 产物目录
├── main.py                       # 程序入口
├── util.py                       # 工具函数（日志、文件检查等）
├── cookiecloud.py                # CookieCloud 相关逻辑
│   └── .env                      # 运行时配置文件（不纳入版本控制）

├── downloader/                   # 下载相关模块
│   ├── __init__.py
│   ├── youtube.py                # YouTube 下载逻辑
│   └── soundcloud.py             # SoundCloud 下载逻辑

├── services/                     # 第三方服务集成（如 CookieCloud）
│   ├── __init__.py
│   └── cookiecloud_service.py    # CookieCloud 封装
│   └── webdav_service.py          # Webdav 封装

├── logs/                         # 日志文件目录（可选）
```
---

## ❤️ 致谢
感谢所有贡献者和开源社区的支持！