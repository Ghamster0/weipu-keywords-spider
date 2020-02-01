import redis

r = redis.Redis(host="localhost", port=6379, db=0, password="root")
# http://www.cqvip.com/data/main/search.aspx?action=so&k=keywords&curpage=0&perpage=0
r.lpush(
    "wepu-keywords:start_urls",
    "http://www.cqvip.com/data/main/search.aspx?action=so&k=医学遗传学&curpage=0&perpage=0"
)

