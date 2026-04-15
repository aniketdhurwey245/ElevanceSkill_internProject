import requests
import xml.etree.ElementTree as ET
from typing import List
from models.schemas import ArxivPaper

ARXIV_API = "http://export.arxiv.org/api/query"


def fetch_arxiv(query: str, category: str, max_results: int = 5) -> List[ArxivPaper]:
    params = {
        "search_query": f"({query}) AND cat:{category}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending",
    }

    try:
        r = requests.get(ARXIV_API, params=params, timeout=15)
        r.raise_for_status()
        return parse_arxiv_xml(r.text)
    except Exception:
        return []


def parse_arxiv_xml(xml_text: str) -> List[ArxivPaper]:
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(xml_text)

    papers = []

    for entry in root.findall("atom:entry", ns):
        def g(tag):
            el = entry.find(tag, ns)
            return el.text.strip() if el is not None and el.text else ""

        paper = ArxivPaper(
            id=g("atom:id").split("/abs/")[-1],
            title=g("atom:title"),
            abstract=g("atom:summary"),
            authors=[a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)],
            published=g("atom:published")[:10],
            categories=[c.get("term") for c in entry.findall("atom:category", ns)],
            url=g("atom:id"),
            pdf_url=g("atom:id").replace("/abs/", "/pdf/")
        )

        papers.append(paper)

    return papers