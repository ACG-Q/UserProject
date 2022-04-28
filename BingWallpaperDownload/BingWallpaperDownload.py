#-*-coding:utf-8 -*-
import requests
import os
import json
import re
import random
import sys

DesktopPath = os.path.join(os.path.expanduser('~'), "Desktop")
Picturespath = os.path.join(os.path.expanduser('~'), "Pictures")

__version__ = "1.1"
__logo__ = """  ____  _              __          __   _ _                             
 |  _ \(_)             \ \        / /  | | |                            
 | |_) |_ _ __   __ _   \ \  /\  / /_ _| | |_ __   __ _ _ __   ___ _ __ 
 |  _ <| | '_ \ / _` |   \ \/  \/ / _` | | | '_ \ / _` | '_ \ / _ \ '__|
 | |_) | | | | | (_| |    \  /\  / (_| | | | |_) | (_| | |_) |  __/ |   
 |____/|_|_| |_|\__, |     \/  \/ \__,_|_|_| .__/ \__,_| .__/ \___|_|   
                 __/ |                     | |         | |              
                |___/                      |_|         |_|      By 六记"""

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

def logo():
    print(__logo__)

def downloader(name, url, path):
    print(path)
    try:
        print(f"[{chr(9660)}] 正在下载 {url} 目标: {path}")
        res = requests.get(url)
        res.raise_for_status()
        utils.saveFile(path, res.content, mode="wb")
        print(f"[{chr(10004)}] 图片 {name} 下载成功, 保存路径: {path}")
        return True
    except BaseException as e:
        print(f"[ERROR] 图片 {name} 下载失败")
        print(f"[ERROR] 下载失败原因: {e}")
        return False
                


# https://www.bing.com/th?id=OHR.AmmoniteShell_ZH-CN9232274077_1920x1080.jpg&rf=LaDigue_1920x1080.jpg

# ID=HpApp,19231.1
# https://www.bing.com/th?id=OHR.IrohazakaRoad_ZH-CN9151363864_1920x1080.jpg&rf=LaDigue_1920x1080.jpg


def getImageId(url):
    imageId = re.findall("id=(.*?)1920x1080.jpg",url)
    return imageId[0]

def getImageInfo():
    res = requests.get("https://cn.bing.com/hp/api/model")
    if res.status_code == 200:
        res = res.json()
        mediaContents = res.get("MediaContents")
        imageInfo = []
        for i in mediaContents:
            imageConten = i.get("ImageContent")
            if imageConten:
                image = imageConten.get("Image")
                imageName = imageConten.get("Title")
                if image:
                    imageUrl = image.get("Url")
                    imageInfo.append({"Name": imageName, "Url": imageUrl})
        return imageInfo
    else:
        return []
        
def main(savePath):
    # 获取图片信息
    info = getImageInfo()
    threads = []
    # 生成图片链接
    for i in info:
        id = getImageId(i.get("Url"))
        # 1080P、4k
        flags = ['1920x1080', 'UHD']
        for flag in flags:
            url = f"https://www.bing.com/th?id={id}{flag}.jpg&rf=LaDigue_{flag}.jpg"
            name = i.get('Name').replace(" ", "_").replace("/","_").replace("\\","_")
            path = utils.montage(savePath, f"{flag}_{name}.jpg")
            downloader(name, url, path)
    
if __name__ == "__main__":
    try:
        logo()
        print(f"Bing壁纸下载工具 v{__version__}")
        args = sys.argv
        defualtPath = os.path.join(Picturespath, "下载")
        if len(args) > 1:
            savePath = args[1]
        else:
            
            print(f"支持回复: \n\tA: {DesktopPath}[桌面路径]\n\tB: {Picturespath}[图片路径]")
            savePath = input(f"请输入保存路径(默认: {defualtPath}): ")
            if savePath.lower() == "a": savePath = DesktopPath
            if savePath.lower() == "b": savePath = Picturespath
           
            
        if savePath is None or savePath == "": savePath = defualtPath
        main(savePath)
    except KeyboardInterrupt as er:
        # ❌
        print(f"\n[{chr(10060)}] 已退出")
    