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
It will
1. Scrape posts of agencies you provided in `mycfg.json` but only those that
   look like seeking for accommodation.
2. Scrape comments of posts that are talking about renting rooms, because those
   who want to find a room are highly likely to comment.
3. Scrape posts (by searching) whose contents are looking for accommodation.

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
    ],
    "tags": [
        "伦敦租房",
        "伦敦住宿",
        "伦敦求租",
        "伦敦租房信息"
    ]
}
```
