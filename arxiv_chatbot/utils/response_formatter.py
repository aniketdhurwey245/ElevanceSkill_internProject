from typing import List
from models.schemas import ChatResponse, ArxivPaper


def format_response(answer: str, papers: List[ArxivPaper]) -> ChatResponse:
    confidence = "🟢 High" if len(answer) > 200 else "🟡 Medium"

    sources = [p.title for p in papers[:3]]

    return ChatResponse(
        answer=answer,
        papers_used=len(papers),
        confidence=confidence,
        sources=sources
    )