# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


@dataclass
class Definition():
    """单个释义，包含CEFR等级、定义和例句"""
    cefr: str
    definition: Bilingual
    examples: list[Bilingual]

@dataclass
class WordItem():
    """单词条目，包含单词、词性、音标和释义列表"""
    word: str
    # 词性
    part_of_speech: str
    # 音标
    phonetic_symbol: list[str]
    # 释义列表
    definitions: list[Definition]
    
@dataclass
class ErrorItem:
    """用于记录爬取错误的 Item"""
    url: str
    error_message: str
