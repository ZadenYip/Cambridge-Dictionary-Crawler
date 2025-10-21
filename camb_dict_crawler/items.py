# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Bilingual():
    """双语（英中）"""
    en: str
    zh: str

@dataclass
class Definition():
    """单个释义，包含CEFR等级、定义和例句"""
    cefr: Optional[str]
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