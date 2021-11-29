```
  ____  _              __          __   _ _                             
 |  _ \(_)             \ \        / /  | | |                            
 | |_) |_ _ __   __ _   \ \  /\  / /_ _| | |_ __   __ _ _ __   ___ _ __ 
 |  _ <| | '_ \ / _` |   \ \/  \/ / _` | | | '_ \ / _` | '_ \ / _ \ '__|
 | |_) | | | | | (_| |    \  /\  / (_| | | | |_) | (_| | |_) |  __/ |   
 |____/|_|_| |_|\__, |     \/  \/ \__,_|_|_| .__/ \__,_| .__/ \___|_|   
                 __/ |                     | |         | |              
                |___/                      |_|         |_|      By 六记
```

## Bing壁纸下载

### 原理

1. 通过 https://cn.bing.com/hp/api/model 必应壁纸API 获取壁纸列

  > 壁纸下载链接: JSONPath: MediaContents.ImageContent.Image.Wallpaper(或者 Url)
  > 
  > 壁纸名称链接: JSONPath: MediaContents.ImageContent.Title
  > 

  ```json
  {
    "不重要的信息": "不重要的信息",
    "MediaContents": [
      {
        "ImageContent": {
          "Description": null,
          "Image": {
            "Url": "/th?id=OHR.Invergarry_ZH-CN9013535988_1920x1080.jpg&rf=LaDigue_1920x1080.jpg",
            "Wallpaper": "/th?id=OHR.Invergarry_ZH-CN9013535988_1920x1200.jpg&rf=LaDigue_1920x1200.jpg",
            "Downloadable": true
          },
          "Headline": null,
          "Title": "Invergarry村庄附近的森林，苏格兰",
          "Copyright": "© Matt Anderson Photography/Getty Images",
          "SocialGood": null,
          "MapLink": {
            "Url": "",
            "Link": ""
          },
          "QuickFact": {
            "MainText": "",
            "LinkUrl": "",
            "LinkText": ""
           },
           "TriviaUrl": "/search?q=Bing+homepage+quiz&filters=WQOskey:\"HPQuiz_20211120_Invergarry\"&FORM=HPQUIZ",
           "BackstageUrl": "/search?q=%e8%8b%8f%e6%a0%bc%e5%85%b0&form=hpcapt&mkt=zh-cn",
           "TriviaId": "HPQuiz_20211120_Invergarry"
         },
         "AudioContent": null,
         "VideoContent": null,
         "Ssd": "20211120_1600",
         "FullDateString": "2021 11月 21"
       },
       "AudioContent": null,
       "VideoContent": null,
       "Ssd": "20211124_1600",
       "FullDateString": "2021 11月 25"
      },
      {"省略...":"省略..."},
      {"省略...":"省略..."},
      {"省略...":"省略..."},
      {"省略...":"省略..."},
      {"省略...":"省略..."},
      {"省略...":"省略..."}
    ],
    "不重要的信息": "不重要的信息",
  }
  ```

2. 组合下载链接

  > 将 https://www.bing.com 和 获取到的壁纸下载链接 进行拼接即可
  > 
  > 例如:
  > 
  > title: `Invergarry村庄附近的森林，苏格兰`
  > 
  > wallpaper: `/th?id=OHR.SquirrelsCairngorms_ZH-CN9369511507_1920x1080.jpg&rf=LaDigue_1920x1080.jpg`
  > 
  > download: `https://www.bing.com/th?id=OHR.SquirrelsCairngorms_ZH-CN9369511507_1920x1080.jpg&rf=LaDigue_1920x1080.jpg`
  > 


### 下载结果(图片文件预览)

#### 默认的是1080P:

> title: `Invergarry村庄附近的森林，苏格兰`
> 
> wallpaper: `/th?id=OHR.SquirrelsCairngorms_ZH-CN9369511507_1920x1080.jpg&rf=LaDigue_1920x1080.jpg`
> 
> download: `https://www.bing.com/th?id=OHR.SquirrelsCairngorms_ZH-CN9369511507_1920x1080.jpg&rf=LaDigue_1920x1080.jpg`
> 

下载结果:

![1920x1080_Invergarry村庄附近的森林，苏格兰.jpg 预览图](https://cdn.jsdelivr.net/gh/ACG-Q/UserProject@main/BingWallpaperDownload/res/1080P预览图.webp)

#### 将 1920x1080 替换成 UHD, 就可以获取4K的壁纸下载链接[不是所有的图片都具有4K版图片]

> download_1080P: `https://www.bing.com/th?id=OHR.SquirrelsCairngorms_ZH-CN9369511507_1920x1080.jpg&rf=LaDigue_1920x1080.jpg`
> 
> download: `https://www.bing.com/th?id=OHR.SquirrelsCairngorms_ZH-CN9369511507_UHD.jpg&rf=LaDigue_UHD.jpg`
> 

下载结果:

![UHD_Invergarry村庄附近的森林，苏格兰.jpg 预览图](https://cdn.jsdelivr.net/gh/ACG-Q/UserProject@main/BingWallpaperDownload/res/4K预览图.webp)

### 使用方法

1. 简单的使用方法

> 直接双击运行，即可
> 

![](https://cdn.jsdelivr.net/gh/ACG-Q/UserProject@main/BingWallpaperDownload/res/BingWallpaperDownload使用.webp)

2. 当作命令行程序使用

> 我这不是合规的命令行程序

```
BingWallpaperDownload.exe 保存路径
例如: BingWallpaperDownload.exe c:/Users/10436/Desktop/adajlksdj/asdasd
```
ps: 会自动创建不存在的文件夹
