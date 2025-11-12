from typing import Literal
from langchain_core.messages import HumanMessage, SystemMessage
from .types import RouteQuery
from .prompts import ROUTER_INSTRUCTIONS

def create_router(llm):
    """
    Return an LLM bound to the RouteQuery structured output.
    """
    return llm.with_structured_output(RouteQuery)

def route_decision(structured_llm_router, question: str) -> Literal["websearch", "vectorstore"]:
    source = structured_llm_router.invoke(
        [SystemMessage(content=ROUTER_INSTRUCTIONS), HumanMessage(content=question)]
    )
    if source.datasource == "websearch":
        return "websearch"
    return "vectorstore"
