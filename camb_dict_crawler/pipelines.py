# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from camb_dict_crawler.items import ErrorItem, WordItem
from scrapy.exporters import JsonLinesItemExporter


class CambDictCrawlerPipeline:
    
    def open_spider(self, spider):
        spider.log("CambDictCrawlerPipeline opened.")
        self.success_exports_file = open("successful_items.jl", "wb")
        self.failure_exports_file = open("error_items.jl", "wb")
        self.success_exports = JsonLinesItemExporter(self.success_exports_file, encoding="utf-8")
        self.failure_exports = JsonLinesItemExporter(self.failure_exports_file, encoding="utf-8")

    def close_spider(self, spider):
        spider.log("CambDictCrawlerPipeline closed.")
        self.success_exports_file.close()
        self.failure_exports_file.close()
        
    def process_item(self, item, spider):
        if isinstance(item, WordItem):
            spider.log(f"WordItem captured: {item.word}")
            self.success_exports.export_item(item)
        elif isinstance(item, ErrorItem):
            spider.log(f"ErrorItem captured: URL={item.url}, Error={item.error_message}")
            self.failure_exports.export_item(item)
        else:
            spider.log(f"Unknown item type: {type(item)}")
            spider.log(f"Should not reach here. Item: {item}")
        return item
