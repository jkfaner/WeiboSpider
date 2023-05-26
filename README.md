<a href="https://github.com/jkfaner/WeiboSpider">
 <img alt="weibo-spider-Logo" src="https://github.com/jkfaner/WeiboSpider/blob/master/image/icons8-微博.svg">
</a>

# WeiboSpider

> 微博爬虫系统，高效率博主图片视频爬取。数据接口均来自weibo.com
- 单机版：https://github.com/jkfaner/WeiboSpider
- 分布式版：https://github.com/jkfaner/WeiboSpiderX

[![GitHub stars](https://img.shields.io/github/stars/jkfaner/apple-monitor.svg)](https://github.com/jkfaner/apple-monitor)

### 功能

爬取关注用户的图片数据，包括但不限于视频、livephoto数据。

### 特点

- 数据增量式爬取
- 自定义参数
- 稳定效率高

### 新增功能

- 自定义爬虫模式
- 自定义只爬用户
- 自定义排除用户
- 自定义数据筛选规则
- 数据增量式爬取

### 使用说明

1. 环境支持

```
- python 3 # 脚本执行环境
- redis # 缓存
```

2. 依赖安装
3. 配置文件设置在`src/resource/system-config.json`具体配置如下:

```json
{
  "spider": {
    "rule": 2,
    "login": {
      "uid": "登录用户的uid"
    },
    "download": {
      "root": "文件保存的根路径",
      "thread": true,
      "workers": 8
    },
    "filter": {
      "filter-user": true,
      "filter-blog": true,
      "filter-type": "筛选条件：请填入'original'或'forward',筛选条件是指爬取的数据，original（原创）forward（转发）",
      "original": [
        "筛选原创内容，这里放入用户的首页地址url，例如：https://weibo.com/u/xxxxx"
      ],
      "forward": [
        "筛选转发内容，这里放入用户的首页地址url，例如：https://weibo.com/u/xxxxx"
      ],
      "backups": [
        "该字段仅做备份使用"
      ]
    }
  },
  "database": {
    "redis": {
      "host": "localhost",
      "port": 6379,
      "password": "",
      "db": 0
    }
  },
  "system": {
    "api": {
      "userBlog": "https://weibo.com/ajax/statuses/mymblog",
      "userInfo": "https://weibo.com/ajax/profile/info",
      "userInfoDetail": "https://weibo.com/ajax/profile/detail",
      "userFriends": "https://weibo.com/ajax/friendships/friends",
      "userFollow": "https://weibo.com/ajax/profile/followContent"
    },
    "user-agent-list": [
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
      "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
      "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
      "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
      "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
      "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
      "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
      "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
      "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
      "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
      "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
      "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36"
    ]
  }
}
```

4. 手动配置爬取用户

### 参考

- https://github.com/dataabc/weiboSpider
- https://github.com/CharlesPikachu/DecryptLogin
- https://github.com/kingname/JsonPathFinder

### 鸣谢

<a target="_blank" href="https://icons8.com/icon/20910/微博">微博</a> icon by <a target="_blank" href="https://icons8.com">
Icons8</a>

### 支持

<p align="center">
  <a href="https://github.com/jkfaner/apple-monitor/blob/master/image/sponsor.jpg">
   <img alt="apple-monitor" src="https://github.com/jkfaner/apple-monitor/blob/master/image/sponsor.jpg">
  </a>
</p>