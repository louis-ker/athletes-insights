from typing import List
# from langchain.schema import Document
from langchain_core.documents import Document

def format_docs(docs: List[Document]) -> str:
    return "\n\n".join(d.page_content for d in docs)
