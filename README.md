Music Downloader For Youtube Premium.

## Prerequisite

1. 本地需要安装3.8以上版本的python
2. 有**魔法**

## How to use
1. 第一次使用,需要打开可执行文件一次以初始化.env以及创建音频存放目录
2. 用户可以自定义.env中的内容,具体可以参考本项目的[.env.example](https://github.com/nichuanfang/ytm_downloader/blob/main/.env.example)中的配置箱
3. 如果你已经安装了cookiecloud,可以通过配置.env相应的cookiecloud参数,此后可以无需手动利用插件导出cookies文件
4. 准备工作都做好之后,点击**可执行文件**根据命令行提示操作

## Developement

1. fork本项目,克隆到本地
2. 创建venv虚拟环境
3. 安装依赖
    ```python
    pip install -r requirements.txt
    ```
4. 编码完成之后,通过下面的命令构建成可执行文件(位于目录 dist 中)
    ```python
    pyinstaller --onefile  main.py
    ```
## Plan

- [x] Cookiecloud integration
- [x] Support soundcloud
- [ ] other cool features is coming...