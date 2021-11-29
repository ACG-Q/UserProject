```
 __          __   _ _ _                            __          __   _ _
 \ \        / /  | | | |                           \ \        / /  | | |
  \ \  /\  / /_ _| | | |__   __ ___   _____ _ __    \ \  /\  / /_ _| | |_ __   __ _ _ __   ___ _ __
   \ \/  \/ / _` | | | '_ \ / _` \ \ / / _ \ '_ \    \ \/  \/ / _` | | | '_ \ / _` | '_ \ / _ \ '__|
    \  /\  / (_| | | | | | | (_| |\ V /  __/ | | |    \  /\  / (_| | | | |_) | (_| | |_) |  __/ |
     \/  \/ \__,_|_|_|_| |_|\__,_| \_/ \___|_| |_|     \/  \/ \__,_|_|_| .__/ \__,_| .__/ \___|_|
                                                                       | |         | |
                                                                       |_|         |_|       By 六记
```

## Wallhaven壁纸下载

### 原理

```mermaid
graph LR
A[配置命令行]
    A --> B{判断}
    B -->|图片页面 例如:https://wallhaven.cc/w/6op786| C[获取图片链接]
    B -->|图片列表页面 例如:首页 排行榜| D[获取图片页面链接 ]
    D --> C
    C --> E[保存图片]
```



```
usage: WallhavenWallpaperDownload.exe [-h] [-o OUTPUT] -d DOWNLOAD

Wallhaven壁纸下载工具 1. 理论上支持Wallhaven.cc所有的链接 2. 不支持多线程下载(防止过多请求)

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        输出路径(默认: C:\Users\10436\Pictures\下载)
                        支持回复: 
                          A: C:\Users\10436\Desktop[桌面路径]
                          B: C:\Users\10436\Pictures[图片路径]
  -d DOWNLOAD, --download DOWNLOAD
                        下载链接
```

### 下载结果(图片文件预览)

![wallhaven](res/wallhaven-3z7zmd.webp)

### 使用方法

1. 不指定下载路径

    ![不指定下载路径](res/不指定下载路径.webp)

2. 指定下载路径

    ![指定下载路径](res/指定下载路径.webp)
