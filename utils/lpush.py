import redis

r = redis.Redis(host="localhost", port=6379, db=0, password="root")
# r.lpush(
#     "wepu-keywords:start_urls",
#     "http://www.cqvip.com/data/main/search.aspx?action=so&k=医学遗传学&curpage=0&perpage=0"
# )
for i in range(10, 20):
    with open(f"/search/odin/data/keywords_parts/{i}.txt", "r") as f:
        for line in f.readlines():
            line = line.strip()
            print(line)
            r.lpush("weipu-keywords:start_urls", f"http://www.cqvip.com/data/main/search.aspx?action=so&k={line}&curpage=0&perpage=0")

