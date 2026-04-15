from dataclasses import dataclass
from typing import List


@dataclass
class ArxivPaper:
    id: str
    title: str
    abstract: str
    authors: List[str]
    published: str
    categories: List[str]
    url: str
    pdf_url: str


@dataclass
class ChatResponse:
    answer: str
    papers_used: int
    confidence: str
    sources: List[str]