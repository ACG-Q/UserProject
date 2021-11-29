#-*-coding:utf-8 -*-
import argparse
import requests
from lxml import etree
import os
import sys
import re
import time

DesktopPath = os.path.join(os.path.expanduser('~'), "Desktop")
Picturespath = os.path.join(os.path.expanduser('~'), "Pictures")

class Utils:
    def __isExists(self, path):
        return os.path.exists(path)
    
    def __isFolder(self, path):
        return os.path.isdir(path)
    
    def __isFile(self, path):
        return os.path.isfile(path)
    
    def create(self, path, mode=0o777):
        dirPath = os.path.dirname(path)
        ps = dirPath.split("\\")
        path = ps[0] + "\\"
        for i in range(1, len(ps)):
            path = self.montage(path, ps[i])
            # print(f"正在创建: {path}")
            if self.__isExists(path):
                continue
            else:
                os.mkdir(path, mode)

    def saveFile(self, path, content, mode="w", encoding="utf8"):
        if not self.__isExists(path): self.create(path)
        # print(f"正在创建: {path}")
        try:
            if self.__isExists(path):
                dirPath = os.path.dirname(path)
                fileName = path.replace(dirPath, "")
                name, ext = fileName.split(".")
                name = name + f"_{''.join(random.sample('QAZwsxEDCrfvTGByhnUJMikOLpqazWSXedcRFVtgbYHNujmIKolP',5))}"
                filename = f"{name}.{ext}"
                path = os.path.join(dirPath, fileName)
                self.create(path)

            if not path is None and ("b" in mode or "B" in mode):
                with open(path, mode=mode) as f:
                    f.write(content)
                return True
            else:
                with open(path, mode=mode, encoding=encoding) as f:
                    f.write(content)
                return True
        except:
            return False

    def montage(self, *args, **kwargs):
        return os.path.join(*args, **kwargs)

utils = Utils()
parser = argparse.ArgumentParser(description="Wallhaven壁纸下载工具 1. 理论上支持Wallhaven.cc所有的链接 2. 不支持多线程下载(防止过多请求)")

def logo():
    print(""" __          __   _ _ _                            __          __   _ _                             
 \ \        / /  | | | |                           \ \        / /  | | |                            
  \ \  /\  / /_ _| | | |__   __ ___   _____ _ __    \ \  /\  / /_ _| | |_ __   __ _ _ __   ___ _ __ 
   \ \/  \/ / _` | | | '_ \ / _` \ \ / / _ \ '_ \    \ \/  \/ / _` | | | '_ \ / _` | '_ \ / _ \ '__|
    \  /\  / (_| | | | | | | (_| |\ V /  __/ | | |    \  /\  / (_| | | | |_) | (_| | |_) |  __/ |   
     \/  \/ \__,_|_|_|_| |_|\__,_| \_/ \___|_| |_|     \/  \/ \__,_|_|_| .__/ \__,_| .__/ \___|_|   
                                                                       | |         | |              
                                                                       |_|         |_|       By 六记""")

def downloader(name, url, path):
    # print(path)
    try:
        res = requests.get(url)
        res.raise_for_status()
        utils.saveFile(path, res.content, mode="wb")
        print(f"图片 {name} 下载成功, 保存路径: {path}")
        return True
    except BaseException as e:
        print(f"图片 {name} 下载失败")
        print(f"下载失败原因: {e}")
        return False

def getImage(url):
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        html = etree.HTML(response.text)
        return {"Code": True, "Url": html.xpath("//img[@id='wallpaper']/@src")[0]}
    except requests.ConnectTimeout as e:
        return {"Code": False, "Msg": f"连接远程服务器超时异常\n失败原因: {e}"}
    except requests.ConnectionError as e:
        return {"Code": False, "Msg": f"连接失败\n失败原因: {e}"}
    except requests.HTTPError as e:
        return {"Code": False, "Msg": f"HTTP错误异常\n失败原因: {e}"}
    except requests.URLRequired as e:
        return {"Code": False, "Msg": f"URL缺失异常\n失败原因: {e}"}
    except BaseException as e:
        return {"Code": False, "Msg": f"除HTTP异常外的异常\n失败原因: {e}"}

def getImages(url):
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        html = etree.HTML(response.text)
        return {"Code": True, "Urls": [url for url in html.xpath("//a/@href") if (__isImagePage(url) and __isWallhaven(url))]}
    except requests.ConnectTimeout as e:
        return {"Code": False, "Msg": f"连接远程服务器超时异常\n失败原因: {e}"}
    except requests.ConnectionError as e:
        return {"Code": False, "Msg": f"连接失败\n失败原因: {e}"}
    except requests.HTTPError as e:
        return {"Code": False, "Msg": f"HTTP错误异常\n失败原因: {e}"}
    except requests.URLRequired as e:
        return {"Code": False, "Msg": f"URL缺失异常\n失败原因: {e}"}
    except BaseException as e:
        return {"Code": False, "Msg": f"除HTTP异常外的异常\n失败原因: {e}"}

def __isImagePage(url):
    # print("/w/", url, bool(re.search(r"/w/", url)))
    if re.search(r"/w/", url):
        return True
    else:
        return False

def __isWallhaven(url):
    # print("https://wallhaven.cc/", url, bool(re.search(r"https://wallhaven.cc/", url)))
    if re.search(r"https://wallhaven.cc/", url):
        return True
    else:
        return False

def main():
    # 处理命令行
    args = parser.parse_args()
    if args.output:
        if args.output.lower() == "a": 
            savePath = DesktopPath
        elif args.output.lower() == "b":
            savePath = Picturespath
        else:
            savePath = args.output
    if args.download:
        if __isWallhaven(args.download):
            url = args.download
        else:
            print("只支持来自于wallhaven.cc的链接")
            sys.exit()
        
    print(f"保存路径: {savePath}\n下载链接: {url} {'是图片页面' if __isImagePage(url) else '是图片列表页面'}")

    # 获取信息
    urls = []
    if not __isImagePage(url):
        info = getImages(url)
        if info.get("Code"):
            urls = info.get("Urls")
        else:
            print(f"{url} 获取失败 -- {info.get('Msg')}")
            sys.exit()
    else:
        urls = [url]

    # 获取图片链接
    imgUrls = []
    for i in range(len(urls)):
        url = urls[i]
        imgUrl = getImage(url)
        if imgUrl.get("Code"):
            imgUrls.append(imgUrl.get("Url"))
        else:
            print(f"{url} 获取图片链接失败 -- {imgUrl.get('Msg')}")
        if i % 15: time.sleep(1)

    # 下载链接
    for url in imgUrls:
        name = url.split("/")[-1]
        path = os.path.join(savePath, name)
        downloader(name, url, path)
        

if __name__ == "__main__":
    logo()
    defualtPath = os.path.join(Picturespath, "下载")
    parser.add_argument('-o', '--output',
        type=str,
        default=defualtPath, 
        help=f"""输出路径(默认: {defualtPath})
            支持回复: 
                A: {DesktopPath}[桌面路径]
                B: {Picturespath}[图片路径]""")
    parser.add_argument('-d', '--download', type=str, help='下载链接', required=True)

    main()