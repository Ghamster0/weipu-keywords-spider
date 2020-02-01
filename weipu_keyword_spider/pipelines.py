# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.files import FilesPipeline
import scrapy
import json
import logging
import shutil
import random
from weipu_keyword_spider.settings import BASE_DATA_DIR, FILES_STORE
from datetime import datetime


class PDFPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        file_links = item["meta"]["download_links"]
        yield scrapy.Request(
            random.choice(file_links), meta={"fid": item["meta"]["fid"], "is_pdf": True}
        )

    def file_path(self, request, response=None, info=None):
        return request.meta["fid"] + ".pdf"

    def item_completed(self, results, item, info):
        result, msg = results[0]
        if result:
            item["meta"]["pdf_checksum"] = msg["checksum"]
        else:
            logging.warning("pdf download fail, url:" + item["meta"]["url"])
        return item


class JSONPipeline(object):
    def process_item(self, item, spider):
        fid = item["meta"]["fid"]
        item_dir = BASE_DATA_DIR + "/" + fid
        # save json
        with open(item_dir + "/" + fid + ".json", "w") as jsonf:
            jsonf.write(json.dumps(item["meta"], ensure_ascii=False))
        # copy pdf
        pdf_file_name = fid + ".pdf"
        shutil.move(FILES_STORE + "/" + pdf_file_name, item_dir + "/" + pdf_file_name)
        # rename dir append time
        curr_time = datetime.now().strftime("%Y%m%d%H%M%S")
        shutil.move(item_dir, item_dir + "." + curr_time)
        return item
