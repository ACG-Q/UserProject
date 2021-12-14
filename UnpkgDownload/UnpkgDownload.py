# -*-coding:utf-8 -*-
import argparse
import requests
import re
import os
import time
import shutil
import tempfile


__version__ = "1.0"
__url = "https://unpkg.com/"
__logo__ = """   __  __            __            ____                      __                __
  / / / /___  ____  / /______ _   / __ \____ _      ______  / /___  ____ _____/ /
 / / / / __ \/ __ \/ //_/ __ `/  / / / / __ \ | /| / / __ \/ / __ \/ __ `/ __  / 
/ /_/ / / / / /_/ / ,< / /_/ /  / /_/ / /_/ / |/ |/ / / / / / /_/ / /_/ / /_/ /  
\____/_/ /_/ .___/_/|_|\__, /  /_____/\____/|__/|__/_/ /_/_/\____/\__,_/\__,_/   
          /_/         /____/                                        By 六记"""

# 下载目标名称的字符
__targetChar = "-_"
# 排除
__excludeFile = ['../','LICENSE']
__excludePath = ['/src/','/packages/','/types/','/dist/docs/','/docs/','/samples/',"/test/","/locale/"]

DownloadsPath = os.path.join(os.path.expanduser('~'), "Downloads")

parser = argparse.ArgumentParser(description="Unpkg.com下载工具 1. 理论上支持Unpkg.com所有的链接 2. 不支持多线程下载(防止过多请求)")


def logo(): print(__logo__)

def __analysisDownload(download_url):
    # if '@' in download_url:
    target = ""
    version = "latest"
    try:
        groups = re.search(f'/?(\w+[{__targetChar}]?\w+)@((\d[.]?){3})/?', download_url).groups()
        target = groups[0]
        version = groups[1]
    except:
        if 'unpkg.com' in download_url:
            groups = re.search(f'unpkg.com/(\w+[{__targetChar}]?\w+)/?', download_url).groups()
            target = groups[0]
        else:
            target = download_url
    finally:
        return target, version

def __createFolder(directorys, file = "./"):
    for directory in directorys:
        if directory[0] == "/": directory = "." + directory
        path = os.path.abspath(os.path.join(file, directory))
        print(f"[i] 待创建: {path}")
        if not os.path.exists(path):
            print(f"[+] 创建目录: {path}")
            os.makedirs(path)
        else:
            print(f"[+] 创建目录: {path}")

def getResponse(download_url, encoding='utf-8'):
    headers = {
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Content-Type': 'text/html;Charset=utf-8',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    
    }
    req = requests.get(download_url, params=None, headers=headers)
    req.encoding = encoding
    return req.text

def getAllVersion(target):
    # print(f"{__url}{target}")
    html = getResponse(f"{__url}{target}/")
    # print(html)
    temp = re.findall(r'<select name="version"(.*?)</select>', html,re.S)[0] 
    patt = re.compile(r'<option.+?>(.+?)</option>')
    return patt.findall(temp)

def listFolderContents(info, splitChar="/"):
    files = []
    folders=[]
    html = getResponse(f"{__url}/{info}{splitChar}")
    table = re.findall(r'<table(.*?)</table>', html, re.S)[0] 
    href = re.findall('href="(.*?)"', table)
    for name in href:
        path = splitChar + name
        if name in __excludeFile or path in __excludePath: continue
        if name[-1] == "/":
            folders.append(path)
            filesTemp, foldersTemp = listFolderContents(info, path)
            folders.extend(foldersTemp)
            files.extend(filesTemp)
        else:
            files.append(path)
    
    return files, folders

def download(url, targetPath):
    if not os.path.exists(targetPath):
        print(f"[{chr(8693)}] 下载: {url}")
        res = requests.get(url)
        fd, path = tempfile.mkstemp()
        try:
            with os.fdopen(fd, 'wb') as tmp:
                # do stuff with temp file
                tmp.write(res.content)
        finally:
            shutil.move(path, targetPath)
            # os.remove(path)
    else:
        print(f"[?] 文件已存在 --> {targetPath}")

def main():
    args = parser.parse_args()
    # !!! 未填写输出路径
    if not args.output and args.output is None and args.output == "":
        savePath = "./"
    else:
        savePath = args.output

    # !!! 解析下载目标target 下载版本version
    target, version = __analysisDownload(args.download)

    # !!! 未填写输出路径 填写的version优先度高✨
    if not (not args.version and args.version is None and args.version == ""):
        version = args.version

    

    print(f"[i] target: {target}\n[i] version: {version}")

    # !!! 获取全部版本
    versions = getAllVersion(target)

    # !!! 获取到版本, 并且存在于所有版本中
    if version.lower() != "latest" and version in versions:
        print(f"[i] 找到指定版本 --> {version}")
    else:
        version = versions[-1]
        print(f"[i] 未找到指定版本 --> {version}")
    
    info = f"{target}@{version}"
    print(f"[i] 下载版本: {info}")

    files, folders = listFolderContents(info)
    targetPath = os.path.join(savePath, info)
    __createFolder(folders, targetPath)
    for file in files:
        url = f"{__url}{info}{file}"
        # print(f"[DEBUG] {targetPath} {file}")
        if file[0] == "/": file = "." + file
        path = os.path.abspath(os.path.join(targetPath, file))
        print(f"[{chr(8595)}] 正在下载 {url} 目标: {path}")
        download(url, path)

    print(f"[{chr(10004)}] 完成")

if __name__ == "__main__":
    logo()
    parser.add_argument('-o', '--output', type=str, default=DownloadsPath, help=f"默认下载路径: {DownloadsPath}")
    parser.add_argument('-d', '--download', type=str, help='下载链接, 支持填写链接、填写目标(vue)、填写目标@版本(vue@2.6.14)', required=True)
    parser.add_argument('-v', '--version', type=str, help='下载版本, 不填写则默认最新')
    main()