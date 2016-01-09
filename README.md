# Intro
抓取微博中伦敦找房子的信息~主要是想给自己找接手的人用的哈~

# Installation (initial configuration)
- create a `mycfg.json` in root directory following the template below.
**REMEMBER** to change the cookies field.
- initialize local database
```sh
python init_db.py
```

# Usage
```sh
scrapy crawl weibo [-a nPages=10]
```

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

# comments by potential tenants (collectedly manually)
- renruocao：房型是ensuit吗？
- 馥焓yeti：邮编是！？？
- 藤原腿：多少钱？
- 追着风奔跑的孩子：1，30号有吗
- 馥焓yeti：多少一周
- _灼灼其华_：可以预约看一下么 另外 这个是几人共用浴室？
