from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class SearchResultMessage:
    """
    统一的搜索结果消息类，包含EXA搜索和FinalAnswerFormat工具的所有字段
    """
    def __init__(self, title: str, url: str, text: str, published_date: Optional[str] = None, source_type: Optional[str] = None, filename: Optional[str] = None, score: Optional[str] = None, score_details: Optional[Dict[str, Any]] = None):
        self.title = title
        self.url = url
        self.text = text
        self.published_date = published_date
        self.source_type = source_type
        self.filename = filename
        self.score = score
        self.score_details = score_details

    
    def to_dict(self) -> Dict[str, Any]:
        """将SearchResult对象转换为字典格式"""
        return {
            "title": self.title,
            "url": self.url,
            "text": self.text,
            "published_date": self.published_date,
            "source_type": self.source_type,
            "filename": self.filename,
            "score": self.score,
            "score_details": self.score_details
        }