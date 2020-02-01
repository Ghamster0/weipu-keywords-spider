from scrapy_redis.spiders import RedisSpider
from urllib.parse import urlparse, parse_qsl, urlunparse, urlencode
import scrapy
import logging
import json
import re
import os
from scrapy.linkextractors import LinkExtractor
from weipu_keyword_spider.settings import BASE_DATA_DIR
from weipu_keyword_spider.items import WeipuSpiderItem


class WeipuSpider(RedisSpider):
    name = "weipu-keywords"
    # feed url like: http://www.cqvip.com/main/search.aspx?k=keywords
    redis_key = "wepu-keywords:start_urls"

    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.base_url = "http://www.cqvip.com"
        self.article_re0 = re.compile("/\w+/\w+/\d+/\d+\.html")
        self.downloadExtractor1 = LinkExtractor(
            restrict_css=".contains .detailtitle a.download"
        )
        self.realDownloadExtractor2 = LinkExtractor(
            restrict_css="#paper_down .contain .getfile"
        )

    def parse(self, response):
        res = json.loads(response.text)
        if "message" not in res or res["message"] == "":
            logging.debug("=> Last page: " + response.url)
            return
        content = res["message"]
        # extract article here
        links = self.article_re0.findall(content)
        for link in links:
            fid = link[1:-5].replace("/", "-")
            yield scrapy.Request(
                url=self.base_url + link, callback=self.parse1, meta={"fid": fid}
            )
        # next page
        parsed_url = list(urlparse(response.url))
        query_dict = dict(parse_qsl(parsed_url[4]))
        query_dict["curpage"] = int(query_dict["curpage"]) + 1
        parsed_url[4] = urlencode(query_dict)
        next_url = urlunparse(parsed_url)
        yield scrapy.Request(url=next_url, callback=self.parse)

    def parse1(self, response):
        links = self.downloadExtractor1.extract_links(response)
        if len(links) <= 0:
            logging.warning(
                "Warning: download button not found in page, url: " + response.url
            )
            return
        # save raw html
        fid = response.meta["fid"]
        dir_path = BASE_DATA_DIR + "/" + fid
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        with open(dir_path + "/" + fid + ".html", "w") as h5f:
            h5f.write(response.text)
        # extract page meta
        page_contains = response.css(".lay .contains")
        title = page_contains.css(".detailtitle h1::text").get()
        publisher = self.strip_join(
            page_contains.css(".detailtitle strong i *::text").getall()
        )
        author = response.xpath("//head/meta[@name='citation_author']/@content").getall()
        date = response.xpath("//head/meta[@name='citation_date']/@content").get()
        issue = response.xpath("//head/meta[@name='citation_issue']/@content").get()
        volume = response.xpath("//head/meta[@name='citation_volume']/@content").get()
        abstract = self.strip_join(
            page_contains.xpath(
                '//div[@class="detailinfo"]/table[contains(@class, "datainfo")][1]//td/text()'
            ).getall()
        )
        keywords = self.strip_join(
            page_contains.xpath(
                '//div[@class="detailinfo"]/table[contains(@class, "datainfo")][2]//tr[2]//td[2]//text()'
            ).getall()
        )
        meta = {
            "fid": fid,
            "title": title,
            "author": author,
            "date": date,
            "issue": issue,
            "volume": volume,
            "publisher": publisher,
            "abstract": abstract,
            "keywords": keywords,
            "url": response.url
        }
        yield scrapy.Request(
            url=links[0].url, callback=self.parse2, meta={"extra_meta": meta}
        )

    def parse2(self, response):
        download_links = self.realDownloadExtractor2.extract_links(response)
        download_links = [i.url for i in download_links]
        if len(download_links) <= 0:
            logging.warning("download link not found! Url: " + response.url)
            return

        meta = response.meta["extra_meta"]
        meta["download_links"] = download_links
        item = WeipuSpiderItem()
        item["meta"] = meta
        yield item

    def strip_join(self, arr):
        return " ".join([i.strip() for i in arr])

