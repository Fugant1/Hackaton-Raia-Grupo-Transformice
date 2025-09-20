from langchain_community.document_loaders import UnstructuredURLLoader
from typing import List, Dict

def scrap(url: str) -> Dict:
    loader = UnstructuredURLLoader(urls=url)
    docs = loader.load()

    doc = docs[0]
    content = doc.page_content.split("\n")
    content = [line.strip() for line in content if line.strip()]

    headline = content[0] if len(content) > 0 else None
    subtitle = content[1] if len(content) > 1 else None
    lead = content[2] if len(content) > 2 else None
    body = " ".join(content[3:]) if len(content) > 3 else None
    return {'headline': headline, 'subtitle': subtitle, 'lead': lead, 'body': body}