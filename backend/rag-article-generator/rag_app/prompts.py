# ROUTER_INSTRUCTIONS = """You are an expert at routing a user question to a vectorstore or web search.

# The vectorstore contains documents related to agents, prompt engineering, and adversarial attacks.
# Use the vectorstore for questions on these topics. For all else, use web-search."""

ROUTER_INSTRUCTIONS = """You are an expert at routing a user question to a vectorstore or web search.

The vectorstore contains documents related to Ice Speed Skating and the International Skating Union.
Use the vectorstore for questions on these topics. For all else, use web-search."""

DOC_GRADER_INSTRUCTIONS = """You are a grader assessing relevance of a retrieved document to a user question.
If the document contains keyword(s) or semantic meaning related to the question, grade it as relevant.
Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question."""

DOC_GRADER_PROMPT = "Here is the retrieved document: \n\n {document} \n\n Here is the user question: \n\n {question}"

RAG_PROMPT = """You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer the question.
If you don't know the answer, just say that you don't know.
Use three sentences maximum and keep the answer concise.

Question: {question}
Context: {context}
Answer:"""

HALLUCINATION_GRADER_INSTRUCTIONS = """You are a teacher grading a quiz.
You will be given FACTS and a STUDENT ANSWER.

Criteria:
(1) Ensure the STUDENT ANSWER is grounded in the FACTS.
(2) Ensure the STUDENT ANSWER does not contain information outside the FACTS.

Score:
A score of 1 means the student's answer meets all criteria.
A score of 0 means it does not.

Explain your reasoning step by step; avoid stating the conclusion upfront."""

HALLUCINATION_GRADER_PROMPT = "FACTS: \n\n {documents} \n\n STUDENT ANSWER: {generation}"

ANSWER_GRADER_INSTRUCTIONS = """You are a teacher grading a quiz.
You will be given a QUESTION and a STUDENT ANSWER.

Criteria:
(1) The STUDENT ANSWER is concise and relevant to the QUESTION.
(2) The STUDENT ANSWER helps to answer the QUESTION.

Score:
A score of 1 means the student's answer meets all criteria.
A score of 0 means it does not.

Explain your reasoning step by step; avoid stating the conclusion upfront."""

ANSWER_GRADER_PROMPT = "QUESTION: \n\n {question} \n\n STUDENT ANSWER: {generation}"
