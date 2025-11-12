from langchain_core.messages import HumanMessage, SystemMessage

from .types import GradeDocuments, GradeHallucinations, GradeAnswer
from .prompts import (
    DOC_GRADER_INSTRUCTIONS, DOC_GRADER_PROMPT,
    HALLUCINATION_GRADER_INSTRUCTIONS, HALLUCINATION_GRADER_PROMPT,
    ANSWER_GRADER_INSTRUCTIONS, ANSWER_GRADER_PROMPT,
)

def create_doc_grader(llm):
    return llm.with_structured_output(GradeDocuments)

def create_hallucination_grader(llm):
    return llm.with_structured_output(GradeHallucinations)

def create_answer_grader(llm):
    return llm.with_structured_output(GradeAnswer)

def grade_document_relevance(structured_grader, document_text: str, question: str) -> str:
    prompt = DOC_GRADER_PROMPT.format(document=document_text, question=question)
    result = structured_grader.invoke(
        [SystemMessage(content=DOC_GRADER_INSTRUCTIONS), HumanMessage(content=prompt)]
    )
    return (result.binary_score or "").lower()

def grade_hallucination(structured_grader, facts_text: str, generation_text: str) -> str:
    prompt = HALLUCINATION_GRADER_PROMPT.format(documents=facts_text, generation=generation_text)
    result = structured_grader.invoke(
        [SystemMessage(content=HALLUCINATION_GRADER_INSTRUCTIONS), HumanMessage(content=prompt)]
    )
    return (result.binary_score or "").lower(), result.explanation

def grade_answer(structured_grader, question: str, generation_text: str) -> str:
    prompt = ANSWER_GRADER_PROMPT.format(question=question, generation=generation_text)
    result = structured_grader.invoke(
        [SystemMessage(content=ANSWER_GRADER_INSTRUCTIONS), HumanMessage(content=prompt)]
    )
    return (result.binary_score or "").lower(), result.explanation
