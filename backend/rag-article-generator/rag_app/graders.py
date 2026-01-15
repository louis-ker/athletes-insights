# from langchain_core.messages import HumanMessage, SystemMessage

# from .types import GradeDocuments, GradeHallucinations, GradeAnswer
# from .prompts import (
#     DOC_GRADER_INSTRUCTIONS, DOC_GRADER_PROMPT,
#     HALLUCINATION_GRADER_INSTRUCTIONS, HALLUCINATION_GRADER_PROMPT,
#     ANSWER_GRADER_INSTRUCTIONS, ANSWER_GRADER_PROMPT,
# )

# def create_doc_grader(llm):
#     return llm.with_structured_output(GradeDocuments)

# def create_hallucination_grader(llm):
#     return llm.with_structured_output(GradeHallucinations)

# def create_answer_grader(llm):
#     return llm.with_structured_output(GradeAnswer)

# def grade_document_relevance(structured_grader, document_text: str, question: str) -> str:
#     prompt = DOC_GRADER_PROMPT.format(document=document_text, question=question)
#     result = structured_grader.invoke(
#         [SystemMessage(content=DOC_GRADER_INSTRUCTIONS), HumanMessage(content=prompt)]
#     )
#     return (result.binary_score or "").lower()

# def grade_hallucination(structured_grader, facts_text: str, generation_text: str) -> str:
#     prompt = HALLUCINATION_GRADER_PROMPT.format(documents=facts_text, generation=generation_text)
#     result = structured_grader.invoke(
#         [SystemMessage(content=HALLUCINATION_GRADER_INSTRUCTIONS), HumanMessage(content=prompt)]
#     )
#     return (result.binary_score or "").lower(), result.explanation

# def grade_answer(structured_grader, question: str, generation_text: str) -> str:
#     prompt = ANSWER_GRADER_PROMPT.format(question=question, generation=generation_text)
#     result = structured_grader.invoke(
#         [SystemMessage(content=ANSWER_GRADER_INSTRUCTIONS), HumanMessage(content=prompt)]
#     )
#     return (result.binary_score or "").lower(), result.explanation

from langchain_core.messages import HumanMessage, SystemMessage
# On importe les nouveaux types
from .types import GradeDocumentsBatch, GradeHallucinations, GradeAnswer 
from .prompts import (
    DOC_GRADER_INSTRUCTIONS, DOC_GRADER_PROMPT,
    HALLUCINATION_GRADER_INSTRUCTIONS, HALLUCINATION_GRADER_PROMPT,
    ANSWER_GRADER_INSTRUCTIONS, ANSWER_GRADER_PROMPT,
)

def create_doc_grader(llm):
    # On bind le modèle "Batch"
    return llm.with_structured_output(GradeDocumentsBatch)

def create_hallucination_grader(llm):
    return llm.with_structured_output(GradeHallucinations)

def create_answer_grader(llm):
    return llm.with_structured_output(GradeAnswer)

# --- MODIFICATION ICI : Fonction Batch ---
def grade_documents_batch(structured_grader, documents: list, question: str):
    """
    Construit une chaîne unique contenant tous les docs numérotés,
    appelle le LLM une seule fois, et renvoie la liste des résultats.
    """
    # 1. Préparer le texte formaté : "Doc 0: ... \n Doc 1: ..."
    formatted_docs_list = []
    for i, d in enumerate(documents):
        # On coupe un peu le contenu pour économiser des tokens si besoin
        content_preview = d.page_content[:1500].replace("\n", " ") 
        formatted_docs_list.append(f"Doc {i}: {content_preview}")
    
    formatted_input = "\n\n".join(formatted_docs_list)
    
    # 2. Préparer le prompt
    prompt = DOC_GRADER_PROMPT.format(question=question, formatted_documents=formatted_input)
    
    # 3. Invocation unique
    result = structured_grader.invoke(
        [SystemMessage(content=DOC_GRADER_INSTRUCTIONS), HumanMessage(content=prompt)]
    )
    
    # result est un objet GradeDocumentsBatch qui contient .scores (list)
    # On transforme ça en un dictionnaire {index: 'yes'/'no'} pour accès rapide
    if result and result.scores:
        return {item.index: item.binary_score.lower() for item in result.scores}
    return {}
# -----------------------------------------

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
