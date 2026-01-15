# import operator
# from typing import List, Literal, Annotated
# from typing_extensions import TypedDict
# from pydantic import BaseModel, Field
# # from langchain.schema import Document
# from langchain_core.documents import Document
# from langchain_core.messages import AIMessage

# # ---------- Pydantic models for structured output ----------

# class RouteQuery(BaseModel):
#     """Route a user query to the most relevant datasource."""
#     datasource: Literal["vectorstore", "websearch"] = Field(
#         ..., description="Choose to route to web search or vectorstore."
#     )

# class GradeDocuments(BaseModel):
#     """Binary score for relevance check on retrieved documents."""
#     binary_score: str = Field(description="Documents relevant? 'yes' or 'no'")

# class GradeHallucinations(BaseModel):
#     """Binary score for hallucination presence + explanation."""
#     binary_score: str = Field(description="Answer grounded in facts? 'yes' or 'no'")
#     explanation: str = Field(description="Reasoning for the score")

# class GradeAnswer(BaseModel):
#     """Binary score to assess answer addresses question."""
#     binary_score: str = Field(description="Answer addresses the question? 'yes' or 'no'")
#     explanation: str = Field(description="Reasoning for the score")

# # ---------- LangGraph state ----------

# class GraphState(TypedDict):
#     """
#     State propagated through the graph.
#     """
#     question: str                 # User question
#     generation: AIMessage         # LLM generation (AIMessage from LangChain)
#     web_search: str               # "Yes"/"No" flag to run web search
#     max_retries: int              # Max retries for generation refinement
#     answers: int                  # Number of answers generated (optional usage)
#     loop_step: Annotated[int, operator.add]  # Accumulated loop counter
#     documents: List[Document]     # Retrieved / enriched documents

import operator
from typing import List, Literal, Annotated
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
from langchain_core.documents import Document
from langchain_core.messages import AIMessage

# ---------- Pydantic models for structured output ----------

class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""
    datasource: Literal["vectorstore", "websearch"] = Field(
        ..., description="Choose to route to web search or vectorstore."
    )

# --- MODIFICATION ICI : Structure pour le batch ---
class GradeSingleDocument(BaseModel):
    """Score for a single document in a batch."""
    index: int = Field(description="The index of the document in the provided list (0, 1, 2...)")
    binary_score: str = Field(description="Relevant? 'yes' or 'no'")

class GradeDocumentsBatch(BaseModel):
    """List of scores for multiple documents."""
    scores: List[GradeSingleDocument] = Field(description="List of scores corresponding to the documents")
# --------------------------------------------------

class GradeHallucinations(BaseModel):
    """Binary score for hallucination presence + explanation."""
    binary_score: str = Field(description="Answer grounded in facts? 'yes' or 'no'")
    explanation: str = Field(description="Reasoning for the score")

class GradeAnswer(BaseModel):
    """Binary score to assess answer addresses question."""
    binary_score: str = Field(description="Answer addresses the question? 'yes' or 'no'")
    explanation: str = Field(description="Reasoning for the score")

class GradeQuality(BaseModel):
    """Score combiné pour vérifier à la fois les hallucinations et la pertinence."""
    is_grounded: str = Field(description="Is the answer supported by the facts? 'yes' or 'no'")
    is_relevant: str = Field(description="Does the answer address the question? 'yes' or 'no'")
    explanation: str = Field(description="Reasoning for the scores")

# ---------- LangGraph state ----------

class GraphState(TypedDict):
    question: str
    generation: AIMessage
    web_search: str
    max_retries: int
    answers: int
    loop_step: Annotated[int, operator.add]
    documents: List[Document]