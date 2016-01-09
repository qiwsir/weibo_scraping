# Intro
抓取微博中伦敦找房子的信息~主要是想给自己接手的人用的哈~

# Installation (initial configuration)
```sh
python init_db.py
```

# Usage
```sh
scrapy crawl weibo [-a nPages=10]
```

# Notes
1. 抓取[移动端](http://weibo.cn)
2. Login with browser cookie
3. 抓取有"求"、"想租"、"急租"字眼的微博
4. 抓取有"请问"字眼的微博，因为有些求租的人@了但是没被转发
5. Using sqlite3 to store data

# Strucuture of weibo HTML
- class="c"     - whole weibo entry including everything
- class="ctt"   - weibo/comment text without OP name
- class="ct"    - posting time
- class="cc"    - `<a>` of comment

# Sample mycfg.json
```json
{
    "cookies": {
        "_T_WM": "REPLACE_THIS_WITH_YOUR_COOKIES",
        "SUHB": "REPLACE_THIS_WITH_YOUR_COOKIES",
        "SUBP": "REPLACE_THIS_WITH_YOUR_COOKIES",
        "SUB": "REPLACE_THIS_WITH_YOUR_COOKIES",
        "SSOLoginState": "REPLACE_THIS_WITH_YOUR_COOKIES"
    },
    "agencies": [
        {"name": "伦敦租房LondonHome", "id": "3045446321"},
        {"name": "伦敦租房资讯快报", "id": "1871496974"},
    ]
}
```
