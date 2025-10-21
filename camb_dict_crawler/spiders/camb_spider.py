from pathlib import Path
from scrapy.spiders import SitemapSpider
from camb_dict_crawler.items import WordItem, Definition, Bilingual
import time
import scrapy
import scrapy.http as s_http

class MySpider(SitemapSpider):
    name = "camb_dict_spider"
    sitemap_urls = [
        "https://dictionary.cambridge.org/sitemap/english-chinese-simplified/sitemap1.xml",
        "https://dictionary.cambridge.org/sitemap/english-chinese-simplified/sitemap2.xml",
        "https://dictionary.cambridge.org/sitemap/english-chinese-simplified/sitemap3.xml",
    ]
    
    def __init__(self, name = None, **kwargs):
        super().__init__(name, **kwargs)

    def get_part_of_speech(self, entry_body_selector: scrapy.Selector) -> str:
        """
        entry_body_selector 参数对应 <div class="pr entry-body__el">  节点
        这个节点下有词性信息，每个词性一个节点
        """
        part_of_speech_raw = entry_body_selector.css("div.posgram.dpos-g.hdib.lmr-5")
        part_of_speech = part_of_speech_raw.xpath("string(.)").get().strip()
        self.log(f"part_of_speech: {part_of_speech}")
        return part_of_speech
    
    def get_phonetic_symbol(self, entry_body_selector: scrapy.Selector) -> list[str]:
        """
        entry_body_selector 参数对应 <div class="pr entry-body__el">  节点
        """
        phonetics_uk = entry_body_selector.css("span.uk.dpron-i").css("span.pron.dpron").xpath("string(.)").get().strip()
        phonetics_us = entry_body_selector.css("span.us.dpron-i").css("span.pron.dpron").xpath("string(.)").get().strip()
        self.log(f"phonetics_uk: {phonetics_uk}")
        self.log(f"phonetics_us: {phonetics_us}")
        return [phonetics_uk, phonetics_us]
        
    def get_definition(self, selector: scrapy.Selector) -> Bilingual:
        """
        selector 参数对应 <div class="def-block ddef_block"> 节点
        """
        
        en_def_raw = selector.css("div.def.ddef_d.db")
        en_def = en_def_raw.xpath("string(.)").get().strip()
        self.log(f"en_definition: {en_def}")
        
        zh_def_raw = selector.css("div.def-body.ddef_b").css("span.trans.dtrans.dtrans-se.break-cj")
        zh_def = zh_def_raw.xpath("string(.)").get().strip()
        self.log(f"zh_definition: {zh_def}")
        
        return Bilingual(en=en_def, zh=zh_def)

    def get_examples(self, selector: scrapy.Selector) -> list[Bilingual]:
        """
        selector 参数对应 <div class="def-block ddef_blopck"> 节点   
        """
        examples: list[Bilingual] = []
        raw_examples = selector.css("div.def-body.ddef_b").css("div.examp.dexamp")
        
        for raw_example in raw_examples:
            en_example = raw_example.css("span.eg.deg").xpath("string(.)").get().strip()
            zh_example = raw_example.css("span.trans.dtrans.dtrans-se.hdb.break-cj").xpath("string(.)").get().strip()
            self.log(f"en_example: {en_example}")
            self.log(f"zh_example: {zh_example}")
            examples.append(Bilingual(en=en_example, zh=zh_example))

        return examples

    def get_definitions(self, sense_body_selector: scrapy.Selector) -> list[Definition]:
        """
        sense_body_selector 参数对应 <div class="sense-body dsense_b">  节点
        """
        definitions: list[Definition] = []
        raw_defs = sense_body_selector.css("div.def-block.ddef_block")
        for raw_def_entry in raw_defs:
            # CEFR 级别
            cefr = raw_def_entry.css("span.def-info.ddef-info").xpath("string(.)").get().strip()
            self.log(f"cefr: {cefr}")
            
            # 定义（释义）
            
            definition: Bilingual = self.get_definition(raw_def_entry)
            examples: list[Bilingual] = self.get_examples(raw_def_entry)
            definitions.append(Definition(cefr=cefr, definition=definition, examples=examples))

        return definitions
        
        
          
    def parse(self, response: s_http.Response):
        self.log(f"response.status: {response.status}")
        word = response.url.split("/")[-1]
        if response.status != 200:
            self.log(f"非200响应，跳过处理。url={response.url}")
            return WordItem(word=word, part_of_speech="", phonetic_symbol=[], definitions=[])
                
        # 页面是首先是按照词性分块
        for entry in response.css('div.pr.entry-body__el'):
            
            
            # 获取词性
            part_of_speech = self.get_part_of_speech(entry)
            phonetic_symbol = self.get_phonetic_symbol(entry)
            
            # 获取该词性下的释义 + 例句
            sense_body = entry.css('div.sense-body.dsense_b')
            definitions = self.get_definitions(sense_body)
            wordItem: WordItem = WordItem(
                word=word,
                part_of_speech=part_of_speech,
                phonetic_symbol=phonetic_symbol,
                definitions=definitions
            )
            
            self.log(f"generated wordItem: {wordItem}")
            yield wordItem
        
