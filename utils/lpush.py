import redis

r = redis.Redis(host="localhost", port=6379, db=0, password="root")
# r.lpush(
#     "wepu-keywords:start_urls",
#     "http://www.cqvip.com/data/main/search.aspx?action=so&k=医学遗传学&curpage=0&perpage=0"
# )
with open("keys.txt", "r") as f:
    for line in f.readlines():
        line = line.strip()
        print(line)
        r.lpush("wepu-keywords:start_urls", f"http://www.cqvip.com/data/main/search.aspx?action=so&k={line}&curpage=0&perpage=0")

